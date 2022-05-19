from spyne import Application, rpc, ServiceBase, Unicode
from spyne.protocol.json import JsonDocument
from spyne.server.wsgi import WsgiApplication
import pandas as pd
import numpy as np
import xgboost as xgb
import json
import pickle
from wsgiref.simple_server import make_server
import warnings
import sys
import os
%ipynb_functions%


warnings.simplefilter(action='ignore')
target_col_name = '%targetColName%'

host = '0.0.0.0'
port = 8000
token = ''
project_path = ''

class bot_generator(object):
    def __init__(self, structure, enc_log):
        self.structure = structure
        self.enc_log = enc_log
        self.target = self.structure['targetName']
        self.bot_code = []
        self.final_code = ''
        if str(self.target) + '_service_documentation.md' in os.listdir(project_path):
            if str(self.target) + '_bot.py' not in os.listdir(project_path):
                with open(str(project_path) + str(self.target) + '_service_documentation.md', 'rb') as file:
                    self.bot_code = file.read().decode('utf-8')
                self.bot_code = self.bot_code.split('```python:')[2].replace('```','')

    def generate_bot_code(self):
        if len(self.bot_code) >0:
            self.final_code = ''
            for line in self.bot_code.split('\n'):
                if line == 'token = \'\'':
                    line = 'token = ' + '\'' + str(token) + '\''
                self.final_code += line.replace('\t', '    ') + '\n'
                self.final_code = self.final_code.replace('token = \'\'', 'token = \'' + str(token) + '\'')
                self.final_code = self.final_code.replace('host = \'0.0.0.0\'', 'host = \'' + str(host) + '\'')
                self.final_code = self.final_code.replace('port = 8000', 'port = ' + str(port))
                self.final_code = self.final_code.replace('project_path = \'\'', 'project_path = ' + '\'' +
                                                          str(project_path) + '\'')


    def make_bot(self):
        if len(self.bot_code) > 0:
            self.generate_bot_code()
            if str(self.target) + '_bot.py' not in os.listdir(project_path):
                with open(str(project_path) + str(self.target) + '_bot.py', 'w') as file:
                    file.write(self.final_code)


class ModelFitter(object):

    def __init__(self):
        # reading structure
        try:
            with open(str(project_path) + str(target_col_name) + '_structure.json', 'r') as file:
                self.structure = json.load(file)
        except:
            print('No file with dataset structure. Use make_json.py to generate it.')
            quit()

        # reading encode log
        try:
            with open(str(project_path) + str(target_col_name) + '_encode.log', 'r') as file:
                self.enc_log = json.load(file)
        except:
            print('No encode log in path. Can\'t use prediction service without encode log')
            quit()

        # reading the final model and predicting
        try:
            self.final_model = pickle.load(open(str(project_path) + str(target_col_name) +
                                                '_predictcion_final_model.dat', 'rb'))
        except:
            print('No model to use. Check if ' + str(target_col_name) + '_predictcion_final_model.dat is in path')
            quit()

        # reading the dataset
        try:
            self.data = pd.read_csv(self.structure['dataPath'], self.structure['csvSeparator'])
        except:
            print('Csv with data set is not in path')
            quit()

        self.bot_generator = bot_generator(self.structure, self.enc_log)
        self.bot_generator.make_bot()
        self.pred_message = {
            'state': 'OK',
            'prediction': {}
        }
        self.error_message = {
            'state': 'error',
            'error_log': ''
        }

    def read_data(self, row):
        try:
            row = json.loads(row)
            row_df = pd.DataFrame(row, index=[0])
            for col in self.structure['columns']:
                if col['name'] not in row_df.columns:
                    if col['dataType'] == 'numeric':
                        row_df[col['name']] = nan_numeric(self.data[col['name']])
                        row_df[col['name'] + '_log'] = np.log(row_df[col['name']] + 1 - min(0, min(row_df[col['name']])))
                    if col['dataType'] == 'category':
                        if col['dataTemplate'] == 'numeric':
                            row_df[col['name']] = nan_categorical(self.data[col['name']])
                        else:
                            row_df[col['name']] = nan_categorical(self.data[col['name']])
                    if col['dataType'] == 'date':
                        row_df[col['name']] = np.nan
                else:
                    if col['dataType'] == 'numeric':
                        row_df[col['name']] = pd.to_numeric(row_df[col['name']], errors='coerce')
                        row_df[col['name']][pd.isna(row_df[col['name']])] = nan_numeric(self.data[col['name']])
                        row_df[col['name'] + '_log'] = np.log(row_df[col['name']] + 1 - min(0, min(row_df[col['name']])))

            return row_df
        except Exception as e:
            self.error_message['error_log'] = str(e)

    def make_prediction(self, row):
        for_model = self.read_data(row)
        if len(self.error_message['error_log']) > 0:
            return json.dumps(self.error_message)

        # preparing the data
        %code_parts_here%
        # cleaning the data
        for name in self.enc_log['to_drop_preproc']:
            if name in for_model.columns:
                del for_model[name]


        %fea_eng_part%

        # auto generate numeric features
        numeric_cols = []
        for col in self.structure['columns']:
            if col['dataType'] == 'numeric' and col['name'] != target_col_name:
                numeric_cols.append(col['name'])
        if len(numeric_cols) > 0:
            if str(numeric_cols[0]) + '_sqr' in self.final_model.feature_names:
                if str(numeric_cols[0]) + '_sqrt' in self.final_model.feature_names:
                    for_model = generate_numeric(numeric_cols, for_model, use=True)

        # category tuning
        if 'columns' in self.enc_log:
            for col in self.enc_log['columns']:
                if col['one_hot']:
                    for i in range(len(col['values'])):
                        if str(col['new_name']) + '_' + str(col['new_values'][i]) not in for_model.columns:
                            if for_model[col_name].values[0] == col['values'][i]:
                                for_model[str(col['new_name']) + '_' + str(col['new_values'][i])] = 1
                            else:
                                for_model[str(col['new_name']) + '_' + str(col['new_values'][i])] = 0
                            if col['new_name'] not in self.enc_log['to_drop']:
                                self.enc_log['to_drop'].append(col['new_name'])

        # cleaning the data
        for name in self.enc_log['to_drop']:
            if name in for_model.columns:
                del for_model[name]

        fea_order = self.final_model.feature_names
        fit_to= pd.DataFrame(columns = fea_order)
        for name in fea_order:
            fit_to[name] = for_model[name]

        dfor_model = xgb.DMatrix(fit_to)
        pred = self.final_model.predict(dfor_model)
        pred = pred[0]
        %pred_code_part%
        self.pred_message['prediction'] = {"prediction": str(pred), "probability": str(probability)}
        return json.dumps(self.pred_message)

    def test_first_row(self):
        row = self.data.loc[0,:]
        print('Testing for:\n' + str(row.to_json()))
        try:
            result = json.loads(self.make_prediction(str(row.to_json())))
            if result['state'] == 'error':
                print('wrong data format:\n')
                print(result['error_log'])
            else:
                prediction = result['prediction']['prediction']
                probability = result['prediction']['probability']
                print('prediction = ' + str(prediction) + '\t with probability = ' + str(probability))
        except Exception as e:
            print(e)


class Soap(ServiceBase):
    @rpc(Unicode, _returns=Unicode)
    def predict(ctx, data):
        return Fitter.make_prediction(data)






app = Application([Soap], tns='Predictor',
                          in_protocol=JsonDocument(validator='soft'),
                          out_protocol=JsonDocument())
application = WsgiApplication(app)

if __name__ == '__main__':
    Fitter = ModelFitter()
    Fitter.test_first_row()
    server = make_server(host, port, application)
    print('Service launched at ' + str(host) + ':' + str(port))
    server.serve_forever()