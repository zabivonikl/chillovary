from os import path
import requests
import json

from lxml import html
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageEnhance


class Info:
    # запускаем загрузчик
    def __init__(self):
        if __name__ == '__main__':
            self.path = ''
        else:
            self.path = 'wallet/'
        self.save()

    # открываем json
    def data(self):
        with open(path.abspath(self.path + "data/wallet_temp.json")) as f:
            js = json.load(f)
        return js

    # генерируем список из валют по формуле курс / номинал
    def wallet_list(self):
        js = self.data()
        wallet_list = []
        wallet_list.extend([str(round(js["Valute"]["GBP"]["Value"] / js["Valute"]["GBP"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["USD"]["Value"] / js["Valute"]["USD"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["EUR"]["Value"] / js["Valute"]["EUR"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["UAH"]["Value"] / js["Valute"]["UAH"]["Nominal"], 2))])
        return wallet_list

    # сохраняем курс на диск
    def save(self):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        request = requests.get(url).text.encode("u8").decode("u8")
        with open(path.abspath(self.path + "data/wallet_temp.json"), "w") as f:
            f.write(request)

    @staticmethod
    def rbc_parse():
        url = 'https://quote.rbc.ru/ticker/181206'
        response = requests.get(url).content
        tree = html.fromstring(response)
        brent_price = tree.xpath('//div[@class="chart__info__row js-ticker"]/span[@class="chart__info__sum"]/text()')
        return f"{brent_price[1]}{brent_price[0]}"

    # преобразуем данные в потребный вид
    def main(self):
        wallet_list = self.wallet_list()
        text = "Курсы валют:\n"
        text += f"Британский фунт/Рубль: {wallet_list[0]}₽\n"
        text += f"Белорусский рубль/Рубль: {wallet_list[1]}₽\n"
        text += f"Доллар США/Рубль: {wallet_list[2]}₽\n"
        text += f"Евро/Рубль: {wallet_list[3]}₽\n"
        text += f"Гривна/Рубль: {wallet_list[4]}₽\n\n"
        text += f"Нефть марки Brent: {self.rbc_parse()}"
        return text

    def list_generator(self):
        data = self.wallet_list()
        data.append(self.rbc_parse())
        return data


class WalletCardGenerator:
    def __init__(self, data):
        if __name__ == '__main__':
            self.path = 'cardgenerator/'
        else:
            self.path = 'wallet/cardgenerator/'
        self.data = data
        self.main()

    def background(self):
        img = Image.open(path.abspath(self.path + 'layouts/money.png'))
        gradient = Image.open(path.abspath(self.path + 'layouts/tube.png'))
        img.paste(gradient, (457, 370), gradient)
        return img

    def icons(self, image):
        img = image
        usd = Image.open(path.abspath(self.path + 'icons/usd.png'))
        eur = Image.open(path.abspath(self.path + 'icons/eur.png'))
        gph = Image.open(path.abspath(self.path + 'icons/gbp.png'))
        uah = Image.open(path.abspath(self.path + 'icons/uah.png'))
        oil = Image.open(path.abspath(self.path + 'icons/oil.png'))
        img.paste(usd, (75, 80), usd)
        img.paste(eur, (60, 240), eur)
        img.paste(gph, (60, 420), gph)
        img.paste(uah, (60, 580), uah)
        img.paste(oil, (50, 760), oil)
        return img

    def text(self, color):
        text = Image.new('RGBA', (1080, 1080))
        drawing = ImageDraw.Draw(text)
        font = ImageFont.truetype(path.abspath(self.path + 'fonts/Roboto.ttf'), 64)

        usd_size = font.getsize(f'{self.data[1]}руб.')
        usd_position = (225, 80 + (184 - usd_size[1]) / 2)
        drawing.text(usd_position, f'{self.data[1]}руб.', fill=color, font=font)

        eur_size = font.getsize(f'{self.data[2]}руб.')
        eur_position = (225, 240 + (185 - eur_size[1]) / 2)
        drawing.text(eur_position, f'{self.data[2]}руб.', fill=color, font=font)

        gbp_size = font.getsize(f'{self.data[0]}руб.')
        gbp_position = (225, 420 + (176 - gbp_size[1]) / 2)
        drawing.text(gbp_position, f'{self.data[0]}руб.', fill=color, font=font)

        uah_size = font.getsize(f'{self.data[3]}руб.')
        uah_position = (225, 580 + (184 - uah_size[1]) / 2)
        drawing.text(uah_position, f'{self.data[3]}руб.', fill=color, font=font)

        oil_size = font.getsize(f'{self.data[4]}$')
        oil_position = (225, 760 + (191 - oil_size[1]) / 2)
        drawing.text(oil_position, f'{self.data[4]}', fill=color, font=font)

        return text

    def main(self):
        img = self.background()
        img = self.icons(img)
        ench = ImageEnhance.Color(img)
        img = ench.enhance(1.1)
        shadow = self.text('#000000').filter(ImageFilter.GaussianBlur(radius=3))
        img.paste(shadow, (0, 0), shadow)
        text = self.text('#ffffff')
        img.paste(text, (0, 0), text)
        img = img.convert('RGB')
        img.save(path.abspath(self.path + 'card.png'))


if __name__ == "__main__":
    data = Info().list_generator()
    WalletCardGenerator(data)
