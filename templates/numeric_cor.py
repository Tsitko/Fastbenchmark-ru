if col_name in test.columns:
    correlation_with_target = abs(np.corrcoef(train[col_name], train[target_col_name])[0, 1])
    print('Correlation with target variable is ', correlation_with_target)
