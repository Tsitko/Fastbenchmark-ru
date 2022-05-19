if col_name in test.columns:

    # dealing with NaNs in column
    train[col_name] = pd.to_numeric(train[col_name], errors='coerce')
    test[col_name] = pd.to_numeric(test[col_name], errors='coerce')
    train[col_name][pd.isna(train[col_name])] = nan_numeric(train[col_name])
    test[col_name][pd.isna(test[col_name])] = nan_numeric(train[col_name])
    numeric_cols.append(col_name)

# if there is no such column in test set - add information to errors and delete column in training set
else:
    print('No ' + str(col_name) + ' in test set')
    errors.append('No ' + str(col_name) + ' in test set')
    to_drop.append(col_name)
