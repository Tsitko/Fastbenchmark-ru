real_train = data.loc[real_train.index, :]
real_test = data.loc[real_test.index, :]
for col_name in real_train.columns:
    real_train[col_name] = pd.to_numeric(real_train[col_name], errors='coerce')
    real_test[col_name] = pd.to_numeric(real_test[col_name], errors='coerce')
    real_train[col_name][pd.isna(real_train[col_name])] = nan_numeric(real_train[col_name])
    real_test[col_name][pd.isna(real_test[col_name])] = nan_numeric(real_train[col_name])