from os import path
from datetime import datetime
import time

from PIL import Image, ImageDraw, ImageFont, ImageFilter


class CardGenerator:
    def __init__(self, data):
        if __name__ == '__main__':
            self.path = 'picgen/'
        else:
            self.path = 'weather/picgen/'
        self.data = data
        self.main()

    def background(self):
        img = Image.open(path.abspath(self.path + f'backgrounds/{self.data[10][2]}.png')).resize((2560, 1440))
        img = img.crop(((2560 - 1080) / 2, (1440 - 1080) / 2, (2560 + 1080) / 2, (1440 + 1080) / 2))
        img = img.filter(ImageFilter.GaussianBlur(radius=5))
        grad = Image.open(path.abspath(self.path + f'gradient.png'))
        img.paste(grad, (0, 1080 - 384), grad)
        return img

    def icon_paste(self, image):
        img = image
        hum = Image.open(path.abspath(self.path + 'icons/hum.png'))
        loc = Image.open(path.abspath(self.path + 'icons/loc.png'))
        press = Image.open(path.abspath(self.path + 'icons/press.png'))
        weather = Image.open(path.abspath(self.path + 'icons/weather.png'))
        wind = Image.open(path.abspath(self.path + 'icons/wind.png'))
        img.paste(loc, (7, 60), loc)
        img.paste(hum, (52, 720), hum)
        img.paste(press, (15, 500), press)
        img.paste(weather, (15, 220), weather)
        img.paste(wind, (15, 370), wind)
        return img

    def text_paste(self, color):
        text = Image.new('RGBA', (1080, 1080))
        drawing = ImageDraw.Draw(text)
        font0 = ImageFont.truetype(path.abspath(self.path + 'fonts/Roboto.ttf'), 68)
        font1 = ImageFont.truetype(path.abspath(self.path + 'fonts/Roboto.ttf'), 50)

        # создание теней
        city_size = font0.getsize(f'{self.data[0]}, {self.data[1]}')
        city_position = (255, 60 + (215 - city_size[1]) / 2)
        drawing.text(city_position, f'{self.data[0]}, {self.data[1]}', fill=color, font=font0)

        date_position = (255, 225)
        drawing.text(date_position, self.data[2], fill=color, font=font1)

        temp_size = font0.getsize(f'{self.data[3]}°')
        temp_position = (980 - temp_size[0], 122)
        drawing.text(temp_position, f'{self.data[3]}°', fill=color, font=font0)

        feels_like_size = font1.getsize(f'{self.data[6]}°')
        feels_like_position = (980 - (temp_size[0] + feels_like_size[0]) / 2, 185)
        drawing.text(feels_like_position, f'{self.data[6]}°', fill=color, font=font1)

        weather_size = font1.getsize(f'{self.data[10][1]}')
        weather_position = (255, 270 + (155 - weather_size[1]) / 2)
        drawing.text(weather_position, f'{self.data[10][1]}', fill=color, font=font1)

        wind_size = font1.getsize(f'{self.data[9][0]}, {self.data[9][2]} км/ч')
        wind_position = (255, 370 + (221 - wind_size[1]) / 2)
        drawing.text(wind_position, f'{self.data[9][0]}, {self.data[9][2]} км/ч', fill=color, font=font1)

        pressure_size = font1.getsize(f'{self.data[7]} мм. рт. ст.')
        pressure_position = (255, 500 + (272 - pressure_size[1]) / 2)
        drawing.text(pressure_position, f'{self.data[7]} мм. рт. ст.', fill=color, font=font1)

        humidity_size = font1.getsize(f'{self.data[8]}%')
        humidity_position = (255, 720 + (194 - humidity_size[1]) / 2)
        drawing.text(humidity_position, f'{self.data[8]}%', fill=color, font=font1)

        # возвращаем img
        return text

    def main(self):
        img = self.background()
        img = self.icon_paste(img)
        shadow = self.text_paste('#000000').filter(ImageFilter.GaussianBlur(radius=5))
        img.paste(shadow, (0, 0), shadow)
        text = self.text_paste('#ffffff')
        img.paste(text, (0, 0), text)
        img.save(path.abspath(self.path + 'card.png'))


if __name__ == '__main__':
    CardGenerator(['Череповец', 'RU', '2020-03-18 15:00:00', 4.2, 2.1, 4.2, -1.1, 758.3, 96,
                   ('Юго-западный', 232, 5.63), ('Rain', 'Небольшой дождь', '10d')])
