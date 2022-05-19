# how much top errors to work with
top_errors = 5

# how much best variables to use
top_features = 4

# how much rows from training set to look at
top_rows = 5

# how much could be the distance btw values in % to take them as similar (to assume that two values are in same claster)
dist = 5

preds_df = pd.DataFrame({'prediction': preds})
preds_df.index = test.index
test_target_df = pd.DataFrame({target_col_name: test_target})
test_target_df.index = test.index
target_df = pd.DataFrame({target_col_name: target})
target_df.index = train.index
test_with_target = test.join(test_target_df).join(preds_df)
train_with_target = train.join(target_df)
test_with_target = test.join(test_target_df).join(preds_df)
train_with_target = train.join(target_df)
test_with_target['abs_err'] = abs(test_with_target[target_col_name] - test_with_target['prediction'])
test_top_errors = test_with_target.sort_values(by='abs_err', ascending = False).head(top_errors)
mean_top_err = test_top_errors.describe().iloc[1:2, :]
show_order = [target_col_name, 'prediction', 'abs_err'] + xgb_fea_imp['feature'].tolist()
test_top_errors[show_order]