for col in self.enc_log['columns']:
    if col['name'] == col_name:
        if not col['one_hot']:
            for i in range(len(col['values'])):
                if for_model[col_name].values[0] == col['values'][i]:
                    for_model[col['new_name']] = col['new_values'][i]
            if col['new_name'] not in for_model.columns:
                for_model[col['new_name']] = nan_categorical(self.data[col['name']])
        else:
            for i in range(len(col['values'])):
                if for_model[col_name].values[0] == col['values'][i]:
                    for_model[str(col['new_name']) + '_' + str(col['new_values'][i])] = 1
                else:
                    for_model[str(col['new_name']) + '_' + str(col['new_values'][i])] = 0