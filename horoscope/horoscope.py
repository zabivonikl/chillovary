from lxml import html
import requests


class DataParse:
    def __init__(self, text):
        if __name__ == '__main__':
            self.path = 'cardgenerator/'
        else:
            self.path = 'horoscope/cardgenerator/'
        urls = {'овен': 'https://horoscopes.rambler.ru/aries/',
                'телец': 'https://horoscopes.rambler.ru/taurus/',
                'близнецы': 'https://horoscopes.rambler.ru/gemini/',
                'рак': 'https://horoscopes.rambler.ru/cancer/',
                'лев': 'https://horoscopes.rambler.ru/leo/',
                'дева': 'https://horoscopes.rambler.ru/virgo/',
                'весы': 'https://horoscopes.rambler.ru/libra/',
                'скорпион': 'https://horoscopes.rambler.ru/scorpio/',
                'стрелец': 'https://horoscopes.rambler.ru/sagittarius/',
                'козерог': 'https://horoscopes.rambler.ru/capricorn/',
                'водолей': 'https://horoscopes.rambler.ru/aquarius/',
                'рыбы': 'https://horoscopes.rambler.ru/pisces/'}
        self.url = urls[text]
        self.text = ''
        self.parse()

    def parse(self):
        response = requests.get(self.url).content.decode('u8')
        tree = html.fromstring(response)
        text = tree.xpath('//div[@class="_1dQ3"]/span/text()')
        self.text = text[0]

    def __str__(self):
        return f'{self.text}'
