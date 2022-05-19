def eval_metric(test_target, preds):
    return mean_absolute_error(np.round(test_target), preds)


def model_tuner(use=False, cross_validations=5):
    if use:
        global real_train
        global real_test
        global real_target
        global xgb_params

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
            step_score += eval_metric(test_target, preds)
        initial_score = step_score / cross_validations
        print('initial score = ' + str(initial_score))

        best_score = initial_score
        try_alpha = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        try_gamma = [1, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1]
        try_depth = [1, 2, 3, 4, 5, 7, 8, 9, 10]
        try_tree_method = ['exact', 'approx', 'hist']
        try_subsample = [0.5, 0.6, 0.7, 0.8, 0.9, 1]

        xgb_params_to_test = xgb_params.copy()
        for tree_method in try_tree_method:
            xgb_params_to_test['tree_method'] = tree_method
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                    random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params_to_test), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += eval_metric(np.round(test_target), preds)
            score = step_score / cross_validations
            print('Score for tree_method = ' + str(tree_method) + ': ' + str(score))
            if score < best_score:
                best_score = score
                xgb_params = xgb_params_to_test.copy()

        xgb_params_to_test = xgb_params.copy()
        for subsample in try_subsample:
            xgb_params_to_test['subsample'] = subsample
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                    random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params_to_test), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += eval_metric(test_target, preds)
            score = step_score / cross_validations
            print('Score for subsample = ' + str(subsample) + ': ' + str(score))
            if score < best_score:
                best_score = score
                xgb_params = xgb_params_to_test.copy()

        xgb_params_to_test = xgb_params.copy()
        for depth in try_depth:
            xgb_params_to_test['max_depth'] = depth
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                    random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params_to_test), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += eval_metric(test_target, preds)
            score = step_score / cross_validations
            print('Score for max_depth = ' + str(depth) + ': ' + str(score))
            if score < best_score:
                best_score = score
                xgb_params = xgb_params_to_test.copy()

        xgb_params_to_test = xgb_params.copy()
        for alpha in try_alpha:
            xgb_params_to_test['alpha'] = alpha
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                    random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params_to_test), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += eval_metric(test_target, preds)
            score = step_score / cross_validations
            print('Score for alpha = ' + str(alpha) + ': ' + str(score))
            if score < best_score:
                best_score = score
                xgb_params = xgb_params_to_test.copy()

        xgb_params_to_test = xgb_params.copy()
        for gamma in try_gamma:
            xgb_params_to_test['gamma'] = gamma
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train, real_target, test_size=0.2,
                                                                    random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params_to_test), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += eval_metric(np.round(test_target), preds)
            score = step_score / cross_validations
            print('Score for gamma = ' + str(gamma) + ': ' + str(score))
            if score < best_score:
                best_score = score
                xgb_params = xgb_params_to_test.copy()