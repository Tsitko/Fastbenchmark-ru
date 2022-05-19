col_name = train.columns[%target%]

if col_name in train.columns:
    # dealing with NaN values
    target = pd.to_numeric(train[col_name], errors='coerce')
    if col_name in test.columns:
        test_target = pd.to_numeric(test[col_name], errors='coerce')
        test_target[pd.isna(test_target)] = np.nanmean(train[col_name])
    target[pd.isna(target)] = np.nanmean(target)

    to_drop.append(col_name)
else:
    print('No ' + str(col_name) + ' in data set')
    errors.append('No ' + str(col_name) + ' in data set')
    to_drop.append(col_name)