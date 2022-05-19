if len(set(train[target_col_name])) <= cat_coef:
    grid = sns.FacetGrid(train[train[target_col_name].notna()], col=target_col_name)
    try:
        grid.map(sns.histplot, col_name)
    except:
        grid.map(sns.distplot, col_name)