try:
    sns.displot(x=train[col_name])
except:
    sns.distplot(train[col_name])