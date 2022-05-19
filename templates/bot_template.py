from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import json
import numpy as np
import pandas as pd
import requests

project_path = ''

# fill your bot token here
token = ''

# change this if your service started not at localhost
host = 'http://localhost'

# change this if your server started not at 8000 port
port = 8000

# specify questions for your variables
%questions_for_variables%


# here is our target variable
target = '%target_col_name%'

# here are your variables
variables = %columns%

# hare are numeric categories
num_categories = %num_cats%

# reading your encode log
try:
    with open(str(project_path) + str(target) + '_encode.log') as file:
        enc_log = json.load(file)
except:
    print('No encode log in path. Can\'t start bot')

# HERE IS YOUR BOT

# check for new messages
updater = Updater(token=token)

# allow to register handler
dispatcher = updater.dispatcher

# here we will store our chats data
chats = []

# command callback handler
def start(bot, update):

    # if user is using start command, we will start dialog from the beginning
    data = {
%data%
    }

    chat = {
        "chat_id": bot.message.chat_id,
        "data": data
    }

    chat_added = False
    for i in range(len(chats)):
        if chats[i]['chat_id'] == chat['chat_id']:
            chats[i]['data'] = chat['data']
            chat_added = True
    if not chat_added:
        chats.append(chat)

    %first_col%(bot, update)

# create a command handler
start_handler = CommandHandler('start', start)

# add command handler to dispatcher
dispatcher.add_handler(start_handler)

# prediction function
def predict(bot, update):
    service_url = str(host) + ':' + str(port) + '/'
    data = None
    for i in range(len(chats)):
        if data is None and chats[i]['chat_id'] == bot.message.chat_id:
            data = chats[i]['data']
            print(data)
    if data is not None:
        try:
            params = json.dumps({"predict": {"data": str(json.dumps(data))}})
            responce = requests.get(service_url, data=params)
            print(responce.json())
            result = json.loads(responce.json())
            if result['state'] == 'error':
                bot.message.reply_text('Sorry, service is unavailable now')
                print('wrong data format for ' + str(bot.message.chat_id) + ':\n')
                print(result['error_log'])
            else:
                prediction = result['prediction']['prediction']
                probability = result['prediction']['probability']
                # print prediction and probability start
                print('prediction = ' + str(prediction) + '\t with probability = ' + str(probability))
                bot.message.reply_text('prediction = ' + str(prediction) + '\t with probability = ' + str(probability))
                # print prediction and probability end
        except Exception as e:
            print(e)
    else:
        print('incorrect data was formed in chat ' + str(bot.message.chat_id))


# functions for categorical variables
%categorical%
# functions for non-categorical variables
%numeric%
# function to find first question without an answer
def question_without_answer(chat_id):
    result = None
    for i in range(len(chats)):
        if chats[i]['chat_id'] == chat_id:
            for variable in variables:
                if chats[i]['data'][variable] == '' and result is None:
                    result = variable
                    return result


# handler for numeric variables and large categories
def txt(bot, update):
    last_question = question_without_answer(bot.message.chat_id)
    if last_question is not None:
        for i in range(len(chats)):
            if chats[i]['chat_id'] == bot.message.chat_id:
                chats[i]['data'][last_question] = bot.message.text
        next_question = question_without_answer(bot.message.chat_id)

%next_question%
        else:
            predict(bot, update)
    else:
        bot.message.reply_text('Use /start command to get new prediction')


text_handler = MessageHandler(Filters.text, txt)
dispatcher.add_handler(text_handler)


# handler for categorical variables
def button(bot, update):
    query = bot.callback_query
    answer = query.data
    if answer == 'other_answer':
        answer = np.nan
    last_question = question_without_answer(query.message.chat.id)
    if last_question is not None:
        for i in range(len(chats)):
            if chats[i]['chat_id'] == query.message.chat.id:
                if last_question in num_categories:
                    answer = pd.to_numeric(answer, errors='coerce')
                    if not pd.isna(answer):
                        answer = float(answer)
                    chats[i]['data'][last_question] = answer
                else:
                    chats[i]['data'][last_question] = answer
        next_question = question_without_answer(query.message.chat.id)

%next_question_query%
        else:
            predict(query, update)
    else:
        query.message.reply_text('Use /start command to get new prediction')



button_handler = CallbackQueryHandler(button)
dispatcher.add_handler(button_handler)

# start polling
while True:
    try:
        updater.start_polling()
        updater.idle()

    except Exception as e:
        time.sleep(5)