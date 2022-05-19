print('Root mean squared error for prediction = '
      + str(np.sqrt(mean_squared_error(test_target, preds))))
sequence_length = min(sequence_length, len(preds), len(test_target))
pred_sequence = preds[0:sequence_length]
test_sequence = test_target[0:sequence_length]
for_plot = pd.DataFrame({'Predicted': pred_sequence, 'Real values': test_sequence})
for_plot = for_plot.sort_values(by='Real values')
for_plot.index = range(sequence_length)
sns.lineplot(data=for_plot)