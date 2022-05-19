
# DATE COLUMN WITH TEMPLATE - %colName%

template = '%dateTemplate%'
col_name = train.columns[%date_col%]
empty_col_train = [0]*len(train[col_name])
empty_col_test = [0]*len(test[col_name])

if col_name in test.columns:

    # New columns to train set to generate features from date

    train[col_name + '_month'] = empty_col_train
    train[col_name + '_year'] = empty_col_train
    train[col_name + '_weekday'] = empty_col_train
    train[col_name + '_monthday'] = empty_col_train

    # New columns to test set to generate features from date

    test[col_name + '_month'] = empty_col_test
    test[col_name + '_year'] = empty_col_test
    test[col_name + '_weekday'] = empty_col_test
    test[col_name + '_monthday'] = empty_col_test

    # generating features from date in train set

    for i, row in train.iterrows():
        if pd.notna(row[col_name]):
            try:
                rowdata = datetime.strptime(row[col_name], template)
            except:
                rowdata = np.nan
        else:
            rowdata = np.nan
        if pd.notna(rowdata):
            train.loc[i, col_name + '_month'] = rowdata.month
            train.loc[i, col_name + '_year'] = rowdata.year
            train.loc[i, col_name + '_weekday'] = rowdata.isoweekday()
            train.loc[i, col_name + '_monthday'] = rowdata.day
        else:
            train.loc[i, col_name + '_month'] = 0
            train.loc[i, col_name + '_year'] = 0
            train.loc[i, col_name + '_weekday'] = 0
            train.loc[i, col_name + '_monthday'] = 0

    # generating features from date in test set

    for i, row in test.iterrows():
        if pd.notna(row[col_name]):
            try:
                rowdata = datetime.strptime(row[col_name], template)
            except:
                rowdata = np.nan
        else:
            rowdata = np.nan
        if pd.notna(rowdata):
            test.loc[i, str(col_name + '_month')] = rowdata.month
            test.loc[i, str(col_name + '_year')] = rowdata.year
            test.loc[i, str(col_name + '_weekday')] = rowdata.isoweekday()
            test.loc[i, str(col_name + '_monthday')] = rowdata.day
        else:
            test.loc[i, str(col_name + '_month')] = 0
            test.loc[i, str(col_name + '_year')] = 0
            test.loc[i, str(col_name + '_weekday')] = 0
            test.loc[i, str(col_name + '_monthday')] = 0

    # deleting useless date column (features are already generated)

    to_drop.append(col_name)
    train[col_name + '_month'] = pd.to_numeric(train[col_name + '_month'])
    test[col_name + '_month'] = pd.to_numeric(test[col_name + '_month'])
    train[col_name + '_year'] = pd.to_numeric(train[col_name + '_year'])
    test[col_name + '_year'] = pd.to_numeric(test[col_name + '_year'])
    train[col_name + '_weekday'] = pd.to_numeric(train[col_name + '_weekday'])
    test[col_name + '_weekday'] = pd.to_numeric(test[col_name + '_weekday'])
    train[col_name + '_monthday'] = pd.to_numeric(train[col_name + '_monthday'])
    test[col_name + '_monthday'] = pd.to_numeric(test[col_name + '_monthday'])

# if there is no such column in test set - add information to errors and delete column in training set

else:
    print('No ' + str(col_name) + ' in test set')
    errors.append('No ' + str(col_name) + ' in test set')
    to_drop.append(col_name)