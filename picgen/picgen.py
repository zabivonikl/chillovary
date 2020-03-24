import requests
from os import path
import textwrap

from PIL import Image, ImageDraw, ImageFont, ImageFilter


class Quotes:
    def __init__(self, authors, text, links, logo):

        # инициализируем пути
        if __name__ == '__main__':
            self.way = 'templates/'
        else:
            self.way = 'picgen/templates/'

        # объявляем константы
        self.authors = authors
        self.text = text
        self.links = links
        self.logo = logo
        self.head_font = ImageFont.truetype(path.abspath(self.way + 'naming.ttf'), 120)
        self.author_font = ImageFont.truetype(path.abspath(self.way + 'sig.ttf'), 50)
        self.text_font = ImageFont.truetype(path.abspath(self.way + 'text.ttf'), 75 )

        # запускаем алгоритм
        self.main()

    def download(self):
        # читаем ссылки из массива, делаем запрос и сохраняем картинку
        for i in range(len(self.links)):
            if len(self.links) == 1:
                img = requests.get(self.links[i])
            else:
                img = requests.get(self.links[i])
            with open(path.abspath(self.way + f'avatar{i}.png'), 'wb') as f:
                f.write(img.content)
        return None

    def dr_background(self):
        # создаём фон
        background = Image.new('RGB', (1080, 1080))

        # высчитываем ширину полосок с аватарами
        authors_count = len(self.authors)
        avatar_width = int(1080 / authors_count)

        # вставляем аватар
        for i in range(authors_count):
            avatar = Image.open(path.abspath(self.way + f'avatar{i}.png'))
            resized = avatar.resize((1080, 1080))
            cropped = resized.crop(((1080 - avatar_width) / 2, 0, (1080 + avatar_width) / 2, 1080))
            background.paste(cropped, (i * avatar_width, 0))

        # накладываем фильтр и кавычки
        bw = background.convert('L').filter(ImageFilter.BoxBlur(radius=10))
        mask = Image.open(path.abspath(self.way + 'black.png')).resize((1080, 1080))
        bw.paste(mask, (0, 0), mask)

        # сохраняемся
        bw.save(path.abspath(self.way + 'quote.png'))

    def dr_logo(self):
        # открываем изображение
        img = Image.open(path.abspath(self.way + 'quote.png'))
        drawing = ImageDraw.Draw(img)

        # получаем размеры и высчитываем позицию
        logo_size = self.head_font.getsize(self.logo)
        logo_position = (int((1080 - logo_size[0]) / 2), 20)

        # рисуем лого
        drawing.text(logo_position, self.logo, fill='#ffffff', font=self.head_font)

        # сохраняем
        img.save(path.abspath(self.way + 'quote.png'))

    def dr_authors(self):
        # открываем изображение
        img = Image.open(path.abspath(self.way + 'quote.png'))
        drawing = ImageDraw.Draw(img)

        # получаем сумму высот строк с авторами
        max_line_height = 0
        for i in range(len(self.authors)):
            line_height = self.author_font.getsize(self.authors[i])[1]
            if line_height > max_line_height:
                max_line_height = line_height
        str_height = int(max_line_height * len(self.authors))

        # впиисываем авторов
        for i in range(len(self.authors)):
            str_width = self.author_font.getsize(self.authors[i])[0]
            str_position = (1060 - str_width, 1060 - str_height + max_line_height * i)
            drawing.text(str_position, self.authors[i], fill='#ffffff', font=self.author_font)

        # сохраняем
        img.save(path.abspath(self.way + 'quote.png'))

    def dr_text(self):
        # открываем изображение
        img = Image.open(path.abspath(self.way + 'quote.png'))
        drawing = ImageDraw.Draw(img)

        # высчитываем высоту стоки
        max_str_height = 0
        for i in range(len(self.text)):
            str_height = self.text_font.getsize(self.text[i])[1]
            if str_height > max_str_height:
                max_str_height = str_height
        count = 0
        spaces = 0
        for i in range(len(self.text)):
            formatted = textwrap.fill(self.text[i], width=21)
            cut_string = formatted.split('\n')
            spaces += 1
            for i in range(len(cut_string)):
                count += 1
        text_height = max_str_height * count + spaces * max_str_height * 0.25

        # пишем текст
        # spaces - отступы между сообщениями
        # line - переносы строк
        line = 0
        spaces = 0
        for a in range(len(self.text)):
            formatted = textwrap.fill(self.text[a], width=21)
            cut_string = formatted.split('\n')
            for i in range(len(cut_string)):
                str_size = self.text_font.getsize(cut_string[i])
                str_position = ((1080 - str_size[0]) / 2,
                                (1080 - text_height) / 2 + max_str_height * line + spaces * max_str_height * 0.25)
                line += 1
                drawing.text(str_position, cut_string[i], fill="#ffffff", font=self.text_font)
            spaces += 1

        # сохраняем изображение
        img = img.convert('RGB')
        img.save(path.abspath(self.way + 'quote.png'))

    def main(self):
        # скачиваем аватары
        self.download()

        # создаём фон
        self.dr_background()

        # пишем лого
        self.dr_logo()

        # подписываем авторов
        self.dr_authors()

        # пишем текст
        self.dr_text()


if __name__ == '__main__':
    Quotes("Семён Куфтырев",
           '" я хоть и не танкист,но тебе свой ствол показать могу"© Илья',
           'http://sun9-43.userapi.com/c855628/v855628566/18c21/hhmqGHpyZoE.jpg',
           'Чилловары')
