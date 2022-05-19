# preparing the data and printing the statistics
xgb_fea_imp = pd.DataFrame(list(model.get_fscore().items()),
columns=['feature', 'importance']).sort_values('importance', ascending=False)
xgb_fea_imp.style.hide_index()