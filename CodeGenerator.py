# -*- encoding: utf-8 -*-

#dataPath = "C:/Projects/ML/TP1/BankChurners.csv"
#target_column_name = "Gender"
import DataTable
import MakeData
import re
import json

def make_names(strng):
    strng = re.sub('[^a-zA-Z0-9\n]', '_', strng)
    return strng

class CodeGenerator(object):

    def __init__(self, DataTable, project_path, testing=False):
        self.csvSeparator = DataTable.getCsvSeparator()
        self.dataPath = DataTable.getDataPath()
        self.data_file_name = ''
        self.names = DataTable.getColNames()
        self.colTypes = DataTable.getColTypes()
        self.target_column_name = DataTable.getTargetName()
        self.target_col_template = None
        self.colTemplates = DataTable.getColTemplate()
        self.client_file_path = DataTable.getDataPath()
        self.metric = DataTable.getMetric()
        self.drop_unselected = DataTable.getDropUnselected()
        self.target_type = DataTable.getTargetType()
        self.code = []
        self.project_path = project_path
        self.testing = testing
        if '\\' in self.dataPath:
            self.data_file_name = self.dataPath.split('\\')[-1]
        elif '/' in self.dataPath:
            self.data_file_name = self.dataPath.split('/')[-1]
        else:
            self.data_file_name = self.dataPath

    def md_from_template(self, text='', template='', start=False, end=False, *args):
        if start:
            with open('templates/md/first_md_cell_start', 'r') as file:
                codePart = file.read()
                self.code.append(codePart)
        else:
            with open('templates/md/md_cell_start', 'r') as file:
                codePart = file.read()
                self.code.append(codePart)
        if text == '':
            if str(template) != '':
                with open('templates/md/' + str(template), 'rb') as file:
                    codePart = file.read().decode('utf-8')
                    codePart = codePart.format(*args)
                    for line in codePart.split('\n'):
                        line = json.dumps(line)
                        line = line.replace('\"', '')
                        line = line.replace('\r\n', '')
                        line = '\"' + line + '\\n",\n'
                        self.code.append(line)
                    self.code[len(self.code) - 1] = self.code[len(self.code) - 1][:-2]
            else:
                with open('templates/md/' + str(template), 'r') as file:
                    codePart = file.read()
                    codePart = codePart.format(*args)
                    for line in codePart.split('\n'):
                        line = '\"' + line + '\\n",\n'
                        self.code.append(line)
                    self.code[len(self.code) - 1] = self.code[len(self.code) - 1][:-2]
        else:
            line = text
            line = json.dumps(line)
            line = line.replace('\"', '')
            line = line.replace('\r\n', '')
            line = '\"' + line + '\"'
            self.code.append(line.format(*args))
        if end:
            with open('templates/md/last_md_cell_end') as file:
                codePart = file.read()
                self.code.append(codePart)
        else:
            with open('templates/md/md_cell_end') as file:
                codePart = file.read()
                self.code.append(codePart)


    def code_from_template(self, category_key='%cat_key%', template='', col_name_key='%colName%',
                           data_template_key='%data_template_key%', start=False, end=False, read_data=False,
                           index=1, data_template='%DataTemplate%', col=False, fea_eng=False, hide=True):
        if start:
            with open('templates/first_code_cell_start', 'r') as file:
                codePart = file.read()
                self.code.append(codePart)
        else:
            if hide:
                with open('templates/code_cell_start', 'r') as file:
                    codePart = file.read()
            else:
                with open('templates/code_cell_start_no_hide', 'r') as file:
                    codePart = file.read()
            if col:
                if fea_eng:
                    if col_name_key in codePart:
                        codePart = codePart.replace(col_name_key, 'feature_eng')
                else:
                    if col_name_key in codePart:
                        codePart = codePart.replace(col_name_key, make_names(self.names[index]))
            else:
                if col_name_key in codePart:
                    codePart = codePart.replace('\"' + str(col_name_key) + '\"', '\"Pass_this_part\"')
            self.code.append(codePart)
        with open('templates/' + str(template), 'r') as file:
            codePart = file.read()
            if read_data:
                codePart = codePart.replace('%target_column_name%', str('\'' + self.target_column_name + '\''))
                codePart = codePart.replace('%data_path%', str('\'' + self.client_file_path.replace('\\', '\\\\') + '\''))
                codePart = codePart.replace('%separator%', str('\'' + self.csvSeparator + '\''))
            else:
                if category_key in codePart:
                    codePart = codePart.replace(category_key, str(index))
                if data_template_key in codePart:
                    codePart = codePart.replace(data_template_key, data_template)
                if col_name_key in codePart:
                    codePart = codePart.replace(col_name_key, make_names(self.names[index]))
        for line in codePart.split('\n'):
            if self.testing:
                if line != 'plt.show()':
                    line = '\"' + line + '\\n",\n'
                    self.code.append(line)
            else:
                line = '\"' + line + '\\n",\n'
                self.code.append(line)
        self.code[len(self.code) - 1] = self.code[len(self.code) - 1][:-2]
        if end:
            with open('templates/last_code_cell_end', 'r') as file:
                codePart = file.read()
                self.code.append(codePart)
        else:
            with open('templates/code_cell_end', 'r') as file:
                codePart = file.read()
                self.code.append(codePart)

    def readData(self):
        self.md_from_template('', 'read_data_head.md', True, False, self.target_column_name, self.data_file_name,
                              self.target_column_name, self.data_file_name)
        self.code_from_template(read_data=True, template='readData.py', start=False)
        self.md_from_template('', 'read_data_tail.md', False, False, self.target_column_name)
        self.md_from_template('Посмотрим на данные:',
                              '', False, False)
        self.code_from_template(template='print_data.py')
        if self.target_type in ['category', 'category_bool']:
            self.code_from_template(template='pairplot_cat.py')
        else:
            self.code_from_template(template='pairplot.py')

    def nan_func(self):
        self.md_from_template('', 'nan_func_head.md', False, False)
        self.code_from_template(template='nan.py')

    def encode_func(self):
        self.md_from_template('', 'encode_func_head.md', False, False)
        self.code_from_template(template='encode_func_with_log.py')



    def dateCol(self, index):
        self.md_from_template('', 'date_head.md', False, False, self.names[index], self.names[index],
                              self.target_column_name)
        self.code_from_template(category_key='%date_col%', template='dates.py', index=index, col=True)
        self.md_from_template('', 'date_tail.md', False, False, self.names[index],
                              self.names[index], self.names[index], self.names[index],
                              self.names[index], self.names[index], self.names[index],
                              self.names[index], self.target_column_name)
        if self.target_type in ['category', 'category_bool', 'string']:
            for date_type in ['year', 'month', 'week', 'weekday', 'monthday', 'hour', 'minute', 'second']:
                self.md_from_template('Распределение сгенерированной переменной для разных значений целевой переменной **{}**. Если '
                                      'у сгененрированной переменной только одно уникальное значение, мы удали её',
                                      '', False, False, date_type, self.target_column_name)
                self.code_from_template(template='date_temp_cat.py',
                                        data_template_key='%col_name%', data_template=date_type)

        else:
            for date_type in ['year', 'month', 'week', 'weekday', 'monthday', 'hour', 'minute', 'second']:
                self.md_from_template('Распределение сгенерированной переменной для разных значений целевой переменной **{}**. Если '
                                      'у сгененрированной переменной только одно уникальное значение, мы удали её',
                                      '', False, False, date_type, self.target_column_name)
                self.code_from_template(template='date_temp.py',
                                        data_template_key='%col_name%', data_template=date_type)

    def dateColTemp(self, index, template):
        self.code_from_template(category_key='%date_col%', template='datesTemp.py', index=index,
                                data_template_key='%dateTemplate%', data_template=template, col=True)

    def catCol(self, index):
        self.md_from_template('', 'catcol.md', False, False, self.names[index], self.names[index],
                              self.target_column_name)
        if self.target_type in ['category', 'category_bool', 'string']:
            if self.colTemplates[index] == 'numeric':
                self.code_from_template(template='catcol_hist_cat-num.py', category_key='%cat_col%', index=index)
                self.code_from_template(category_key='%cat_col%', template='category-num.py', index=index, col=True)
            else:
                self.code_from_template(template='catcol_hist_cat.py', category_key='%cat_col%', index=index)
                self.code_from_template(category_key='%cat_col%', template='category.py', index=index, col=True)
        else:
            if self.colTemplates[index] == 'numeric':
                self.code_from_template(template='catcol_hist-num.py', category_key='%cat_col%', index=index)
                self.code_from_template(category_key='%cat_col%', template='category-num.py', index=index, col=True)
                self.md_from_template('Распределение переменной **{}** для разных значений **{}**.',
                                      '', False, False, self.target_column_name, self.names[index])
                self.code_from_template(template='catcol_hist_target.py')
            else:
                self.code_from_template(template='catcol_hist.py', category_key='%cat_col%', index=index)
                self.code_from_template(category_key='%cat_col%', template='category.py', index=index, col=True)
                self.md_from_template('Распеделение перменной **{}** для разных значений **{}**.',
                                      '', False, False, self.target_column_name, self.names[index])
                self.code_from_template(template='catcol_hist_target.py')

    def textCol(self, index):
        self.md_from_template('', 'text_head.md', False, False, self.names[index])
        self.code_from_template(category_key='%text_col%', template='text.py', index=index, col=True)

    def drop_all_na(self):
        self.code_from_template(template='drop_all_na_func.py')
        self.md_from_template('Измените значение use на True, чтобы удалить все записи с NaN',
                              '', False, False)
        self.code_from_template(template='drop_all_na_config.py', hide=False)

    def numCol(self, index):
        self.md_from_template('', 'numeric.md', False, False, self.names[index], self.names[index],
                              self.target_column_name)
        self.code_from_template(category_key='%numeric_col%', template='numeric_head.py', index=index)
        self.md_from_template('Статистика переменной **{}**',
                              '', False, False, self.names[index])
        self.code_from_template(template='numeric_stat.py')
        self.md_from_template('Преобразование переменной **{}** для использования в ML модели.',
                              '', False, False, self.names[index])
        self.code_from_template(category_key='%numeric_col%', template='numeric.py', index=index, col=True)
        if self.target_type not in ['category', 'category_bool', 'string']:
            self.md_from_template('Посмотрим на корреляцию переменных **{}** и **{}**',
                                  '', False, False, self.target_column_name, self.names[index])
            self.code_from_template(category_key='%numeric_col%', template='numeric_cor.py', index=index)
            self.md_from_template('Если корреляция достаточно большая, отобразим её на графике',
                                  '', False, False, self.target_column_name, self.names[index])
            self.code_from_template(category_key='%numeric_col%', template='numeric_cor_plot.py', index=index)
            self.md_from_template('Также может быть полезным добавить логарифм переменной, как новую переменную,'
                                  'посмотрим на распределение этой новой переменной:',
                                  '', False, False, self.target_column_name, self.names[index])
            self.code_from_template(category_key='%numeric_col%', template='numeric_log.py', index=index)
        else:
            self.md_from_template('Посмотрим на распределение для разных значений целевой переменной:',
                                  '', False, False, self.target_column_name, self.names[index])
            self.code_from_template(template='numeric_plot_cat_target.py')
            self.md_from_template('Также может быть полезным добавить логарифм переменной, как новую переменную,'
                                  'посмотрим на распределение этой новой переменной:',
                                  '', False, False, self.target_column_name, self.names[index])
            self.code_from_template(category_key='%numeric_col%', template='numeric_log.py', index=index)

    def cleanData(self):
        self.md_from_template('', 'drop_head.md', False, False)
        self.code_from_template(template='drop.py')

    def cleanData_final(self):
        self.md_from_template('', 'drop_final_head.md', False, False)
        self.code_from_template(template='drop_final.py')

    def target(self, index):
        if self.target_type in ['category', 'category_bool', 'string'] and self.target_col_template is None:
            self.md_from_template('', 'target_cat_head.md', False, False, self.target_column_name,
                                  self.target_column_name)
            self.code_from_template(category_key='%target%', template='target_cat_hist.py', index=index,
                                    data_template_key='%category_type%', data_template=self.target_type)
            self.code_from_template(category_key='%target%', template='targetcat.py', index=index,
                                    data_template_key='%category_type%', data_template=self.target_type)
        elif self.target_type in ['category', 'category_bool', 'string'] and self.target_col_template == 'numeric':
            self.md_from_template('', 'target_cat_head.md', False, False, self.target_column_name,
                                  self.target_column_name)
            self.code_from_template(category_key='%target%', template='target_cat_hist-num.py', index=index,
                                    data_template_key='%category_type%', data_template=self.target_type)
            self.code_from_template(category_key='%target%', template='targetcat-num.py', index=index,
                                    data_template_key='%category_type%', data_template=self.target_type)
        else:
            self.md_from_template('', 'target_head.md', False, False, self.target_column_name, self.target_column_name)
            self.code_from_template(category_key='%target%', template='target.py', index=index)
            self.md_from_template('Статистика переменной {}', '', False, False, self.target_column_name)
            self.code_from_template(category_key='%target%', template='target_stat.py', index=index)
            self.md_from_template('Распределение переменной {}', '', False, False, self.target_column_name)
            self.code_from_template(category_key='%target%', template='target_hist.py', index=index)
            if self.metric == 'rmsle':
                self.md_from_template('', 'target_large_tail.md', False, False, self.target_column_name)
                self.code_from_template(category_key='%target%', template='target_log.py', index=index)

    def writeCode(self):
        with open(self.project_path + 'predict_' + str(self.target_column_name) + '.ipynb', 'w', errors='ignore') as file:
                file.writelines(self.code)
                file.close()
    def xgbModel(self):
        self.md_from_template('', 'xgb_head.md', False, False, self.target_column_name, self.target_column_name)
        if self.target_type == 'category' and self.target_col_template is None:
            self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                    template='xgbst_mult.py')
            self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_fimp.py')
            self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_mult_tail.py')
        elif self.target_type == 'category' and self.target_col_template == 'numeric':
            self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                    template='xgbst_mult-num.py')
            self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_fimp.py')
            self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_mult_tail-num.py')
        else:
            if self.target_type in ['category_bool'] and self.target_col_template is None:
                self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                        template='xgbst_bool.py')
                self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_fimp.py')
                self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_mult_tail.py')
                self.md_from_template('Посмотрим на значение интегральной кривой для неокругленных предсказанных данных'
                                      'и отобразим эти значения на графике', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_bool_reg.py')
            elif self.target_type in ['category_bool'] and self.target_col_template == 'numeric':
                self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                        template='xgbst_bool-num.py')
                self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_fimp.py')
                self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_mult_tail-num.py')
                self.md_from_template('Посмотрим на значение интегральной кривой для неокругленных предсказанных данных'
                                      'и отобразим эти значения на графике', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_bool_reg-num.py')
            else:
                if self.metric == 'rmsle':
                    self.code_from_template(data_template_key='%target_col_name%',
                                            data_template=self.target_column_name,
                                            template='xgbst_rmsle.py')
                    self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_fimp.py')
                    self.md_from_template('Точность предсказательной модели и график (данные целевой переменной отсортированы,'
                                          'чтобы можно было легко увидеть, на каких промежутках мы получаем наибольшие ошибки):', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_rmsle_tail.py')
                else:
                    self.code_from_template(data_template_key='%target_col_name%',
                                            data_template=self.target_column_name,template='xgbst.py')
                    self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_fimp.py')
                    self.md_from_template('Точность предсказательной модели и график (данные целевой переменной отсортированы,'
                                          'чтобы можно было легко увидеть, на каких промежутках мы получаем наибольшие ошибки):', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_tail.py')

    def fit_real(self, the_end=True, template='fit_real.md'):
        self.md_from_template('', template, False, False, self.target_column_name, self.target_column_name)
        if self.target_type == 'category' and self.target_col_template is None:
            self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                    template='fit_real_mult.py')
            self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_fimp.py')
            self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_mult_tail.py', end=the_end)
        elif self.target_type == 'category' and self.target_col_template == 'numeric':
            self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                    template='fit_real_mult-num.py')
            self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_fimp.py')
            self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                  False, False, self.target_column_name)
            self.code_from_template(template='xgbst_mult_tail-num.py', end=the_end)
        else:
            if self.target_type in ['category_bool'] and self.target_col_template is None:
                self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                        template='fit_real_bool.py')
                self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_fimp.py')
                self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_mult_tail.py')
                self.md_from_template('Посмотрим на значение интегральной кривой для неокругленных предсказанных данных'
                                      'и отобразим эти значения на графике', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_bool_reg.py', end=the_end)
            elif self.target_type in ['category_bool'] and self.target_col_template == 'numeric':
                self.code_from_template(data_template_key='%target_col_name%', data_template=self.target_column_name,
                                        template='fit_real_bool-num.py')
                self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_fimp.py')
                self.md_from_template('Классификационные метрики для предсказательной модели:', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_mult_tail-num.py')
                self.md_from_template('Посмотрим на значение интегральной кривой для неокругленных предсказанных данных'
                                      'и отобразим эти значения на графике', '',
                                      False, False, self.target_column_name)
                self.code_from_template(template='xgbst_bool_reg-num.py', end=the_end)
            else:
                if self.metric == 'rmsle':
                    self.code_from_template(data_template_key='%target_col_name%',
                                            data_template=self.target_column_name,
                                            template='fit_real_rmsle.py')
                    self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_fimp.py')
                    self.md_from_template('Точность предсказательной модели и график (данные целевой переменной отсортированы,'
                                          'чтобы можно было легко увидеть, на каких промежутках мы получаем наибольшие ошибки):', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_rmsle_tail.py', end=the_end)
                else:
                    self.code_from_template(data_template_key='%target_col_name%',
                                            data_template=self.target_column_name, template='fit_real.py')
                    self.md_from_template('Важность переменных для предсказательной модели для переменной **{}**:', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_fimp.py')
                    self.md_from_template('Точность предсказательной модели и график (данные целевой переменной отсортированы,'
                                          'чтобы можно было легко увидеть, на каких промежутках мы получаем наибольшие ошибки):', '',
                                          False, False, self.target_column_name)
                    self.code_from_template(template='xgbst_tail.py', end=the_end)

    def errorStat(self):
        self.md_from_template('', 'error_stat_head.md', False, False)
        self.code_from_template(template='error_stat_head.py')
        self.md_from_template('В этой части мы попробуем найти в обучающей выборке записи, наимоболее близкие '
                              'к записям из тестовой выборки, для которых мы получили максимальную ошибку', '',
                              False, False)
        self.code_from_template(template='error_stat_bottom.py')

    def fea_eng(self):
        self.md_from_template('', 'fea_eng_head.md', False, False)
        self.code_from_template(template='fea_eng_head.py')
        self.md_from_template('', 'fea_eng_middle.md', False, False)
        if self.testing:
            self.code_from_template(template='fea_eng_middle_test.py', col=True, fea_eng=True, hide=False)
            self.code_from_template(template='fea_eng_middle.py', hide=False)
        else:
            self.code_from_template(template='fea_eng_middle.py', col=True, fea_eng=True, hide=False)
        self.md_from_template('Измените значение _use_ на **True**, чтобы автоматически сгенерировать новые переменные', '', False, False)
        self.code_from_template(template='numeric_features.py')
        if self.testing:
            self.code_from_template(template='numeric_features_use_true.py', hide=False)
        else:
            self.code_from_template(template='numeric_features_use.py', hide=False)
        self.md_from_template('Тут мы обратно разделим data на тестовую и обучающую выборки', '',
                              False, False)
        self.code_from_template(template='fea_eng_tail.py')

    def cat_tuner(self):
        self.md_from_template('', 'cat_tune.md', False, False)
        if self.target_type == 'category':
            self.code_from_template(template='category_tuner_mult.py')
        elif self.target_type == 'category_bool':
            self.code_from_template(template='category_tuner_bool.py')
        elif self.metric == 'rmsle':
            self.code_from_template(template='category_tuner_log.py')
        else:
            self.code_from_template(template='category_tuner.py')
        self.md_from_template('Измените значение _use_ на **True** чтобы настроить категории'
                              ' (это может занять много времени)', '', False, False)
        self.code_from_template(template='category_tuner_middle.py', hide=False)

    def model_tuner(self):
        self.md_from_template('', 'model_tuner_head.md', False, False)
        if self.target_type == 'category':
            self.code_from_template(template='model_tuner_mult.py')
        elif self.target_type == 'category_bool':
            self.code_from_template(template='model_tuner_bool.py')
        elif self.metric == 'rmsle':
            self.code_from_template(template='model_tuner_log.py')
        else:
            self.code_from_template(template='model_tuner.py')
        self.md_from_template('Измените значение _use_ на **True** чтобы подобрать настройки модели'
                              ' (это может занять много времени)', '', False, False)
        self.code_from_template(template='model_tuner_middle.py', hide=False)

    def drop_unselected_func(self):
        self.md_from_template('## Удаление неиспользуемых переменных', '', False, False)
        uns_cols = ''
        for col in self.drop_unselected:
            uns_cols += '    \'' + str(col) + '\',\n'
        uns_cols = uns_cols[:-2]
        self.code_from_template(data_template_key='%unselectedCols%', data_template=uns_cols,
                                template='drop_unselected.py')
        if self.target_type in ['category', 'category_bool']:
            self.code_from_template(template='pairplot_cat.py')
        else:
            self.code_from_template(template='pairplot.py')

    def run(self):
        self.readData()
        if len(self.drop_unselected) > 0:
            self.drop_unselected_func()
        self.drop_all_na()
        self.nan_func()
        self.encode_func()
        for i in range(len(self.names)):
            if self.names[i] == self.target_column_name:
                self.target_col_template = self.colTemplates[i]
                self.target(i)
        for i in range(len(self.names)):
            if self.names[i] != self.target_column_name:
                if self.colTypes[i] == 'date':
                    if self.colTemplates[i] is None:
                        self.dateCol(i)
                    else:
                        self.dateColTemp(i, self.colTemplates[i])
                if self.colTypes[i] in ['category', 'category_bool']:
                    self.catCol(i)
                if self.colTypes[i] == 'string':
                    self.textCol(i)
                if self.colTypes[i] == 'numeric':
                    self.numCol(i)
        self.cleanData()
        self.xgbModel()
        self.errorStat()
        self.fit_real(the_end=False, template='fit_real.md')
        self.fea_eng()
        self.cat_tuner()
        self.model_tuner()
        self.cleanData_final()
        self.fit_real(the_end=True, template='fit_real_final.md')
        self.writeCode()
        return self.target_column_name



#if __name__ == '__main__':
    # DT = DataTable.DataTable([],[])
    # MD = MakeData.MakeData(dataPath, target_column_name)
    # DT.loadData(MD.MakeData())
    # CG = CodeGenerator(DT, dataPath)
    # CG.readData()
    # for i in range(0, len(DT.colTypes)):
    #     if DT.getColType(i+1) == 'target':
    #         CG.target(i)
    # for i in range(0, len(DT.colTypes)):
    #     if DT.getColType(i+1) == 'date':
    #         if DT.getColTemplate(i+1) == 'None':
    #             CG.dateCol(i)
    #         else:
    #             CG.dateColTemp(i,DT.getColTemplate(i+1))
    #     if DT.getColType(i+1) == 'category' or DT.getColType(i+1) == 'category_bool':
    #         CG.catCol(i)
    #     if DT.getColType(i+1) == 'string':
    #         CG.textCol(i)
    #     if DT.getColType(i+1) == 'numeric':
    #         CG.numCol(i)
    # CG.cleanData()
    # CG.xgbModel()
    #
    # CG.writeCode()