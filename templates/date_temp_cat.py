if len(set(train[col_name + '_%col_name%']))>1:
    grid = sns.FacetGrid(train, col=target_col_name)
    try:
        grid.map(sns.histplot, col_name + '_%col_name%')
    except:
        grid.map(sns.distplot, col_name + '_%col_name%')
else:
    to_drop.append(col_name + '_%col_name%')