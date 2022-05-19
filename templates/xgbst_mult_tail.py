for_plot = pd.DataFrame({'Id': range(len(preds_categorical)), 'Predictions': preds_categorical, 'Real values': test_target_categorical})
plt.rcParams['figure.figsize'] = (8.27, 11.69)
sns.scatterplot(data=for_plot, x='Id', y='Predictions', hue='Real values')
pd.DataFrame(classification_report(test_target_categorical, preds_categorical, output_dict=True)).T