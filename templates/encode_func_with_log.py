def encode_func(col_name, distribution=False, one_hot=False, categories=None, encode=True, print_param=True,
                cat_tune=False):
    global train
    global test
    try:
        encode_log_col = {
            'name': col_name,
            'new_name': col_name,
            'one_hot': one_hot,
            'values': np.unique(train[col_name]).tolist(),
            'new_values': np.unique(train[col_name]).tolist()
        }
    except:
        encode_log_col = {
            'name': col_name,
            'new_name': col_name,
            'one_hot': one_hot,
            'categories': categories,
            'values': np.unique(train[col_name].astype(str)).tolist(),
            'new_values': np.unique(train[col_name].astype(str)).tolist()
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

    # replacing category names with numbers
    if encode:
        encoder = LabelEncoder()
        encoder.fit(train[col_name].astype(str))
        train[col_name + '_encoded'] = encoder.transform(train[col_name].astype(str))
        try:
            test[col_name + '_encoded'] = encoder.transform(test[col_name].astype(str))
            encode_log_col['new_values'] = encoder.transform(encode_log_col['values']).tolist()
        except:
            encoder = LabelEncoder()
            encoder.fit(train[col_name].append(test[col_name]).astype(str))
            train[col_name + '_encoded'] = encoder.transform(train[col_name].astype(str))
            test[col_name + '_encoded'] = encoder.transform(test[col_name].astype(str))
            if max(test[col_name + '_encoded']) > max(train[col_name + '_encoded']):
                other_cat = max(train[col_name + '_encoded']) + 1
                test[col_name + '_encoded'][test[col_name + '_encoded'] > max(train[col_name + '_encoded'])] = other_cat
            encode_log_col['new_values'] = encoder.transform(encode_log_col['values']).tolist()
            for j in range(len(encode_log_col['new_values'])):
                if encode_log_col['new_values'][j] > max(train[col_name + '_encoded']):
                    encode_log_col['new_values'][j] = other_cat
        if print_param:
            print('encode parameters:')
            keys = encoder.classes_
            values = encoder.transform(encoder.classes_)
            dictionary = dict(zip(keys, values))
            for key in dictionary.keys():
                print(str(key) + ': ' + str(dictionary[key]))
        to_drop.append(col_name)
        col_name = col_name + '_encoded'

        # dealing with NaN values
        train[col_name] = pd.to_numeric(train[col_name], errors='coerce')
        train[col_name][pd.isna(train[col_name])] = nan_categorical(train[col_name])
        test[col_name] = pd.to_numeric(test[col_name], errors='coerce')
        test[col_name][pd.isna(test[col_name])] = nan_categorical(train[col_name])

    if (distribution and not one_hot) or (categories is not None):
        new_codes_train = [0] * train[col_name]
        new_codes_test = [0] * test[col_name]
        encode_log_new_values = [0] * len(encode_log_col['new_values'])
        i = 0
        for value in train[col_name].value_counts().index:
            for j in range(len(encode_log_new_values)):
                if encode_log_col['new_values'][j] == value:
                    encode_log_new_values[j] = i
            new_codes_train[train[col_name] == value] = i
            new_codes_test[test[col_name] == value] = i
            i += 1
        train[col_name] = new_codes_train
        test[col_name] = new_codes_test
        encode_log_col['new_values'] = encode_log_new_values

    if categories is not None:
        categories = categories - 1
        for j in range(len(encode_log_col['new_values'])):
            if encode_log_col['new_values'][j] >= categories:
                encode_log_col['new_values'][j] = categories
        train[col_name][train[col_name] >= categories] = categories
        test[col_name][test[col_name] >= categories] = categories

    if one_hot and len(set(train[col_name])) > 2:
        for i in range(len(encode_log['columns'])):
            if encode_log['columns'][i]['name'] == col_name:
                encode_log['columns'][i]['one_hot'] = True
        try:
            col_names = []
            for i in range(len(set(train[col_name].append(test[col_name])))):
                col_names.append(col_name + '_' + str(i))
            enc = LabelBinarizer()
            enc.fit(train[col_name].append(test[col_name]))
            new_features = pd.DataFrame(enc.transform(train[col_name]), columns=col_names)
            new_features.index = train.index
            train = train.join(new_features)
            new_features = pd.DataFrame(enc.transform(test[col_name]), columns=col_names)
            new_features.index = test.index
            test = test.join(new_features)
            to_drop.append(col_name)
        except: pass

    encode_log_col['new_name'] = col_name
    for i in range(len(encode_log['columns'])):
        if encode_log['columns'][i]['name'] == col_name:
            encode_log['columns'][i] = encode_log_col
    if not cat_tune:
        with open(str(target_col_name) + '_encode.log', 'w') as file:
            json.dump(encode_log, file)

    return None

