
import pandas as pd
from datetime import datetime
import telegram

dateTemplates = ['%m/%d/%y', '%y/%m/%d', '%M/%D/%Y', '%Y/%M/%D', '%m-%d-%y', '%y-%m-%d', '%M-%D-%Y', '%Y-%M-%D']
csvSeparators = [',', ';', '\t']

class MakeData(object):
    def __init__(self, data_path, target_column_name, msg):
        self.data_path = data_path
        self.target_column_name = target_column_name
        self.csvSeparator = None
        self.data = None
        self.msg = msg
        self.errors = False

    def separator(self):
        for csvSeparator in csvSeparators:
            # read data
            try:
                dt = pd.read_csv(self.data_path, sep=csvSeparator)
                # cut data
                if dt.shape[0] > 1000:
                    dt = dt.sample(1000)
                if dt.shape[1] > 2:
                    self.csvSeparator = csvSeparator
                    self.data = dt
                    break
            except: pass
        if self.csvSeparator == None:
            self.msg.reply_text('Can\'t read csv (wrong format)')
            self.errors = True

    def check_for_date(self,col_name):
        temp = None
        if self.csvSeparator == None:
            self.separator()
        df = self.data.sample(30)
        val = df[col_name].values.tolist()
        rating = [0]*len(dateTemplates)
        i=0
        for template in dateTemplates:
           for v in val:
                try:
                    datetime.strptime(v, template)
                    rating[i] += 1
                except: pass
           i+=1
        if max(rating)>20:
            temp=dateTemplates[rating.index(max(rating))]
        return temp



    def dtype_to_str(self, dt, length=1000):
        if dt == "int64":
            if length <= 50:
                if length == 2:
                    return "category_bool"
                else:
                    return "category"
            else:
                return "numeric"
        if dt == "float64":
            return "numeric"
        if dt == "datetime":
            return "dates"
        if dt == "object":
            if length > 50:
                return "string"
            if length <= 50:
                if length == 2:
                    return "category_bool"
                else:
                    return "category"

    def define_data_types(self):
        if self.csvSeparator == None:
            self.separator()
        d = self.data.columns
        parts = []
        target = False
        for i in range(len(d)):
            if d[i] == self.target_column_name:

                part = {"dataType": "target",
                        "dataTemplate": self.dtype_to_str(self.data.dtypes[i].name, len(set(self.data[d[i]]))),
                        "Name": str(d[i])}
                target = True
            else:
                if self.dtype_to_str(self.data.dtypes[i].name)=='string':
                    temp = self.check_for_date(d[i])
                    if temp == None:
                        part = {"dataType": self.dtype_to_str(self.data.dtypes[i].name, len(set(self.data[d[i]]))),
                            "dataTemplate": "None",
                            "Name": str(d[i])}
                    else:
                        part = {"dataType": 'date',
                                "dataTemplate": temp,
                                "Name": str(d[i])}
                else:
                    part = {"dataType": self.dtype_to_str(self.data.dtypes[i].name, len(set(self.data[d[i]]))),
                        "dataTemplate": "None",
                        "Name": str(d[i])}
            parts.append(part)
        if not target:
            self.msg.reply_text('No ' + str(self.target_column_name) + ' in file.')
            self.errors = True
        return parts

    def MakeData(self):
        if self.csvSeparator == None:
            self.separator()
        if self.errors:
            return False
        else:
            dataFormat = {"csvSeparator": self.csvSeparator,
                   "dataPath": self.data_path,
                   "columns": self.define_data_types()}
            if self.errors:
                return False
            else:
                return dataFormat

