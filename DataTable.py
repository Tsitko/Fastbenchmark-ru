class DataTable(object):

    def __init__(self):
        self.colTypes = []
        self.colDataTemplates = []
        self.colNames = []
        self.csvSeparator = ','
        self.dataPath = ''
        self.data = None
        self.target_name = ''
        self.target_type = ''
        self.metric = 'rmse'
        self.drop_unselected = []

    def getMetric(self):
        return self.metric

    def getDropUnselected(self):
        return self.drop_unselected

    def getTargetName(self):
        return self.target_name

    def getTargetType(self):
        return self.target_type

    def getCsvSeparator(self):
        return self.csvSeparator

    def getDataPath(self):
        return self.dataPath

    def getColNames(self):
        return self.colNames

    def getColQuant(self):
        return len(self.colTypes)

    def getColTypes(self, position=None):
        if position == None:
            return self.colTypes
        if len(self.colTypes) < position or position <= 0:
            return None
        return self.colTypes[position]

    def getColTemplate(self, position=None):
        if position == None:
            return self.colDataTemplates
        else:
            return self.colDataTemplates[position]

    def loadData(self, data):
        try:
            data = data
            self.target_name = data['targetName']
            self.metric = data['metric']
            if 'to_drop' in data:
                self.drop_unselected = data['to_drop']
            for element in data['columns']:
                if element['name'] == self.target_name:
                    self.target_type = element['dataType']
                    self.colTypes.append(element['dataType'])
                    self.colNames.append(element['name'])
                    if element['dataTemplate'] == 'None':
                        self.colDataTemplates.append(None)
                    else:
                        self.colDataTemplates.append(element['dataTemplate'])
                else:
                    self.colTypes.append(element['dataType'])
                    self.colNames.append(element['name'])
                    if element['dataTemplate'] == 'None':
                        self.colDataTemplates.append(None)
                    else:
                        self.colDataTemplates.append(element['dataTemplate'])
            self.csvSeparator = data['csvSeparator']
            self.dataPath = data['dataPath']
        except: pass

