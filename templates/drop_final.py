# clean data
for name in to_drop:
    if name in train.columns:
        train = train.drop(name, axis=1)
    if name in test.columns:
        test = test.drop(name, axis=1)
    if name in real_train.columns:
        real_train = real_train.drop(name, axis=1)
    if name in real_test.columns:
        real_test = real_test.drop(name, axis=1)

if str(target_col_name) + '_encode.log' in os.listdir():
    with open(str(target_col_name) + '_encode.log', 'r') as file:
        enc_log = json.load(file)
    for name in to_drop:
        if name not in enc_log['to_drop']:
            enc_log['to_drop'].append(name)
    with open(str(target_col_name) + '_encode.log', 'w') as file:
        enc_log = json.dump(enc_log, file)
else:
    enc_log = {
        'to_drop': []
    }
    for name in to_drop:
        if name not in enc_log['to_drop']:
            enc_log['to_drop'].append(name)
    with open(str(target_col_name) + '_encode.log', 'w') as file:
        enc_log = json.dump(enc_log, file)