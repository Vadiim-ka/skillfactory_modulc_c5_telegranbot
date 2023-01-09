import telebot
from extension import APIException, Convertor
from config import TOKEN, exchanges

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def start(message: telebot.types.Message):
    text = "Добрый день. Чтобы начать работу введите команду боту в следующем формате : <валюта> \
    < в какую валюту перевести > \
    < колличество переводимой валюты  > \
    список доступнвх валют /values"
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in exchanges.keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    try:
        base, quote, amount = message.text.split()
    except ValueError as e:
        bot.reply_to(message, 'Неверное количество параметров!')

    try:
        new_prise = Convertor.get_price(base, quote, amount)
        bot.reply_to(message, f'Цена {amount} {base} в {quote} : {new_prise}')
    except APIException as e:
        bot.reply_to(message, f'Ошибка в команде: \n{e}')


bot.polling()
