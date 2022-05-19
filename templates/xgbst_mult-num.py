# MAKE MODEL

# subsample for feature engineering
real_train = train
real_target = target
real_test = test
real_test_target = test_target
train, test, target, test_target = train_test_split(train, target, test_size=0.2, random_state=1)

# more rounds -> better prediction, but longer training
num_boost_rounds = 1000
eta = 10/num_boost_rounds

# parameters for xgboost
xgb_params = {
    'eta': eta,
    'subsample': 0.80,
    'objective': 'multi:softmax',
    'num_class': len(np.unique(target)),
    'eval_metric': 'merror'
}

# transforming the data for xgboost
dtrain = xgb.DMatrix(train, target)
dtest = xgb.DMatrix(test)
dreal_test = xgb.DMatrix(real_test)
# training the model
model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)

# predict
preds = model.predict(dtest)
preds = pd.to_numeric(preds)
preds[pd.isna(preds)] = np.nanmean(preds)

real_preds = model.predict(dreal_test)
real_preds = pd.to_numeric(real_preds)
real_preds[pd.isna(real_preds)] = np.nanmean(real_preds)