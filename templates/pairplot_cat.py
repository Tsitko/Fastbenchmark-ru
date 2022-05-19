if len(train.columns) <= 10:
    try:
        sns.pairplot(train, hue=target_col_name)
    except: pass