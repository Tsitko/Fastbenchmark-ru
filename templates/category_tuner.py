def category_tuner(use=False, categories=10, cross_validations=5):
    if use:
        global real_train
        global real_test
        global real_target
        global train
        global test

        # more rounds -> better prediction, but longer training
        num_boost_rounds = 1000
        eta = 10 / num_boost_rounds

        step_score = 0
        for i in range(cross_validations):
            train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2, random_state=i)
            dtrain = xgb.DMatrix(train, target)
            dtest = xgb.DMatrix(test)
            model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
            preds = model.predict(dtest)
            preds = pd.to_numeric(preds)
            preds[pd.isna(preds)] = np.nanmean(preds)
            step_score += np.sqrt(mean_squared_error(np.round(test_target), preds))
        initial_score = step_score / cross_validations
        print('initial score = ' + str(initial_score))

        to_encode = []
        for cat in real_train.columns:
            if (len(np.unique(real_train[cat])) <= categories) and (len(np.unique(real_train[cat])) > 2):
                step_score = 0
                for i in range(cross_validations):
                    train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                        random_state=i)
                    encode_func(cat, one_hot=True, print_param=False, encode=False, cat_tune=True)
                    dtrain = xgb.DMatrix(train, target)
                    dtest = xgb.DMatrix(test)
                    model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
                    preds = model.predict(dtest)
                    preds = pd.to_numeric(preds)
                    preds[pd.isna(preds)] = np.nanmean(preds)
                    step_score += np.sqrt(mean_squared_error(np.round(test_target), preds))
                score = step_score / cross_validations
                print('Score for ' + str(cat) + ': ' + str(score))
                if score < initial_score:
                    to_encode.append(cat)
        for cat in to_encode:
            train = real_train
            test = real_test
            encode_func(cat, one_hot=True, print_param=False, encode=False)
            real_train = train
            real_test = test