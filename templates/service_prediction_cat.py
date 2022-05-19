probability = 1
pred = round(pred)
for col in self.enc_log['columns']:
    if col['name'] == target_col_name:
        for i in range(len(col['new_values'])):
            if pred == col['new_values'][i]:
                pred = col['values'][i]
                break