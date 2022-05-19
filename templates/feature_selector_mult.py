def feature_selector(use=False, cross_validations=5, use_top=5, num_rounds=100):
    best_features = xgb_fea_imp['feature'].values.tolist()
    if use:
        global real_train
        global real_test
        global real_target

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
            step_score += mean_absolute_error(np.round(test_target), preds)
        initial_score = step_score / cross_validations
        print('initial score = ' + str(initial_score))
        to_use = xgb_fea_imp['feature'].values.tolist()[0:use_top]
        score = initial_score
        tested = []
        if num_rounds > 2 ** (len(xgb_fea_imp['feature']) - use_top):
            try_samples = []
            for L in range(0, len(xgb_fea_imp['feature']) - use_top + 1):
                for sample in itertools.combinations(range(use_top, len(xgb_fea_imp['feature'])), L):
                    try_samples.append(sample)
        for rnd in range(min(num_rounds, 2 ** (len(xgb_fea_imp['feature']) - use_top))):
            print('round ' + str(rnd + 1))
            use_in_round = to_use
            if num_rounds < 2 ** (len(xgb_fea_imp['feature']) - use_top):
                while True:
                    random_features = np.random.random_integers(use_top, len(xgb_fea_imp['feature']) - 1,
                                                                len(xgb_fea_imp['feature']) - use_top)
                    extra_features = xgb_fea_imp['feature'][random_features].tolist()
                    features = set(use_in_round + extra_features)
                    if features not in tested:
                        tested.append(features)
                        break
                use_in_round = list(features)
            else:
                random_features = list(try_samples[rnd])
                extra_features = xgb_fea_imp['feature'][random_features].tolist()
                features = set(use_in_round + extra_features)
                use_in_round = list(features)
            step_score = 0
            for i in range(cross_validations):
                train, test, target, test_target = train_test_split(real_train[use_in_round],
                                                                    real_target, test_size=0.2, random_state=i)
                dtrain = xgb.DMatrix(train, target)
                dtest = xgb.DMatrix(test)
                model = xgb.train(dict(xgb_params), dtrain, num_boost_round=num_boost_rounds)
                preds = model.predict(dtest)
                preds = pd.to_numeric(preds)
                preds[pd.isna(preds)] = np.nanmean(preds)
                step_score += mean_absolute_error(np.round(test_target), preds)
            step_score = step_score/cross_validations
            print('round score = ' + str(step_score) +'\n')
            if step_score < score:
                score = step_score
                best_features = use_in_round
        return score, best_features
    else:
        return np.Inf, best_features