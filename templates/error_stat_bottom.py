features = xgb_fea_imp['feature'][0:top_features].tolist()
to_compare = train_with_target
for feature in features:
    condition1 = train_with_target[feature] >= (mean_top_err[feature]*(1 - (dist/100))).values[0]
    condition2 = train_with_target[feature] < (mean_top_err[feature]*(1 + (dist/100))).values[0]
    condition = condition1 & condition2
    if to_compare[condition].shape[0] >= top_rows:
        to_compare = to_compare[condition]
    else:
        break
show_order = [target_col_name] + xgb_fea_imp['feature'].tolist()
to_compare[show_order].head(top_rows)