from os import path
from datetime import datetime
from random import randint

import sqlite3


class Sql:
    # кусок адреса для открываемых файлов и объявление константы
    def __init__(self, usr_id):
        self.usr_id = usr_id
        if __name__ == '__main__':
            self.way = ''
        else:
            self.way = 'database/'

    # поиск id города в БД по VK ID
    def find(self):
        try:
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''SELECT lat, lon FROM VK WHERE VK_ID="{self.usr_id}"''')
                return curs.fetchone()
        except Exception as e:
            return f'Вероятно, вас ещё нет в БД. Укажите свой город.\n\nОшибка: {e}'

    # смена id города у пользователя
    def add(self, chords):
        try:
            # открываем БД
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()

                # запизиваем координаты в пару к VK id
                curs.execute(f'''INSERT INTO VK ('VK_ID', 'lat', 'lon') VALUES ("{self.usr_id}",
                                                                                "{chords[0]}", "{chords[1]}")''')
        except Exception as e:
            return f'Вероятно, Антон мудак.\n\nКод ошибки: {e}'
        return f'Координаты успешно добавлены! Напишите "Погода"'

    def statistic(self, peer_id, method, user_name):
        # смотрим, есть ли пользователь в таблице
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT usr_id FROM Statistic WHERE peer_id="{peer_id}"''')
            users = curs.fetchall()
        user_list = []
        for i in range(len(users)):
            user_list.extend(users[i])
        if self.usr_id in user_list:
            # открываем БД
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()

                # достаём предыдущее значение и прибавляем 1
                curs.execute(f'''SELECT {method} FROM Statistic
                                 WHERE (peer_id, usr_id) = ("{peer_id}", "{self.usr_id}")''')
                count = curs.fetchone()[0] + 1

                # запихуеваем новое значение в таблицу
                curs.execute(f'''UPDATE Statistic SET ({method}, user_name) = ("{count}", "{user_name}")
                                 WHERE (peer_id, usr_id) = ("{peer_id}", "{self.usr_id}")''')
        else:
            # если значения в таблице нет, то создаём новую строку
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''INSERT INTO Statistic (usr_id, peer_id, {method}, user_name) VALUES
                                 ("{self.usr_id}", "{peer_id}", "{1}", "{user_name}")''')

    # сегодня дежурит...
    def conversation_members(self, peer_id, duty):
        names = []
        # открываем БД
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT user_name, usr_id FROM Statistic WHERE peer_id="{peer_id}"''')
            users_list = curs.fetchall()
            names.extend(users_list[int(duty)])
        return names

    def conversation_count(self, peer_id):
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT usr_id FROM Statistic WHERE peer_id="{peer_id}"''')
            users = curs.fetchall()
        count_of_users = len(users)
        return count_of_users

    # ежедневный рандом
    def daily_random(self, peer_id):
        # объявляем константы
        now = datetime.now()
        peer_list = []
        time = int(now.strftime("%d%H"))

        # проверяем наличие диалога в БД
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT peer_id FROM daily_random''')
            peers = curs.fetchall()
        for i in range(len(peers)):
            peer_list.extend(peers[i])
        if peer_id in peer_list:

            # считываем время и ищем разность с текущим
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''SELECT time FROM daily_random WHERE peer_id="{peer_id}"''')
                time_int = curs.fetchone()[0]
            delta = time - time_int

            # возвращаем число
            if delta < 24:
                with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                    curs = conn.cursor()
                    curs.execute(f'''SELECT randomint FROM daily_random WHERE peer_id="{peer_id}"''')
                    return int(curs.fetchone()[0])
            else:
                # обновляем число
                random = randint(2, 6)
                with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                    curs = conn.cursor()
                    curs.execute(f'''UPDATE daily_random SET (randomint, time)=("{random}", "{time}")
                                     WHERE peer_id="{peer_id}"''')
                    return random
        else:

            # добавляем диалог в БД
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''INSERT INTO daily_random (peer_id, randomint) VALUES
                                 ("{peer_id}", "{randint(2, 6)}")''')

    def vlad_count(self, peer_id):
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT vladcount FROM Statistic WHERE peer_id="{peer_id}"''')
            vlads = curs.fetchall()
            s = 0
            for i in range(len(vlads)):
                s += vlads[i][0]
            return s

    def channels_adding(self, channels):
        for i in range(len(channels)):
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''UPDATE youtube SET channel{i + 1}="{channels[i]}" WHERE usr_id="{self.usr_id}"''')

    def channels_getting(self):
        channel_list = []
        id_list = []
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT usr_id FROM youtube''')
            peers = curs.fetchall()
        for i in range(len(peers)):
            id_list.extend(peers[i])
        if self.usr_id in id_list:
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''SELECT * FROM youtube WHERE usr_id = "{self.usr_id}"''')
                channels = curs.fetchall()[0]
                for i in range(1, len(channels)):
                    if channels[i] is not None:
                        channel_list.append(channels[i])
            return channel_list
        else:
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''INSERT INTO youtube (usr_id) VALUES ("{self.usr_id}")''')
                curs.execute(f'''SELECT * FROM youtube WHERE usr_id = "{self.usr_id}"''')
                channels = curs.fetchall()[0]
                for i in range(1, len(channels)):
                    if channels[i] is not None:
                        channel_list.append(channels[i])
            return channel_list
