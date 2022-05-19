# CATEGORY COLUMN - %colName%
col_name = train.columns[%cat_col%]
try:
    sns.displot(x=train[col_name])
except:
    plt.hist(train[col_name].values.astype(str))
