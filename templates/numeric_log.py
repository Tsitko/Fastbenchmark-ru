if col_name in test.columns:
    train[col_name + '_log'] = np.log(train[col_name] + 1 - min(0, min(train[col_name])))
    test[col_name + '_log'] = np.log(test[col_name] + 1 - min(0, min(test[col_name])))
    try:
        sns.displot(x=train[col_name + '_log'])
    except:
        sns.distplot(train[col_name + '_log'])