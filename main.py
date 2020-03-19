from random import randint, uniform  # используется в dora
from datetime import datetime
from os import path

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import Config, YTConfig, logo

from weather.wallet import Wallets
from weather.weather import Weather
from weather.card_generator import CardGenerator

from picgen.picgen import Quotes
from database.database import Sql

from youtube.youtube_parse import Youtube


class VK:
    """
    Основной класс бота
    Обрабатывает сообщения, запускает требующиеся классы и функции для обработки команд и отсылает ответы
    """
    def __init__(self):
        self.session = vk_api.VkApi(token=Config.TOKEN, client_secret=Config.TOKEN)  # логинимся как группа по токену
        # получаем возможность вызывать методы не используя функцию self.session.method
        self.api = self.session.get_api()
        self.main()  # запуск основного цикла

    def vladcount(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'vladcount')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Насчитано {Sql(usr_id).vlad_count(peer_id)} пидорасов')

    def veruchkacontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'veruchkacontrol')
        random = randint(0, len(Config.VERA_ANS) - 1)
        if random == 2:
            resp = VkUpload(self.session).photo_messages(photos=path.abspath('media/photos/parvin.jpg'))
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=Config.VERA_ANS[random])

    def lenuhacontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'lenuhacontrol')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.LENUHA_ANS[randint(0, len(Config.LENUHA_ANS) - 1)])

    def fizichkacontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'fizichkacontrol')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.FIZIVHKA_ANS[randint(0, len(Config.FIZIVHKA_ANS) - 1)])

    def bogdancontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'bogdancontrol')
        ans = randint(0, len(Config.BOGDAN_ANS) - 1)
        if ans == 1:
            resp = VkUpload(self.session).photo_messages(photos=path.abspath('media/photos/jungle.jpg'))
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=Config.BOGDAN_ANS[ans])

    def ilyushacontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'ilyushacontrol')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.ILYUSHA_ANS[randint(0, len(Config.ILYUSHA_ANS) - 1)])

    def garikcontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'garikcontrol')
        response = self.api.users.get(user_ids=usr_id)
        usr_name = f"@id{usr_id} ({response[0]['first_name']} {response[0]['last_name']})"
        if randint(0, 1) == 1:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Сегодня {usr_name} неудачник! Он поймал гарик')
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Сегодня {usr_name} счастливчик! Он не поймал гарик')

    def jestyanka(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'jestyanka')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.NWORDS_ANS[randint(0, len(Config.NWORDS_ANS) - 1)])

    def arvikcontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'arvikcontrol')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.ARVIK_ANS[randint(0, len(Config.ARVIK_ANS) - 1)])

    def hi_tube(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'hi_tube')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.HI_TUBE_ANS[randint(0, len(Config.HI_TUBE_ANS) - 1)])

    def shock(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'shock')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.SHOCK_ANS[randint(0, len(Config.SHOCK_ANS) - 1)])

    def sanychcontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'sanychcontrol')
        random = randint(0, len(Config.SANYCH_ANS) - 1)
        if random == 2:
            members = Sql(usr_id).conversation_count(peer_id)
            r = Sql(usr_id).daily_random(peer_id)
            duty = int(datetime.now().strftime("%d"))
            while duty > members - 1:
                duty /= int(r)
            member = Sql(usr_id).conversation_members(peer_id, duty)
            usr_name = f"@id{member[1]}({member[0]})"
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'{Config.SANYCH_ANS[random]} {usr_name}')
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=Config.SANYCH_ANS[random])

    def kkcontrol(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'kkcontrol')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Ваш рост {randint(145, 220)} см')

    def gaymetr(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'gaymetr')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Вы гей на {randint(0, 250)} владов из 250')

    def bibametr(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'bibametr')
        response = self.api.users.get(user_ids=usr_id,
                                      fields='sex')
        sex = int(response[0]['sex'])
        values = ['см', 'мм', 'м', 'нм']
        if sex == 2:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Ваша длина хуя {randint(0, 30)} {values[randint(0, 3)]}')
        elif sex == 1:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Ваша глубина пизды {randint(0, 30)} {values[randint(0, 3)]}')
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Сначала скажи что у тебя мерять, TRANSJENDA (укажите в вк пол)')

    def weather(self, usr_id, peer_id, day=0):
        city_id = Sql(usr_id).find()
        resp = Weather(day, city_id).day_list()
        if len(resp) < 10:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Сначала укажите город\n\nДобавь, <название города>')
        else:
            CardGenerator(resp)
            self.statistic(peer_id, usr_id, 'weather')
            resp = VkUpload(self.session).photo_messages(photos=path.abspath('weather/picgen/card.png'))
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def weather_adding(self, usr_id, message, peer_id):
        self.statistic(peer_id, usr_id, 'weather_adding')
        usr_id = message['from_id']
        city = message['text'].split(',')[1].replace(' ', '').capitalize()
        resp = Sql(usr_id).add(city)
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=resp)

    def wallet(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'wallet')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Wallets().main())

    def calculate(self, usr_id, text, peer_id):
        self.statistic(peer_id, usr_id, 'calculate')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Ответ: {eval(text)}')

    def dora(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'dora')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Ваш IQ: {round(uniform(-10, 6) ** 3, 2)}')

    def help(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'help')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=Config.HELP_ANS)

    def quote_repl(self, usr_id, reply, peer_id):
        self.statistic(peer_id, usr_id, 'quote')
        self.api.messages.setActivity(type='typing',
                                      peer_id=peer_id)
        quote_logo = logo(peer_id)
        usr_id = [reply['from_id']]
        text = [reply['text']]
        usr_data = self.api.users.get(user_ids=usr_id, fields='photo_200')
        link = [usr_data[0]['photo_200']]
        usr_name = [f"{usr_data[0]['first_name']} {usr_data[0]['last_name']}"]
        Quotes(authors=usr_name,
               text=text,
               links=link,
               logo=quote_logo)
        resp = VkUpload(self.session).photo_messages(photos=path.abspath('picgen/templates/quote.png'))
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Цитатка...',
                               attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def quote_fwr(self, usr_id, reply, peer_id):
        self.statistic(peer_id, usr_id, 'quote')
        self.api.messages.setActivity(type='typing',
                                      peer_id=peer_id)
        quote_logo = logo(peer_id)
        ids = []
        for i in range(len(reply)):
            ids.append(reply[i]['from_id'])
        ids = set(ids)
        ids = list(ids)
        links = []
        users = []
        text = []
        usr_data = self.api.users.get(user_ids=str(ids)[1:-1].replace(" ", ""),
                                      fields='photo_200')
        for i in range(len(usr_data)):
            links.append(usr_data[i]['photo_200'])
            author = f"{usr_data[i]['first_name']} {usr_data[i]['last_name']}"
            users.append(author)
        for i in range(len(reply)):
            text.append(reply[i]['text'])

        Quotes(authors=users,
               text=text,
               links=links,
               logo=quote_logo)
        resp = VkUpload(self.session).photo_messages(photos=path.abspath('picgen/templates/quote.png'))
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Цитатка...',
                               attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def statistic(self, peer_id, usr_id, method):
        response = self.api.users.get(user_ids=usr_id)
        usr_name = f"{response[0]['first_name']} {response[0]['last_name']}"
        Sql(usr_id).statistic(peer_id=peer_id,
                              method=method,
                              user_name=usr_name)

    def stat_return(self, usr_id):
        resp = "ℹСтатистика бота\n\n"
        resp += Sql(usr_id).peer_ids()
        self.api.messages.send(peer_id=Config.CONSOLE_ID,
                               random_id=randint(0, 512),
                               message=resp)

    def youtube(self, usr_id, peer_id):
        self.statistic(peer_id, usr_id, 'youtube')
        url_list = Sql(usr_id).channels_getting()
        template = str(Youtube(url_list).dict_generator()).replace("'", '"')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Последние видео...',
                               template=template)

    def channels_adding(self, usr_id, peer_id, text):
        self.statistic(peer_id, usr_id, 'channel_adding')
        url_list = text.replace("https://www.youtube.com/channel/", "").replace(' ', '').split(",")
        Sql(usr_id).channels_adding(url_list)
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Каналы успешно добавлены')

    def main(self):
        self.api.messages.send(peer_id=Config.CONSOLE_ID,   # сообщаем о запуске бота в консоль
                               random_id=randint(0, 512),
                               message=f'✅Бот запущен.\n ')
        while True:    # запускаем основной цикл
            try:    # задаём кастомную обработку исключений
                for event in VkBotLongPoll(self.session, Config.GROUP_ID).listen():  # слушаем сервер
                    # вытаскиваем peer_id и присваеваем его к переменной
                    peer_id = event.object['message']['peer_id']
                    # тоже самое, что и с peer_id
                    usr_id = event.object['message']['from_id']
                    # создаём массив из сообщения для распознования слов
                    text = event.object['message']['text'].lower().split(' ')
                    # прописываем триггер на новые сообщения
                    if event.type == VkBotEventType.MESSAGE_NEW:
                        # проверяем peer_id на наличие в конфиге
                        # если хотя бы один элемент из конфига соответствует какому-нибудь элементу текста
                        if peer_id in Config.LOCAL_ROFL:
                            if any(i in Config.VLAD for i in text):
                                self.vladcount(usr_id, peer_id)
                            if any(i in Config.VERA for i in text):
                                self.veruchkacontrol(usr_id, peer_id)
                            if any(i in Config.LENUHA for i in text):
                                self.lenuhacontrol(usr_id, peer_id)
                            if any(i in Config.FIZIVHKA for i in text):
                                self.fizichkacontrol(usr_id, peer_id)
                            if any(i in Config.BOGDAN for i in text):
                                self.bogdancontrol(usr_id, peer_id)
                            if any(i in Config.ILYUSHA for i in text):
                                self.ilyushacontrol(usr_id, peer_id)
                            if any(i in Config.ARVIK for i in text):
                                self.arvikcontrol(usr_id, peer_id)
                        if peer_id == Config.CONSOLE_ID:
                            if any(i in ['статистика'] for i in text):
                                self.stat_return(usr_id)
                        if any(i in Config.SANYCH for i in text):
                            self.sanychcontrol(usr_id, peer_id)
                        if any(i in Config.GARIK for i in text):
                            self.garikcontrol(usr_id, peer_id)
                        if any(i in Config.KATYA for i in text):
                            self.kkcontrol(usr_id, peer_id)
                        if any(i in ['бибаметр'] for i in text):
                            self.bibametr(usr_id, peer_id)
                        if any(i in Config.NWORDS for i in text):
                            self.jestyanka(usr_id, peer_id)
                        if any(i in ['гейметр'] for i in text):
                            self.gaymetr(usr_id, peer_id)
                        if any(i in Config.HI_TUBE for i in text):
                            self.hi_tube(usr_id, peer_id)
                        if any(i in Config.SHOCK for i in text):
                            self.shock(usr_id, peer_id)
                        # у погоды множество вариаций синтаксиса, поэтому требуется смотреть тип элемента и
                        # отталкиваться от его типа
                        if event.object['message']['text'].lower() in Config.WEATHER:
                            self.weather(usr_id, peer_id, 0)
                        if any(i in Config.WEATHER for i in event.object['message']['text'].lower().split(', ')) and\
                                str(event.object['message']['text'].lower().split(', ')[1]).isdigit():
                            day = event.object['message']['text'].lower().split(', ')
                            day = int(day[1])
                            self.weather(usr_id, peer_id, day)
                        elif any(i in Config.WEATHER for i in event.object['message']['text'].lower().split(', ')):
                            if event.object['message']['text'].lower().split(', ')[1] == 'завтра':
                                day = 8
                                self.weather(usr_id, peer_id, day)
                            elif event.object['message']['text'].lower().split(', ')[1] == 'послезавтра':
                                day = 16
                                self.weather(usr_id, peer_id, day)
                        if any(i in ['добавь'] for i in event.object['message']['text'].lower().split(',')):
                            self.weather_adding(usr_id, event.object['message'], peer_id)
                        if any(i in Config.WALLET for i in text):
                            self.wallet(usr_id, peer_id)
                        if any(i in Config.CALCULATE for i in event.object['message']['text'].lower().split(',')):
                            self.calculate(usr_id=usr_id,
                                           text=event.object['message']['text'].lower().split(',')[1],
                                           peer_id=peer_id)
                        if any(i in Config.DORA for i in text):
                            self.dora(usr_id, peer_id)
                        if any(i in Config.YOUTUBE for i in text):
                            self.youtube(usr_id, peer_id)
                        if any(i in 'каналы' for i in event.object['message']['text'].lower().split(';')):
                            self.channels_adding(usr_id, peer_id, event.object['message']['text'].split(';')[1])
                        if any(i in Config.HELP for i in text):
                            self.help(usr_id=usr_id, peer_id=peer_id)
                        # у цитат тоже есть несколько вариаций, поэтому требуется прописать 2 проверки для запуска
                        # одной и той же функции
                        if any(i in Config.QUOTE for i in text) and 'reply_message' in event.object['message']:
                            self.quote_repl(usr_id, event.object['message']['reply_message'], peer_id)
                        elif 'from_id' in event.object['message']['fwd_messages'][0] and\
                                any(i in Config.QUOTE for i in text):
                            self.quote_fwr(usr_id, event.object['message']['fwd_messages'], peer_id)
            except IndexError:  # игнорируем index errors
                pass
            except Exception as e:  # говорим роботу, чтоб отправлял ошибки в консольный диалог
                self.api.messages.send(peer_id=Config.CONSOLE_ID,
                                       random_id=randint(0, 512),
                                       message=f'♻Бот перезапущен.\nПричина: {e}')


if __name__ == '__main__':
    VK()
