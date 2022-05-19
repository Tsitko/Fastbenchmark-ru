# MAKE MODEL

train = real_train
target = real_target
test = real_test
test_target = real_test_target
target_log = np.log(target + 1 - min(0, min(target)))

# more rounds -> better prediction, but longer training
num_boost_rounds = 1000
eta = 10/num_boost_rounds

# transforming the data for xgboost with log transformation for target
dtrain = xgb.DMatrix(train, target_log)
dtest = xgb.DMatrix(test)
dreal_test = xgb.DMatrix(real_test)
# training the model
model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
pickle.dump(model, open(str(target_col_name) + '_predictcion_final_model.dat', 'wb'))

# predict and back transformation
preds = model.predict(dtest)
preds = np.exp(preds) -1 + min(0, min(target))
preds = pd.to_numeric(preds)
preds[pd.isna(preds)] = np.nanmean(preds)

real_preds = model.predict(dreal_test)
real_preds = np.exp(real_preds) -1 + min(0, min(target))
real_preds = pd.to_numeric(real_preds)
real_preds[pd.isna(real_preds)] = np.nanmean(real_preds)