# MAKE MODEL

train = real_train
target = real_target
test = real_test
test_target = real_test_target

# more rounds -> better prediction, but longer training
num_boost_rounds = 1000
eta = 10/num_boost_rounds

# transforming the data for xgboost
dtrain = xgb.DMatrix(train, target)
dtest = xgb.DMatrix(test)
dreal_test = xgb.DMatrix(real_test)
# training the model
model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
pickle.dump(model, open(str(target_col_name) + '_predictcion_final_model.dat', 'wb'))

# predict
preds = model.predict(dtest)
preds = pd.to_numeric(preds)
preds[pd.isna(preds)] = np.nanmean(preds)

real_preds = model.predict(dreal_test)
real_preds = pd.to_numeric(real_preds)
real_preds[pd.isna(real_preds)] = np.nanmean(real_preds)

preds_categorical = []
test_target_categorical = []
for i in range(len(preds)):
    if round(preds[i]) in target_real_values['Category value']:
        pred_name_index = target_real_values['Category value'].index(round(preds[i]))
    else:
        pred_name_index = target_real_values['Category value'].index(min(target_real_values['Category value']))
    test_target_name_index = target_real_values['Category value'].index(test_target[i])
    preds_categorical.append(target_real_values['Category name'][pred_name_index])
    test_target_categorical.append(target_real_values['Category name'][test_target_name_index])