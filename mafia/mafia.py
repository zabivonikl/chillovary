from os.path import abspath
from random import randint

import vk_api
import sqlite3

from config import Config


class Mafia:
    def __init__(self, text, peer_id, usr_id):
        self.session = vk_api.VkApi(token=Config.TOKEN, client_secret=Config.TOKEN)
        self.api = self.session.get_api()
        self.peer_id = peer_id
        self.usr_id = usr_id
        resp = self.api.users.get(user_ids=usr_id,
                                  fields='can_write_private_message')
        self.usr_name = f"{resp[0]['first_name']} {resp[0]['last_name']}"
        self.can_write_private_message = resp[0]['can_write_private_message']
        if text == 'начать':
            self.start()
        elif text == 'готов':
            self.player_adding()
        elif text == 'назначить роли':
            self.role()
        elif text == 'ночь':
            self.night()
            self.result()
        elif text == 'день':
            self.day()
            self.result()
        else:
            self.passing()

    def passing(self):
        self.api.messages.send(peer_id=self.peer_id,
                               random_id=randint(0, 512),
                               message='Такой команды нет')

    def start(self):
        games_list = []
        with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
            curs = conn.cursor()
            curs.execute('''select * from sqlite_master where type = "table"''')
            table_list = curs.fetchall()
            for i in range(len(table_list)):
                games_list.append(table_list[i][2])
        if str(self.peer_id) in games_list:
            with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''DROP TABLE [{self.peer_id}]''')
                curs.execute(f'''CREATE TABLE [{self.peer_id}] (user_id INTEGER, role TEXT, killed INTEGER);''')
                curs.execute(f'''UPDATE games SET (peer_id, condition)=("{self.peer_id}", 1)
                                 WHERE peer_id="{self.peer_id}"''')
        else:
            with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''CREATE TABLE [{self.peer_id}]
                                 (user_id INTEGER, user_name TEXT, role TEXT, killed INTEGER);''')
                curs.execute(f'''INSERT INTO games (peer_id, condition) VALUES ("{self.peer_id}, 1")''')
        keyboard = {'inline': True,
                    "buttons": [
                        [{
                            "action": {
                                "type": "text",
                                "label": "Готов"
                            },
                            "color": "positive"
                        }]]}
        self.api.messages.send(peer_id=self.peer_id,
                               random_id=randint(0, 512),
                               message='Игра создана\n\nДля адекватной работы бота требуется начать диалог с беседой\n'
                                       'https://vk.com/im?sel=-177983601',
                               keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))

    def player_adding(self):
        if int(self.can_write_private_message) == 1:
            with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''SELECT user_id FROM [{self.peer_id}]''')
                players = curs.fetchall()
                players_list = []
                for i in range(len(players)):
                    players_list.append(players[i][0])
                if self.usr_id in players_list:
                    self.api.messages.send(peer_id=self.peer_id,
                                           random_id=randint(0, 512),
                                           message=f'*id{self.usr_id} ({self.usr_name}), вы уже учавствуете')
                else:
                    curs.execute(f'''INSERT INTO [{self.peer_id}] (user_id, role, killed) VALUES
                                     ("{self.usr_id}", "City_Zen", "0")''')
                    keyboard = {'inline': True,
                                "buttons": [
                                    [{
                                        "action": {
                                            "type": "text",
                                            "label": "Все здесь"
                                        },
                                        "color": "positive"
                                    }]]}
                    self.api.messages.send(peer_id=self.peer_id,
                                           random_id=randint(0, 512),
                                           message=f'*id{self.usr_id} ({self.usr_name}) играет!',
                                           keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
        else:
            self.api.messages.send(peer_id=self.peer_id,
                                   random_id=randint(0, 512),
                                   message='Сначала создайте диалог с ботом\nhttps://vk.com/im?sel=-177983601')

    def role(self):
        with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT user_id FROM [{self.peer_id}]''')
            players = curs.fetchall()
        if len(players) < 5:
            keyboard = {'inline': True,
                        "buttons": [
                            [{
                                "action": {
                                    "type": "text",
                                    "label": "Готов"
                                },
                                "color": "positive"
                            }]]}
            self.api.messages.send(peer_id=self.peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Недостаточно игроков, нажмите готов, чтоб присоединиться\n\n'
                                           f'Игроков: {len(players)}/5',
                                   keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
        else:
            with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
                curs = conn.cursor()
                mafia_list = []
                while len(mafia_list) < 2:
                    mafia = players[randint(0, len(players))][0]
                    curs.execute(f'''UPDATE [{self.peer_id}] SET role="Mafia" WHERE user_id="{mafia}"''')
                    curs.execute(f'''SELECT user_id FROM [{self.peer_id}] WHERE role="Mafia"''')
                    mafia_list.append(curs.fetchall()[len(mafia_list)])
                for i in range(len(mafia_list)):
                    self.api.messages.send(peer_id=mafia_list[i][0],
                                           random_id=randint(0, 512),
                                           message=f'Вы мафия')
                curs.execute(f'''SELECT user_id FROM [{self.peer_id}] WHERE role="City_Zen"''')
                players = curs.fetchall()
                doctor = players[randint(0, len(players) - 1)][0]
                curs.execute(f'''UPDATE [{self.peer_id}] SET role="Doctor" WHERE user_id="{doctor}"''')
                self.api.messages.send(peer_id=doctor,
                                       random_id=randint(0, 512),
                                       message='Вы доктор')
                curs.execute(f'''SELECT user_id FROM [{self.peer_id}] WHERE role="City_Zen"''')
                players = curs.fetchall()
                for i in range(len(players)):
                    self.api.messages.send(peer_id=players[i][0],
                                           random_id=randint(0, 512),
                                           message=f'Вы мирный житель')
                keyboard = {'inline': True,
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "Ночь"
                                    },
                                    "color": "positive"
                                }]]}
                self.api.messages.send(peer_id=self.peer_id,
                                       random_id=randint(0, 512),
                                       message='Роли назначены',
                                       keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
                curs.execute(f'''UPDATE games SET condition="2" WHERE peer_id="{self.peer_id}"''')

    def night(self):
        with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT condition FROM games WHERE peer_id="{self.peer_id}"''')
            condition = curs.fetchall()
            if condition[0][0] % 2 == 0:
                keyboard = {'inline': True,
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "День"
                                    },
                                    "color": "positive"
                                }]]}
                self.api.messages.send(peer_id=self.peer_id,
                                       random_id=randint(0, 512),
                                       message='Ночь окончена',
                                       keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))
            else:
                keyboard = {'inline': True,
                            "buttons": [
                                [{
                                    "action": {
                                        "type": "text",
                                        "label": "День"
                                    },
                                    "color": "positive"
                                }]]}
                self.api.messages.send(peer_id=self.peer_id,
                                       random_id=randint(0, 512),
                                       message='Ночь недоступна',
                                       keyboard=str(keyboard).replace("'", '"').replace('True', 'true'))

    def day(self):
        pass

    def result(self):
        with sqlite3.connect(abspath('mafia/mafia_db.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT user_id FROM [{self.peer_id}] WHERE role!="Mafia"''')
            players = curs.fetchall()
            curs.execute(f'''SELECT user_id FROM [{self.peer_id}] WHERE "role=Mafia"''')
            mafia = curs.fetchall()
        resp = self.api.users.get(user_ids=mafia[0][0])
        mafia_names = f"*id{mafia[0][0]}({resp[0]['first_name']} {resp[0]['last_name']})"
        for i in range(1, len(mafia)):
            resp = self.api.users.get(user_ids=mafia[i][0])
            mafia_names += f", *id{mafia[i][0]}({resp[0]['first_name']} {resp[0]['last_name']})"
        if len(players) == 0:
            self.api.messages.send(peer_id=self.peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Победила мафия.\n\nМафия: {mafia_names}')
        elif len(mafia) == 0:
            self.api.messages.send(peer_id=self.peer_id,
                                   random_id=randint(0, 512),
                                   message=f'Мафия проиграла.\n\nМафия: {mafia_names}')
        else:
            pass
