target_log = np.log(target + 1 - min(0, min(target)))
try:
    sns.displot(x=target_log)
except:
    sns.distplot(target_log)
