from os import path

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
        img.paste(loc, (70, 55), loc)
        img.paste(hum, (100, 755), hum)
        img.paste(press, (90, 600), press)
        img.paste(weather, (85, 270), weather)
        img.paste(wind, (77, 448), wind)
        return img

    def text_paste(self, image):
        img = image
        text = Image.new('RGBA', (1080, 1080))
        drawing = ImageDraw.Draw(text)
        font0 = ImageFont.truetype(path.abspath(self.path + 'fonts/Roboto.ttf'), 72)
        font1 = ImageFont.truetype(path.abspath(self.path + 'fonts/Roboto.ttf'), 60)

        # создание теней
        city_size = font0.getsize(f'{self.data[0]}, {self.data[1]}')
        city_position = (245, 55 + (215 - city_size[1]) / 2)
        drawing.text(city_position, f'{self.data[0]}, {self.data[1]}', fill='#000000', font=font0)

        date_position = (245, 200)
        drawing.text(date_position, self.data[2], fill='#000000', font=font0)

        text.filter(ImageFilter.GaussianBlur(radius=200))

        # наложение тени
        img.paste(text, (0, 0), text)
        img.show()

        # возвращаем img
        return img

    def main(self):
        img = self.background()
        img = self.icon_paste(img)
        img = self.text_paste(img)
        # img.save(path.abspath(self.path + 'card.png'))


if __name__ == '__main__':
    CardGenerator(['Череповец', 'RU', '2020-03-18 15:00:00', 4.2, 2.1, 4.2, -1.1, 758.3, 96,
                   ('Юго-западный', 232, 5.63), ('Rain', 'Небольшой дождь', '10d')])