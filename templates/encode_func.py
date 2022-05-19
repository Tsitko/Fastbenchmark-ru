def encode_func(col_name, distribution=False, one_hot=False, categories=None, encode=True, print_param=True, cat_tune=False):
    global train
    global test

    # replacing category names with numbers
    if encode:
        encoder = LabelEncoder()
        encoder.fit(train[col_name].astype(str))
        train[col_name + '_encoded'] = encoder.transform(train[col_name].astype(str))
        try:
            test[col_name + '_encoded'] = encoder.transform(test[col_name].astype(str))
        except:
            encoder = LabelEncoder()
            encoder.fit(train[col_name].append(test[col_name]).astype(str))
            train[col_name + '_encoded'] = encoder.transform(train[col_name].astype(str))
            test[col_name + '_encoded'] = encoder.transform(test[col_name].astype(str))
            if max(test[col_name + '_encoded']) > max(train[col_name + '_encoded']):
                other_cat = max(train[col_name + '_encoded']) + 1
                test[col_name + '_encoded'][test[col_name + '_encoded'] > max(train[col_name + '_encoded'])] = other_cat
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
        new_codes_train = [0]*train[col_name]
        new_codes_test = [0]*test[col_name]
        i = 0
        for value in train[col_name].value_counts().index:
            new_codes_train[train[col_name] == value] = i
            new_codes_test[test[col_name] == value] = i
            i += 1
        train[col_name] = new_codes_train
        test[col_name] = new_codes_test

    if categories is not None:
        categories = categories - 1
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

    return None
