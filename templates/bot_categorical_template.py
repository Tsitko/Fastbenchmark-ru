def %name%(bot, update):
    for col in enc_log['columns']:
        if col['name'] == '%name%':
            if len(col['values']) < 10:
                # decorator start
                decorator = dict([(col['values'][i],i) for i in range(len(col['values']))])
                # decorator end
                button = []
                values_array = np.asarray(col['values'])
                dec_keys_array = np.asarray(list(decorator.keys()))
                dec_values_array = np.asarray(list(decorator.values()))
                for i in range(len(col['values'])):
                    if col['values'][i] != 'nan':
                        button.append([InlineKeyboardButton(str(dec_keys_array[dec_values_array == i][0]),
                                                            callback_data=str(values_array[dec_values_array == i][0]))])
                button.append([InlineKeyboardButton('None of those', callback_data='other_answer')])
                reply_markup = InlineKeyboardMarkup(button)
                bot.message.reply_text(%name%_question, reply_markup=reply_markup)
            else:
                bot.message.reply_text(%name%_question)