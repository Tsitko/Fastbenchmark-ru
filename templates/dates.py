
# DATE COLUMN - %colName%

col_name = train.columns[%date_col%]

if col_name in test.columns:

    # Generating features from dates
    train[col_name] = pd.to_datetime(train[col_name])
    test[col_name] = pd.to_datetime(test[col_name])

    train[col_name + '_year'] = train[col_name].dt.year
    train[col_name + '_month'] = train[col_name].dt.month
    train[col_name + '_week'] = train[col_name].dt.weekofyear
    train[col_name + '_weekday'] = train[col_name].dt.dayofweek
    train[col_name + '_monthday'] = train[col_name].dt.day
    train[col_name + '_hour'] = train[col_name].dt.hour
    train[col_name + '_minute'] = train[col_name].dt.minute
    train[col_name + '_second'] = train[col_name].dt.second

    test[col_name + '_year'] = test[col_name].dt.year
    test[col_name + '_month'] = test[col_name].dt.month
    test[col_name + '_week'] = test[col_name].dt.weekofyear
    test[col_name + '_weekday'] = test[col_name].dt.dayofweek
    test[col_name + '_monthday'] = test[col_name].dt.day
    test[col_name + '_hour'] = test[col_name].dt.hour
    test[col_name + '_minute'] = test[col_name].dt.minute
    test[col_name + '_second'] = test[col_name].dt.second

    to_drop.append(col_name)

# if there is no such column in test set - add information to errors and delete column in training set

else:
    print('No ' + str(col_name) + ' in test set')
    errors.append('No ' + str(col_name) + ' in test set')
    to_drop.append(col_name)