import telebot
# import requests
# import json
from config import keys, TOKEN
from extentions import ConvertoinException, CryptoConverter

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Чтобы начать работу введите команду в формате: \n <имя вылюты>  \
    <в какую валюту перевести>\
     <кол-во валюты> \n Список доспупных валют по /values'
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def value(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров')

        quote, base, amount = values
        total_base = CryptoConverter.get_price(quote, base, amount)
    except ConvertoinException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:

    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)

bot.polling(none_stop=True)
# @bot.message_handler(content_types=['text', ])
# def repeat(message: telebot.types.Message):
#     bot.send_message(message.chat.id, "Что ты сказал? Ану, повтори! :-)")
#
# @bot.message_handler(content_types=['photo', ])
# def repeat(message: telebot.types.Message):
#     bot.reply_to(message, f'Nice mem XXD, {message.chat.username}')