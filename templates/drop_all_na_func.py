def drop_all_na(use=False):
    global train
    global test
    if use:
        train = train.dropna()
        test = test.dropna()
    else:
        train_lost_rate = round((1 - (train.dropna().shape[0] / train.shape[0])) * 100)
        test_lost_rate = round((1 - (test.dropna().shape[0] / test.shape[0])) * 100)
        print('Your train set will lost ' + str(train_lost_rate) + '% of its rows.')
        print('Your test set will lost ' + str(test_lost_rate) + '% of its rows.')
