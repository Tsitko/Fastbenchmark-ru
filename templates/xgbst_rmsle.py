# MAKE MODEL

# subsample for feature engineering
real_train = train
real_target = target
real_test = test
real_test_target = test_target
train, test, target, test_target = train_test_split(train, target, test_size=0.2, random_state=1)
target_log = np.log(target + 1 - min(0, min(target)))

# more rounds -> better prediction, but longer training
num_boost_rounds = 1000
eta = 10/num_boost_rounds

# parameters for xgboost
xgb_params = {
    'eta': eta,
    'subsample': 0.80
}

# transforming the data for xgboost with log transformation for target
dtrain = xgb.DMatrix(train, target_log)
dtest = xgb.DMatrix(test)
dreal_test = xgb.DMatrix(real_test)
# training the model
model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)

# predict and back transformation
preds = model.predict(dtest)
preds = np.exp(preds) -1 + min(0, min(target))
preds = pd.to_numeric(preds)
preds[pd.isna(preds)] = np.nanmean(preds)

real_preds = model.predict(dreal_test)
real_preds = np.exp(real_preds) -1 + min(0, min(target))
real_preds = pd.to_numeric(real_preds)
real_preds[pd.isna(real_preds)] = np.nanmean(real_preds)

