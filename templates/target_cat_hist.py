# TARGET COLUMN (categorical) - %colName%

col_name = train.columns[%target%]
categoryType = '%category_type%'
try:
    sns.displot(x=train[col_name], aspect=max(1.5,0.15*len(np.unique(train[col_name].astype(str)))))
except:
    plt.hist(train[col_name].values.astype(str))
plt.xticks(rotation=90)
plt.show()