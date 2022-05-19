if col_name in test.columns:
    # encoding values
    encode_func(col_name, distribution=False, one_hot=False, categories=None)
# if there is no such column in test set - add information to errors and delete column in training set

else:
    print('No ' + str(col_name) + ' in test set')
    errors.append('No ' + str(col_name) + ' in test set')
    to_drop.append(col_name)
