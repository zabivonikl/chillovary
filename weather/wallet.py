from os import path
import requests
import json

from lxml import html


class Wallets:
    # запускаем загрузчик
    def __init__(self):
        pass
        # self.save()

    # открываем json
    @staticmethod
    def data():
        with open(path.abspath("weather/data/wallet_temp.json")) as f:
            js = json.load(f)
        return js

    # генерируем список из валют по формуле курс / номинал
    def wallet_list(self):
        js = self.data()
        wallet_list = []
        wallet_list.extend([str(round(js["Valute"]["GBP"]["Value"] / js["Valute"]["GBP"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["BYN"]["Value"] / js["Valute"]["BYN"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["USD"]["Value"] / js["Valute"]["USD"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["EUR"]["Value"] / js["Valute"]["EUR"]["Nominal"], 2))])
        wallet_list.extend([str(round(js["Valute"]["UAH"]["Value"] / js["Valute"]["UAH"]["Nominal"], 2))])
        return wallet_list

    # сохраняем курс на диск
    def save(self):
        url = "https://www.cbr-xml-daily.ru/daily_json.js"
        request = requests.get(url).text.encode("u8").decode("u8")
        with open(path.abspath("weather/data/wallet_temp.json"), "w") as f:
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
        wallet_list = Wallets().wallet_list()
        text = "Курсы валют:\n"
        text += f"Британский фунт/Рубль: {wallet_list[0]}₽\n"
        text += f"Белорусский рубль/Рубль: {wallet_list[1]}₽\n"
        text += f"Доллар США/Рубль: {wallet_list[2]}₽\n"
        text += f"Евро/Рубль: {wallet_list[3]}₽\n"
        text += f"Гривна/Рубль: {wallet_list[4]}₽\n\n"
        text += f"Нефть марки Brent: {self.rbc_parse()}"
        return text


if __name__ == "__main__":
    Wallets().finmarket_parse()
