def feature_selector(use=False, cross_validations=5):
    if use:
        global real_train
        global real_test
        global real_target
        global xgb_params

        features = real_train.columns

        # more rounds -> better prediction, but longer training
        num_boost_rounds = 1000
        eta = 10 / num_boost_rounds

        for i in range(cross_validations):
            train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2, random_state=i)
            dtrain = xgb.DMatrix(train, target)
            dtest = xgb.DMatrix(test)
            model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
            preds = model.predict(dtest)
            preds = pd.to_numeric(preds)
            preds[pd.isna(preds)] = np.nanmean(preds)
            fea_imp = pd.DataFrame(list(model.get_fscore().items()),
                                   columns=['feature', 'importance']).sort_values('importance', ascending=False)
            for feature in features:
                if feature not in fea_imp['feature'].values.tolist():
                    print('Useless feature: ' + str(feature))
                    features = features[features != feature]
        real_train = real_train[features]
        real_test = real_test[features]