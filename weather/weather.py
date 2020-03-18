from os import path
import requests
import json

from config import Config




class Weather:
    # запускаем загрузчик и объявляем день
    def __init__(self, d, city_id="569223"):
        if __name__ == '__main__':
            self.path = ''
        else:
            self.path = 'weather/'
        self.saver(city_id)
        self.day = int(d)

    def saver(self, id):
        # скачиваем прогноз погоды в json и сохраняем на диск
        url = f"http://api.openweathermap.org/data/2.5/forecast?id={id}&APPID={Config.TOKEN2}&lang=ru"
        try:
            weather = requests.get(url).text.encode('utf-8').decode('utf-8')
            with open(path.abspath(self.path + "data/weather_temp.json"), "w") as f:
                f.write(f"{weather}")
        except Exception as e:
            print(f"ошибОЧКА: {e}")

    # открываем JSON и возвращем его содержимое
    def data(self):
        try:
            with open(path.abspath(self.path + "data/weather_temp.json"), encoding="utf-8") as f:
                data = json.load(f)
            return data
        except Exception as e:
            print(f'Открытие JSON {e}')

    # следующие 10 методов преобразуют данные из json в понятный для пользователя вид
    def date(self):
        js = self.data()
        date = []
        for i in range(40):
            dt = js["list"][i]["dt_txt"]
            date.extend([dt])
        return date

    def temperature(self):
        js = self.data()
        temp = []
        for i in range(40):
            kelvins = js["list"][i]["main"]["temp"]
            celsius = round(kelvins - 273.15, 1)
            temp.extend([celsius])
        return temp

    def feels_like(self):
        js = self.data()
        feels_like = []
        for i in range(40):
            kelvins = js["list"][i]["main"]["feels_like"]
            celsius = round(kelvins - 273.15, 1)
            feels_like.extend([celsius])
        return feels_like

    def min_temp(self):
        js = self.data()
        min_temp = []
        for i in range(40):
            kelvins = js["list"][i]["main"]["temp_min"]
            celsius = round(kelvins - 273.15, 1)
            min_temp.extend([celsius])
        return min_temp

    def max_temp(self):
        js = self.data()
        max_temp = []
        for i in range(40):
            kelvins = js["list"][i]["main"]["temp_max"]
            celsius = round(kelvins - 273.15, 1)
            max_temp.extend([celsius])
        return max_temp

    def pressure(self):
        js = self.data()
        pressure = []
        for i in range(40):
            mbars = js["list"][i]["main"]["pressure"]
            millimeters = round(mbars / 1.3333, 1)
            pressure.extend([millimeters])
        return pressure

    def humidity(self):
        js = self.data()
        humidity = []
        for i in range(40):
            persents = js["list"][i]["main"]["humidity"]
            humidity.extend([persents])
        return humidity

    def wind(self):
        js = self.data()
        wind = {}
        words = ''
        for i in range(40):
            deg = js["list"][i]["wind"]["deg"]
            speed = js["list"][i]["wind"]["speed"]
            if 0 <= deg <= 22.3 or 337.4 <= deg <= 360:  # север
                words = "Северный"
            elif 292.3 <= deg <= 337.3:  # северо-запад
                words = "Северо-западный"
            elif 247.4 <= deg <= 292.3:  # запад
                words = "Западный"
            elif 202.3 <= deg <= 247.3:  # юго-запад
                words = "Юго-западный"
            elif 157.4 <= deg <= 202.3:  # юг
                words = "Южный"
            elif 112.4 <= deg <= 157.3:  # юго-восток
                words = "Юго-восточный"
            elif 67.4 <= deg <= 112.3:  # восток
                words = "Восточный"
            elif 22.4 <= deg <= 67.3:  # северо-восток
                words = "Северо-восточный"
            wind[i] = words, deg, speed
        return wind

    def weather(self):
        js = self.data()
        weather = {}
        for i in range(40):
            main = js["list"][i]["weather"][0]["main"]
            description = js["list"][i]["weather"][0]["description"].capitalize()
            icon = js["list"][i]["weather"][0]["icon"]
            weather[i] = main, description, icon
        return weather

    def info(self):
        js = self.data()
        city_name = js["city"]["name"]
        city_lat = js["city"]["coord"]["lat"]
        city_lon = js["city"]["coord"]["lon"]
        country = js["city"]["country"]
        info = [city_name, country, city_lat, city_lon]
        return info

    # данный метод объединяет информацию их вышестоящих методов для дня, передаваемого экземпляру класса
    def day_list(self):
        day_list = []
        day_list.extend([self.info()[0]])  # 0
        day_list.extend([self.info()[1]])  # 1
        day_list.extend([self.date()[self.day]])  # 2
        day_list.extend([self.temperature()[self.day]])  # 3
        day_list.extend([self.min_temp()[self.day]])  # 4
        day_list.extend([self.max_temp()[self.day]])  # 5
        day_list.extend([self.feels_like()[self.day]])  # 6
        day_list.extend([self.pressure()[self.day]])  # 7
        day_list.extend([self.humidity()[self.day]])  # 8
        day_list.extend([self.wind()[self.day]])  # 9
        day_list.extend([self.weather()[self.day]])  # 10
        return day_list

    # возвращает преобразованную информацию из метода day_list
    def returning(self):
        text = f"Данные о городе: {self.info()[0]}, {self.info()[1]}\n\n"
        text += f"Дата: {str(self.date()[self.day])[8:10]}.{str(self.date()[self.day])[5:7]}." \
                f"{str(self.date()[self.day])[:4]} {str(self.date()[self.day])[-8:-3]}\n\n"
        text += f"Температура: {self.temperature()[self.day]}С°\n"
        text += f"Ощущается как: {self.feels_like()[self.day]}С°\n"
        text += f"Минимальная температура: {self.min_temp()[self.day]}С°\n"
        text += f"Максимальная температура: {self.max_temp()[self.day]}С°\n"
        text += f"\n"
        text += f"Осадки: {self.weather()[self.day][1]}\n"
        text += f"Давление: {self.pressure()[self.day]} Мм.Рт.С\n"
        text += f"Влажность: {self.humidity()[self.day]}%\n"
        text += f"Ветер: {self.wind()[self.day][0]}, {self.wind()[self.day][2]} км/ч\n"
        return text


if __name__ == "__main__":
    print("0 - погода сегодня")
    print("1 - погода на ближайшую неделю")
    choose = int(input())
    if choose == 0:
        print("Погода сегодня:\n")
        print(Weather(1).day_list())
    elif choose == 1:
        print("Погода на ближайшую неделю:")
        Weather(1).all_days()
    else:
        print("Ошибка ввода")
