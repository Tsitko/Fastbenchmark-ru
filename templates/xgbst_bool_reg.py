for_plot = pd.DataFrame({'Id': range(len(preds)), 'Prediction': preds, 'Real values': test_target_categorical})
sns.scatterplot(data=for_plot, x='Id', y='Prediction', hue='Real values')
print('roc auc score is ' + str(roc_auc_score(np.round(test_target), preds)))
