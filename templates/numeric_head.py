# NUMERIC  COLUMN - %colName%

col_name = train.columns[%numeric_col%]
try:
    sns.displot(x=train[col_name].dropna())
except:
    sns.distplot(train[col_name].dropna())