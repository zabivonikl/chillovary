from os import path
from datetime import datetime
from random import randint

from transliterate import translit
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
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''SELECT OW_ID FROM VK WHERE VK_ID="{self.usr_id}"''')
            ow_id = str(curs.fetchone()[0])
        return ow_id

    # смена id города у пользователя
    def add(self, city):
        try:
            # открываем БД
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()

                # вытаскиваем id города
                curs.execute(F'''SELECT OW_ID FROM Cities WHERE CityName_RU="{city}"''')
                usr_city = curs.fetchone()[0]

                # запизиваем id города в пару к VK id
                curs.execute(f'''INSERT INTO VK ('VK_ID', 'OW_ID') VALUES ("{self.usr_id}", "{usr_city}")''')
        except Exception as e:
            return f'Неудачная попытка\nПричина: {e}\n\nВероятно, вашего города нет в списке.'
        return f'ID вашего города: {usr_city}'

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
                curs.execute(f'''SELECT {method} FROM Statistic WHERE (peer_id, usr_id) = ("{peer_id}", "{self.usr_id}")''')
                count = curs.fetchone()[0] + 1

                # запихуеваем новое значение в таблицу
                curs.execute(f'''UPDATE Statistic SET ({method}, user_name) = ("{count}", "{user_name}") WHERE (peer_id, usr_id) = ("{peer_id}", "{self.usr_id}")''')
        else:
            # если значения в таблице нет, то создаём новую строку
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''INSERT INTO Statistic (usr_id, peer_id, {method}, user_name) VALUES ("{self.usr_id}", "{peer_id}", "{1}", "{user_name}")''')

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
                    curs.execute(f'''UPDATE daily_random SET (randomint, time)=("{random}", "{time}") WHERE peer_id="{peer_id}"''')
                    return random
        else:

            # добавляем диалог в БД
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''INSERT INTO daily_random (peer_id, randomint) VALUES ("{peer_id}", "{randint(2, 6)}")''')

    # статистика
    def peer_ids(self):
        # достаём все значения из таблицы
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute('''SELECT * FROM Statistic''')
            data = curs.fetchall()

        # обнуляем переменные
        vladcount = 0
        veruchkacontrol = 0
        lenuhacontrol = 0
        fizichkacontrol = 0
        bogdancontrol = 0
        sanychcontrol = 0
        jestyanka = 0
        hi_tube = 0
        shock = 0
        gaymetr = 0
        bibametr = 0
        weather = 0
        weather_adding = 0
        wallet = 0
        calculate = 0
        help = 0
        quote = 0
        dora = 0
        ilyushacontrol = 0
        garikcontrol = 0
        youtube = 0

        # высчитываем сумму вызовов каждого метода
        for i in range(len(data)):
            vladcount += data[i][3]
            veruchkacontrol += data[i][4]
            lenuhacontrol += data[i][5]
            fizichkacontrol += data[i][6]
            bogdancontrol += data[i][7]
            sanychcontrol += data[i][8]
            jestyanka += data[i][9]
            hi_tube += data[i][10]
            gaymetr += data[i][11]
            bibametr += data[i][12]
            weather += data[i][13]
            weather_adding += data[i][14]
            wallet += data[i][15]
            calculate += data[i][16]
            help += data[i][17]
            quote += data[i][18]
            dora += data[i][19]
            shock += data[i][20]
            ilyushacontrol += data[i][21]
            garikcontrol += data[i][22]
            youtube += data[i][23]

        # генерируем и возвращаем текст
        text = f'Пидорсчёт: {vladcount}\n'
        text += f'Веручек: {veruchkacontrol}\n'
        text += f'Ленух: {lenuhacontrol}\n'
        text += f'Физичек: {fizichkacontrol}\n'
        text += f'Богданов: {bogdancontrol}\n'
        text += f'Санычей: {sanychcontrol}\n'
        text += f'Илюш: {ilyushacontrol}\n'
        text += f'Оскорблений: {jestyanka}\n'
        text += f'Гариков: {garikcontrol}\n'
        text += f'Привет, Тюбов: {hi_tube}\n'
        text += f'Ээ: {shock}\n'
        text += f'Гейметров: {gaymetr}\n'
        text += f'Бибаметров: {bibametr}\n'
        text += f'Дор: {dora}\n'
        text += f'Ютаров: {youtube}\n'
        text += f'Запросов погод: {weather}\n'
        text += f'Смен города: {weather_adding}\n'
        text += f'Запросов курсов валют: {wallet}\n'
        text += f'Калькуляторов: {calculate}\n'
        text += f'Вызовов справки: {help}\n'
        text += f'Цитат: {quote}\n'
        return text

    # позволяет добавлять рускоязычное название города в таблицу
    def add_city(self, city_en, city_ru):
        with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
            curs = conn.cursor()
            curs.execute(f'''UPDATE Cities SET CityName_RU="{city_ru}" WHERE CityName_EN="{city_en}"''')

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
            with sqlite3.connect(path.abspath(self.way + 'CityAndVk.db')) as conn:
                curs = conn.cursor()
                curs.execute(f'''SELECT * FROM youtube WHERE usr_id = "{self.usr_id}"''')
                channels = curs.fetchall()[0]
                for i in range(1, len(channels)):
                    if channels[i] is not None:
                        channel_list.append(channels[i])
            return channel_list


if __name__ == '__main__':
    Sql(0).conversation_members(2000000005, 0)
