if len(set(train[col_name])) <= cat_coef:
    grid = sns.FacetGrid(train[train[col_name].notna()], col=col_name)
    try:
        grid.map(sns.histplot, target_col_name)
    except:
        grid.map(sns.distplot, target_col_name)