if col_name in test.columns:
    if correlation_with_target >= correlation_level:
        train_sequence = train.sample(sequence_length)
        col_sequence = train_sequence[col_name]
        target_sequence = train_sequence[target_col_name]
        if np.nanmean(col_sequence) >= np.nanmean(target_sequence):
            target_sequence =  target_sequence*np.nanmean(col_sequence)/np.nanmean(target_sequence)
        else:
            col_sequence = col_sequence * np.nanmean(target_sequence) / np.nanmean(col_sequence)
        for_plot = pd.DataFrame({col_name: col_sequence, target_col_name: target_sequence})
        for_plot = for_plot.sort_values(by=target_col_name)
        for_plot.index = range(sequence_length)
        sns.lineplot(data=for_plot)