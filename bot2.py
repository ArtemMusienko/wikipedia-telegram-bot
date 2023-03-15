# -*- coding: utf-8 -*-
import config
import random
import telebot
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config
from telebot import types

config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('')
mgr = owm.weather_manager()
bot = telebot.TeleBot("")

@bot.message_handler(commands=['start'])
def welcome(message):
    sti = open('static/weather.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti) 

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - <b>{1.first_name}</b>, подсказать с погодой?😍 Не забывай про команду /help. Рад видеть тебя!☺️".format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(commands=['help'])
def dqw(message):
    sti = open('static/help.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
          
    bot.send_message(message.chat.id,"Приветствую! Я Telegram бот по имени <b>Weather for You</b>. Что же я умею?\nЯ смогу рассказать тебе подробно про погоду в любом городе мира!🌦\n\nЕсли ввести любой город мира, то бот сообщит подробную информацию о погоде в нем🌍. Вводить город можно и на русском, и на английском языках. Если ввести город с маленькой буквы, то тоже будет положительный результат. Если города не существует, то тогда будет выдана ошибка об его отсутствие. Данный бот ориентирован только на работу с погодой и не более!🔥\n\n Последнее обновление <em>1.3.3</em>: \n\n \t\t\t\t\t\t\t- Изменено название бота \n \t\t\t\t\t\t\t- Оптимизирован код\n \t\t\t\t\t\t\t- Команда <em>/faq</em> убрана, а команда <em>/help</em> дополнилась большей информацией\n\nЭтот Telegram бот написан на языке программирования <b>\"Python\"❤️</b>".format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(content_types=['text'])
def send_echo(message):
    try: 
     observation = mgr.weather_at_place( message.text )
     w = observation.weather
     temp = w.temperature('celsius')["temp"]
     humidity = w.humidity
     wind = w.wind()["speed"]

     answer = "В городе " + message.text + " сейчас " + w.detailed_status + "\n"
     answer += "Температура сейчас в районе " + str(temp) + " ℃\nУровень влажности: " + str(humidity) + "%\nСкорость ветра: " + str(wind) + " м/c\n\n"

     if temp < 10:
          answer += "Сейчас холодно, одевайся тепло!🥶"         
     elif temp < 20:
          answer += "Сейчас более менее тепло, но все равно что-нибудь накинь сверху❗"
     else:
          answer += "Температура прекрасная, сейчас уж точно не замерзнешь!🥵"  

     bot.send_message(message.chat.id, answer)
    except: 
     bot.send_message(message.chat.id,'Ошибка! 🚫 Город не найден.')

bot.polling( none_stop = True)