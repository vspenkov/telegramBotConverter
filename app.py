import telebot
import datetime
import requests
import json
from config import TOKEN, keys
from osnov import Convertor, ConverterException, d, DT

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands= ["start","help"]) #приветсвенное сообщение
def help(message: telebot.types.Message):
    text = "Чтобы провести конвертацию валюты Вам необходимо ввести данные в следующем порядке:\n <имя валюты> \
<в какую валюту конвертировать>  <сумма перевода>     \
\n Для того, чтобы узнать список валют введите команду: /values"

    bot.reply_to(message, text)

@bot.message_handler(commands= ["values"])  #вывод всех доступных валют
def values(message: telebot.types.Message):
    text = "Доступные валюты:"
    for key in keys.keys():
        text = "\n".join((text, key, ))
    bot.reply_to(message, text)



@bot.message_handler(content_types = ["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        values = list(map(str.lower, values))
        quote, base, amount = values
        total = Convertor.get_price(values)
    except ConverterException as e:
        bot.reply_to(message, f"Ошибка пользователя.\n{e}")

    except Exception as e:
        bot.reply_to(message, f"Не удалось обработать команду\n{e}")
    else:
        text = f"Цена {amount} {quote} в {base} на {DT} составляет - {total} {keys[base]}"
        bot.send_message(message.chat.id, text)



bot.polling()