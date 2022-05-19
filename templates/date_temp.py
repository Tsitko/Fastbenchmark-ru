if len(set(train[col_name + '_%col_name%']))>1:
    grid = sns.FacetGrid(train, col=col_name + '_%col_name%')
    grid.map(sns.histplot, target_col_name)
else:
    to_drop.append(col_name + '_%col_name%')