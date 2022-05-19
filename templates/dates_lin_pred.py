secs_train = (datetime.now()-train[col_name]).dt.total_seconds()
secs_test = (datetime.now()-test[col_name]).dt.total_seconds()
regr = linear_model.LinearRegression()
regr.fit(secs_train.values.reshape(-1,1), target.values.reshape(-1,1))
prediction_train = regr.predict(secs_train.values.reshape(-1,1))[:,0].tolist()
prediction_test = regr.predict(secs_test.values.reshape(-1,1))[:,0].tolist()

sns.lineplot(data=pd.DataFrame({'Predictions': prediction_test[1:100],
                                'Real values': test_target[1:100]}))
train[col_name + '_lin_pred'] = prediction_train
test[col_name + '_lin_pred'] = prediction_test