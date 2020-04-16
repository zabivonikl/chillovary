from random import randint, uniform
from datetime import datetime
from os import path

import vk_api
from vk_api import VkUpload
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType

from config import Config, logo

from wallet.wallet import Info, WalletCardGenerator
from weather.weather import Weather
from weather.card_generator import WeatherCardGenerator

from picgen.picgen import Quotes
from database.database import Sql

from youtube.youtube_parse import Youtube

from horoscope.horoscope import DataParse

from mafia.mafia import Mafia

from distortion.distortion import Distortion


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

    def universal(self, peer_id, answers):
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=answers[randint(0, len(answers) - 1)]
                               .replace("%u", f'{round(uniform(-1000, 250), 2)}')
                               .replace('%i', f'{randint(0, 250)}')
                               .replace("%d", f'{randint(0, 210)}')
                               .replace('%l', f'{randint(0, 999999)}'))

    def vladcount(self, usr_id, peer_id):
        response = self.api.users.get(user_ids=usr_id)
        usr_name = f"{response[0]['first_name']} {response[0]['last_name']}"
        Sql(usr_id).statistic(peer_id=peer_id,
                              method='vladcount',
                              user_name=usr_name)
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Насчитано {Sql(usr_id).vlad_count(peer_id)} пидорасов')

    def veruchkacontrol(self, peer_id):
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

    def bogdancontrol(self, peer_id):
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

    def garikcontrol(self, usr_id, peer_id):
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

    def sanychcontrol(self, usr_id, peer_id):
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

    def bibametr(self, usr_id, peer_id):
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
        chords = Sql(usr_id).find()
        resp = Weather(day, chords).day_list()
        if resp[9] is None:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Сначала укажите свою геопозицию')
        else:
            WeatherCardGenerator(resp)
            resp = VkUpload(self.session).photo_messages(photos=path.abspath('weather/picgen/card.png'))
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def weather_adding(self, message, peer_id):
        if message['geo'] is not None:
            usr_id = message['from_id']
            chords = (round(message['geo']['coordinates']['latitude'], 2),
                      round(message['geo']['coordinates']['longitude'], 2))
            resp = Sql(usr_id).add(chords)
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message=resp)
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Прикрепите свою геопозицию, чтобы я знал, куда присылать прогноз погоды')

    def wallet(self, peer_id):
        data = Info().list_generator()
        WalletCardGenerator(data)
        resp = VkUpload(self.session).photo_messages(photos=path.abspath('wallet/cardgenerator/card.png'))
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def calculate(self, text, peer_id):
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Ответ: {eval(text)}')

    def quote_repl(self, reply, peer_id):
        self.api.messages.setActivity(type='typing',
                                      peer_id=peer_id)
        quote_logo = logo(peer_id)
        usr_id = [reply['from_id']]
        text = [reply['text']]
        usr_data = self.api.users.get(user_ids=usr_id, fields='photo_max')
        link = [usr_data[0]['photo_max']]
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

    def quote_fwr(self, reply, peer_id):
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
                                      fields='photo_max')
        for i in range(len(usr_data)):
            links.append(usr_data[i]['photo_max'])
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

    def dist(self, peer_id, message):
        if message['attachments'][0]['type'] == 'photo':
            length = len(message['attachments'][0]['photo']['sizes']) - 1
            url = message['attachments'][0]['photo']['sizes'][length]['url']
        else:
            url = self.api.users.get(message['from_id'], fields='photo_max')[0]['photo_max']
        Distortion(url)
        resp = VkUpload(self.session).photo_messages(photos=path.abspath('distortion/picture.jpg'))
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Сжал...',
                               attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

    def youtube(self, usr_id, peer_id):
        url_list = Sql(usr_id).channels_getting()
        template = str(Youtube(url_list).dict_generator()).replace("'", '"')
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Последние видео...',
                               template=template)

    def channels_adding(self, usr_id, peer_id, text):
        url_list = text.replace("https://www.youtube.com/channel/", "").replace(' ', '').split(",")
        Sql(usr_id).channels_adding(url_list)
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message='Каналы успешно добавлены')

    def horoscope(self, peer_id, text):
        self.api.messages.send(peer_id=peer_id,
                               random_id=randint(0, 512),
                               message=f'Гороскоп {text}\n\n{DataParse(text)}')

    def coin(self, peer_id):
        random = randint(0, 100)
        if random in range(0, 49):
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Выпала решка')
        elif random == 100:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Монета упала на ребро')
        else:
            self.api.messages.send(peer_id=peer_id,
                                   random_id=randint(0, 512),
                                   message='Выпал орёл')

    @staticmethod
    def mafia(usr_id, peer_id, text):
        Mafia(text.strip(), peer_id, usr_id)

    def roflan(self, peer_id, text):
        for i in text:
            if i in Config.ROFLAN:
                resp = VkUpload(self.session).photo_messages(photos=path.abspath(f'roflan/{i}.png'))
                self.api.messages.send(peer_id=peer_id,
                                       random_id=randint(0, 512),
                                       attachment=f"photo{resp[0]['owner_id']}_{resp[0]['id']}")

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
                                self.veruchkacontrol(peer_id)
                            if any(i in Config.LENUHA for i in text):
                                self.universal(peer_id, Config.LENUHA_ANS)
                            if any(i in Config.FIZIVHKA for i in text):
                                self.universal(peer_id, Config.FIZIVHKA_ANS)
                            if any(i in Config.BOGDAN for i in text):
                                self.bogdancontrol(peer_id)
                            if any(i in Config.ILYUSHA for i in text):
                                self.universal(peer_id, Config.ILYUSHA_ANS)
                            if any(i in Config.ARVIK for i in text):
                                self.universal(peer_id, Config.ARVIK_ANS)
                        if any(i in Config.SANYCH for i in text):
                            self.sanychcontrol(usr_id, peer_id)
                        if any(i in Config.GARIK for i in text):
                            self.garikcontrol(usr_id, peer_id)
                        if any(i in Config.KATYA for i in text):
                            self.universal(peer_id, Config.katya_ans)
                        if any(i in ['бибаметр'] for i in text):
                            self.bibametr(usr_id, peer_id)
                        if any(i in Config.NWORDS for i in text):
                            self.universal(peer_id, Config.NWORDS_ANS)
                        if any(i in Config.GAYMETR for i in text):
                            self.universal(peer_id, Config.gaymetr_ans)
                        if any(i in Config.HI_TUBE for i in text):
                            self.universal(peer_id, Config.HI_TUBE_ANS)
                        if any(i in Config.SHOCK for i in text):
                            self.universal(peer_id, Config.SHOCK_ANS)
                        if any(i in Config.SIGA for i in text):
                            self.universal(peer_id, Config.SIGA_ANS)
                        if any(i in Config.NANDOMO for i in text):
                            self.universal(peer_id, Config.NANDOMO_ANS)
                        if any(i in Config.MAFIA for i in event.object['message']['text']
                                .replace('[club177983601|@kalianka_flex]', "мафия,")
                                .replace("[club177983601|Чилловары]", "мафия,").lower().split(',')):
                            self.mafia(usr_id, peer_id,
                                       event.object['message']['text']
                                       .replace('[club177983601|@kalianka_flex]', "мафия,")
                                       .replace("[club177983601|Чилловары]", "мафия,").lower().split(',')[1])
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
                        if any(i in ['геопозиция'] for i in text):
                            self.weather_adding(event.object['message'], peer_id)
                        if any(i in Config.WALLET for i in text):
                            self.wallet(peer_id)
                        if any(i in Config.CALCULATE for i in event.object['message']['text'].lower().split(',')):
                            self.calculate(text=event.object['message']['text'].lower().split(',')[1],
                                           peer_id=peer_id)
                        if any(i in Config.DORA for i in text):
                            self.universal(peer_id, Config.dora_ans)
                        if any(i in Config.YOUTUBE for i in text):
                            self.youtube(usr_id, peer_id)
                        if any(i in Config.HOROSCOPE for i in event.object['message']['text'].lower().split(', ')):
                            self.horoscope(peer_id, event.object['message']['text'].lower().split(', ')[1])
                        if any(i in Config.COIN for i in text):
                            self.coin(peer_id)
                        if any(i in 'каналы' for i in event.object['message']['text'].lower().split(';')):
                            self.channels_adding(usr_id, peer_id, event.object['message']['text'].split(';')[1])
                        if any(i in Config.HELP for i in text):
                            self.universal(peer_id, Config.HELP_ANS)
                        if any(i in Config.ROFLAN for i in text):
                            self.roflan(peer_id, text)
                        if any(i in Config.DISTORTION for i in text):
                            self.dist(peer_id, event.object['message'])
                        # у цитат тоже есть несколько вариаций, поэтому требуется прописать 2 проверки для запуска
                        # одной и той же функции
                        if any(i in Config.QUOTE for i in text) and 'reply_message' in event.object['message']:
                            self.quote_repl(event.object['message']['reply_message'], peer_id)
                        elif 'from_id' in event.object['message']['fwd_messages'][0] and\
                                any(i in Config.QUOTE for i in text):
                            self.quote_fwr(event.object['message']['fwd_messages'], peer_id)
            except IndexError:  # игнорируем index errors
                pass
            except Exception as e:  # говорим роботу, чтоб отправлял ошибки в консольный диалог
                self.api.messages.send(peer_id=Config.CONSOLE_ID,
                                       random_id=randint(0, 512),
                                       message=f'♻Бот перезапущен.\nПричина: {e}')


if __name__ == '__main__':
    VK()
