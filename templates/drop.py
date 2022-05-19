# clean data
for name in to_drop:
    if name in train.columns:
        train = train.drop(name, axis=1)
    if name in test.columns:
        test = test.drop(name, axis=1)


if str(target_col_name) + '_encode.log' in os.listdir():
    with open(str(target_col_name) + '_encode.log', 'r') as file:
        enc_log = json.load(file)
    for name in to_drop:
        if name not in enc_log['to_drop_preproc']:
            enc_log['to_drop_preproc'].append(name)
    with open(str(target_col_name) + '_encode.log', 'w') as file:
        enc_log = json.dump(enc_log, file)
else:
    enc_log = {
        'to_drop': [],
        'to_drop_preproc': []
    }
    for name in to_drop:
        if name not in enc_log['to_drop_preproc']:
            enc_log['to_drop_preproc'].append(name)
    with open(str(target_col_name) + '_encode.log', 'w') as file:
        enc_log = json.dump(enc_log, file)