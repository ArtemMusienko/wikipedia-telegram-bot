import telebot, wikipedia, re
from telebot import types


bot = telebot.TeleBot('')

wikipedia.set_lang("ru")

def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext=ny.content[:1000]
        wikimas=wikitext.split('.')
        wikimas = wikimas[:-1]
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not('==' in x):
                    # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if(len((x.strip()))>3):
                   wikitext2=wikitext2+x+'.'
            else:
                break
        return wikitext2
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    # except Exception as e:
    except:
        return 'В энциклопедии нет информации об этом☹️'

@bot.message_handler(commands=["start"])
def start(message):
    sti = open('static/Wikipedia.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ <b>{1.first_name}</b>.\nЕсли будет нужно развернутое определение конкретного термина, то с радостью смогу помочь в этом!😉".format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(commands=["help"])
def faq(message):
    sti = open('static/Wikipedia2.tgs', 'rb')
    bot.send_sticker(message.chat.id, sti)
    bot.send_message(message.chat.id, "Я Telegram бот <b>{1.first_name}🤓</b>.\n<em>Главная функция бота</em> - работа с энциклопедией <b>Wikipedia</b>, выдавая нужное определение конкретного термина.\n\nБот написан на языке программирования <b>Python🐍</b>.\n\nВ скором времени я буду постоянно развиваться и радовать тебя своими новыми функциями. \n\n<em>Последнее обновление 0.1.5 beta:</em> \n\n \t\t\t\t\t\t\t- Добавлено контекстное меню с выбором всех\n \t\t\t\t\t\t\tсуществующих команд;\n \t\t\t\t\t\t\t- Добавлена новая команда \"/help\";\n \t\t\t\t\t\t\t- Изменено описание и фотография бота;\n \t\t\t\t\t\t\t- Оптимизирован код;".format(message.from_user, bot.get_me()),
        parse_mode='html')

@bot.message_handler(content_types=["text"])
def handle_text(message):
    bot.send_message(message.chat.id, getwiki(message.text))

bot.polling(none_stop=True, interval=0)
