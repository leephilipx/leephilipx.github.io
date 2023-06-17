# telepot for Bot API
# pprint for readable display of dict
import telepot
from pprint import pprint
import time

# Initialise bot object
token = '1151311124:AAFvyXTM2aZqCKf0pyHqVkCuLIY_v53KN3k'
bot = telepot.Bot(token)

## Sample dictionary returned from bot.getUpdates() ##
## {'message': {'chat': {'first_name': 'Philip',
##                       'id': 966642681,
##                       'last_name': 'Lee',
##                       'type': 'private'},
##              'date': 1589778918,
##              'from': {'first_name': 'Philip',
##                       'id': 966642681,
##                       'is_bot': False,
##                       'language_code': 'en',
##                       'last_name': 'Lee'},
##              'message_id': 104,
##              'text': '/kill'},
##  'update_id': 420914819}

response = bot.getUpdates()[-1]
prevID = response['update_id']

print('>> Service initialised!')

while 1:
    time.sleep(2)
    response = bot.getUpdates(offset=prevID)[-1]
    textMsg = response['message']['text']
    chatID = response['message']['chat']['id']
    if textMsg == '/start' or textMsg == '/start@testm20bot':
        bot.sendMessage(chatID, 'I\'m a parrot bot')
        print('>> Service running!')
        prevID = response['update_id']
        while 1:
            time.sleep(0.5)
            response = bot.getUpdates(offset=prevID)[-1]
            textMsg = response['message']['text']
            chatID = response['message']['chat']['id']
            if response['update_id'] > prevID:
                prevID = response['update_id']
                if textMsg == '/start' or textMsg == '/start@testm20bot':
                    bot.sendMessage(chatID, 'I\'m already alive lol')
                elif textMsg == '/kill' or textMsg == '/kill@testm20bot':
                    bot.sendMessage(chatID, 'I\'m ded')
                    print('>> Service halted!')
                    break
                elif textMsg == '/end' or textMsg == '/end@testm20bot':
                    bot.sendMessage(chatID, '<< Improper usage of /end command >>')
                elif textMsg.startswith('/'):
                    bot.sendMessage(chatID, '<< Unknown command entered >>')
                else:
                    bot.sendMessage(chatID, textMsg)
                    print('Returned "' + textMsg + '" to ID = ' + str(chatID))
    elif textMsg == '/end' or textMsg == '/end@testm20bot':
        bot.sendMessage(chatID, 'I\'m permanently ded')
        print('>> Service terminated! Please re-run')
        break


### Logic when msg is received
##def handle(response):
##    global runLogic
##    textMsg = response['text']
##    chatID = response['chat']['id']
##    if runLogic:
##        if textMsg == '/start' or textMsg == '/start@testm20bot':
##            bot.sendMessage(chatID, 'I\'m already alive lol')
##        elif textMsg == '/kill' or textMsg == '/kill@testm20bot':
##            bot.sendMessage(chatID, 'I\'m ded')
##            print('>> Service halted!')
##            runLogic = 0;
##        elif textMsg == '/end' or textMsg == '/end@testm20bot':
##            bot.sendMessage(chatID, '<< Improper usage of /end command >>')
##        elif textMsg.startswith('/'):
##            bot.sendMessage(chatID, '<< Unknown command entered >>')
##        else:
##            bot.sendMessage(chatID, textMsg)
##            print('Returned "' + textMsg + '" to ID = ' + str(chatID))
##    elif textMsg == '/start' or textMsg == '/start@testm20bot':
##        bot.sendMessage(chatID, 'I\'m a parrot bot')
##        print('>> Service running!')
##        runLogic = 1;
##    elif textMsg == '/end' or textMsg == '/end@testm20bot':
##        bot.sendMessage(chatID, 'I\'m permanently ded')
##        print('>> Service terminated! Please re-run')
##        sys.exit()
##
### Run these commands once
##runLogic = 0
##MessageLoop(bot, handle).run_as_thread()
