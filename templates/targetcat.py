if categoryType == 'category' or categoryType == 'category_bool':
    # replacing category names with numbers
    encoder = LabelEncoder()
    encoder.fit(train[col_name])
    target = encoder.transform(train[col_name])
    target_real_values = {'Category name': encoder.classes_.tolist(),
                          'Category value': encoder.transform(encoder.classes_).tolist()}
    encode_log_col = {
        'name': col_name,
        'new_name': col_name,
        'one_hot': 'False',
        'categories': 'None',
        'values': target_real_values['Category name'],
        'new_values': target_real_values['Category value']
    }
    if str(target_col_name) + '_encode.log' not in os.listdir():
        with open(str(target_col_name) + '_encode.log', 'w') as file:
            encode_log = {'columns': [encode_log_col],
                          'to_drop_preproc': [],
                          'to_drop': []}
            json.dump(encode_log, file)
    with open(str(target_col_name) + '_encode.log', 'r') as file:
        encode_log = json.load(file)

    new_col = True
    for i in range(len(encode_log['columns'])):
        if encode_log['columns'][i]['name'] == col_name:
            encode_log_col = encode_log['columns'][i]
            new_col = False
    if new_col:
        encode_log['columns'].append(encode_log_col)

    if col_name in test.columns:
        test_target = encoder.transform(test[col_name])
    to_drop.append(col_name)

    # dealing with NaN values
    target = pd.to_numeric(target, errors='coerce')
    target[pd.isna(target)] = np.nanmean(target)
    if col_name in test.columns:
        test_target = pd.to_numeric(test_target, errors='coerce')
        test_target[pd.isna(test_target)] = np.nanmean(test_target)

else:
    print('This version can predict only numeric and categorical values values')
    quit()



if col_name in train.columns:
    to_drop.append(col_name)
else:
    print('No ' + str(col_name) + ' in data set')
    errors.append('No ' + str(col_name) + ' in data set')
    to_drop.append(col_name)
