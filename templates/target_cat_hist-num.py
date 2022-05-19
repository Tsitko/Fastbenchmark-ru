# TARGET COLUMN (categorical) - %colName%

col_name = train.columns[%target%]
categoryType = '%category_type%'
try:
    sns.displot(x=train[col_name])
except:
    sns.distplot(train[col_name])