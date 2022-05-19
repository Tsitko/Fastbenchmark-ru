# CATEGORY COLUMN - %colName%

col_name = train.columns[%cat_col%]
try:
    sns.displot(x=train.dropna()[col_name], hue=train.dropna()[target_col_name])
except:
    sns.distplot(train[col_name].dropna())