for_plot = pd.DataFrame({'Id': range(len(preds)), 'Predictions': np.round(preds), 'Real values': np.round(test_target)})
sns.scatterplot(data=for_plot, x='Id', y='Predictions', hue='Real values')
pd.DataFrame(classification_report(np.round(test_target), np.round(preds), output_dict=True)).T