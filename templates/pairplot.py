if len(train.columns) <= 10:
    try:
        sns.pairplot(train)
    except: pass