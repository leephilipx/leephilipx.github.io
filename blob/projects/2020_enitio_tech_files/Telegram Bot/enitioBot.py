## ENITIO TELEGRAM BOT 2020 @testm20bot ##
## Permissions: admin, group privacy disabled ##

# pprint for readable display of dictionary
import time
import datetime
import telepot
from telepot.loop import MessageLoop
from pprint import pprint

# Initialise bot object
token = '''TOKEN GOES HERE'''
bot = telepot.Bot(token)

# Log print and log        ## Why must file manipulation be in a function
def logprint(log):
    global logfilename
    f = open(logfilename, 'a+')
    f.write(log + '\n')
    f.close
    print(log)

# Received chat message
def on_chat_message(response):
    global passwordListen
    # End function if message type is a pinned message
    if 'pinned_message' in response:
        return;
    content_type, chat_type, chat_id = telepot.glance(response)
    textMsg = response['text']
    fromstr = ('[GROUP] ' + response['chat']['title']) if ('title' in response['chat']) else ('[PRIVATE] ' + response['chat']['last_name'] + ' ' + response['chat']['first_name'])
    if textMsg == '/start' or textMsg == '/start@testm20bot':  # Edit this with correct bot username
        logprint(fromstr + ' (ID = ' + str(chat_id) + ') started')
        keyboard = {'inline_keyboard': [[{'callback_data': 'games', 'text': 'Games'}, {'callback_data': 'info', 'text': 'Info'}]]}
        bot.sendMessage(chat_id, 'Welcome to virtual Enitio 2020, this bot will be used to communicate instructions with you. Please select your next step!', reply_markup=keyboard)
        # Only pins group chat
        if 'title' in response['chat']:
            bot.pinChatMessage(chat_id, response['message_id']+1, disable_notification=None)
    elif textMsg == '/password' or textMsg == '/password@testm20bot':  # Edit this with correct bot username
        bot.sendMessage(chat_id, 'Please input the password to redeem your points.')
        passwordListen.append(chat_id)
    elif chat_id in passwordListen:
        # Remove all duplicates if exist due to multiple members sending /password
        while chat_id in passwordListen:
            passwordListen.remove(chat_id)
        if textMsg == 'password':
            logprint('>> ' + fromstr + ' (ID = ' + str(chat_id) + ') has succesfully claimed their points.')
            bot.sendMessage(chat_id, text='You have succesfully claimed your points!')
            f = open('claimedscores.txt', 'a+')
            f.write(str(datetime.datetime.now()) + '\t ID = ' + str(chat_id) + '\t' + fromstr + ' (Member: ' + response['from']['last_name'] + ' ' + response['from']['first_name'] + ')\n')
            f.close
        else:
            bot.sendMessage(chat_id, text='Invalid password!')
    elif textMsg.startswith('/'):
        bot.sendMessage(chat_id, text='Invalid command entered!\n\nCommands:\n/start  Shows Enitio Bot\'s GUI\n/password  Enter password for points')

# Received action on inline keyboard buttons   
def on_callback_query(response):
    query_id, from_id, query_data = telepot.glance(response, flavor='callback_query')
    chat_id = response['message']['chat']['id']
    msg_id = response['message']['message_id']
    if query_data == 'back1':
        keyboard = {'inline_keyboard': [[{'callback_data': 'games', 'text': 'Games'}, {'callback_data': 'info', 'text': 'Info'}]]}
    elif query_data == 'games' or query_data == 'back2':
        keyboard = {'inline_keyboard': [[{'callback_data': 'minecraft', 'text': 'Minecraft'}, {'callback_data': 'unity', 'text': 'Unity Game'}],\
                                        [{'callback_data': 'back1', 'text': '« Previous Menu'}]]}
    elif query_data == 'info':
        keyboard = {'inline_keyboard': [[{'callback_data': 'replace', 'text': 'info: TEXT'}],\
                                        [{'callback_data': 'back1', 'text': '« Previous Menu'}]]}
    elif query_data == 'minecraft':
        keyboard = {'inline_keyboard': [[{'callback_data': 'replace', 'text': 'minecraft: TEXT'}],\
                                        [{'callback_data': 'back2', 'text': '« Back to Games'}]]}
    elif query_data == 'unity':
        keyboard = {'inline_keyboard': [[{'callback_data': 'replace', 'text': 'unity: TEXT'}],\
                                        [{'callback_data': 'back2', 'text': '« Back to Games'}]]}
    else:
        keyboard = response['message']['reply_markup']
    # Notification -- bot.answerCallbackQuery(query_id, text='Got it')
    bot.editMessageReplyMarkup((chat_id, msg_id), reply_markup=keyboard)

passwordListen = []
logfilename = 'log_' + datetime.datetime.now().strftime("%y%m%d_%H%M%S") + '.txt'
logprint('ENITIO TELEGRAM BOT 2020  [CTRL + C to kill]  ' + str(datetime.datetime.now()) + '\n  Listening ...\n')
MessageLoop(bot, {'chat': on_chat_message, 'callback_query': on_callback_query}).run_as_thread()

# Runs the function endlessly
while 1:
    time.sleep(10)


## Sample dictionary returned from on_chat_message() ##
## {'chat': {'all_members_are_administrators': True,
##           'id': -452432836,
##           'title': 'Enitio Test Group',
##           'type': 'group'},
##  'date': 1589801203,
##  'entities': [{'length': 9, 'offset': 0, 'type': 'bot_command'}],
##  'from': {'first_name': 'Philip',
##           'id': 966642681,
##           'is_bot': False,
##           'language_code': 'en',
##           'last_name': 'Lee'},
##  'message_id': 576,
##  'text': '/password'}

## Sample dictonary returned from on_callback_query()
## {'chat_instance': '2323170187566962',
##  'data': 'info',
##  'from': {'first_name': 'Philip',
##           'id': 966642681,
##           'is_bot': False,
##           'language_code': 'en',
##           'last_name': 'Lee'},
##  'id': '4151698702819722902',
##  'message': {'chat': {'all_members_are_administrators': True,
##                       'id': -452432836,
##                       'title': 'Enitio Test Group',
##                       'type': 'group'},
##              'date': 1589792815,
##              'from': {'first_name': 'Enitio Test',
##                       'id': 1151311124,
##                       'is_bot': True,
##                       'username': 'testm20bot'},
##              'message_id': 524,
##              'reply_markup': {'inline_keyboard': [[{'callback_data': 'games',
##                                                     'text': 'Games'},
##                                                    {'callback_data': 'info',
##                                                     'text': 'Info'}]]},
##              'text': 'Welcome to virtual Enitio 2020, this bot will be used to '
##                      'communicate instructions with you. Please select your '
##                      'next step!'}}
