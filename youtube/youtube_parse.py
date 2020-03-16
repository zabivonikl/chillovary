from os import path

from PIL import Image
from lxml import etree
import vk_api
from vk_api import VkUpload
import requests
from textwrap import shorten

from config import YTConfig, Config


class Youtube:
    def __init__(self, ch_list):
        self.authors = []
        self.title = []
        self.link = []
        self.img = []
        self.cl = ch_list
        if __name__ == '__main__':
            self.way = ''
        else:
            self.way = 'youtube/'
        self.channel_parse()
        self.pictures_download()
        self.pictures_correction()
        self.pictures_upload()

    def xml_download(self, id):
        url = YTConfig.ROOT_URL + id
        response = requests.get(url).content
        with open(path.abspath(self.way + 'temp/xml.xml'), 'wb') as f:
            f.write(response)

    def channel_parse(self):
        authors = []
        title = []
        link = []
        img = []
        for i in range(len(self.cl)):
            self.xml_download(self.cl[i])
            tree = etree.parse(path.abspath(self.way + 'temp/xml.xml'))
            root = tree.getroot()
            title.append(root[7][8][0].text)
            img.append(root[7][8][2].attrib['url'])
            link.append(root[7][4].attrib['href'])
            authors.append(root[5][0].text)
        self.authors = authors
        self.title = title
        self.link = link
        self.img = img

    def pictures_download(self):
        for i in range(len(self.cl)):
            response = requests.get(self.img[i]).content
            with open(path.abspath(self.way + f'temp/preview{i}.jpg'), 'wb') as f:
                f.write(response)

    def pictures_correction(self):
        for i in range(len(self.cl)):
            img = Image.open(path.abspath(self.way + f'temp/preview{i}.jpg'))
            chords = int((480 - 439) / 2), int((360 - 270) / 2), int((480 + 439) / 2), int((360 + 270) / 2)
            cropped = img.crop(chords).resize((221 * 3, 136 * 3))
            cropped.save(path.abspath(self.way + f'temp/preview{i}.jpg'))

    def pictures_upload(self):
        url_list = []
        paths = []
        session = vk_api.VkApi(token=Config.TOKEN, client_secret=Config.TOKEN)
        for i in range(len(self.cl)):
            paths.append(path.abspath(self.way + f'temp/preview{i}.jpg'))
        resp = VkUpload(session).photo_messages(photos=paths)
        for i in range(len(self.cl)):
            url_list.append(f"{resp[i]['owner_id']}_{resp[i]['id']}")
        self.img = url_list

    def dict_generator(self):
        elements = []
        for i in range(len(self.cl)):
            part = {
                    "title": shorten(self.title[i], 80),
                    "description": shorten(self.authors[i], 80),
                    "action": {
                        "type": "open_link",
                        "link": self.link[i]
                    },
                    "photo_id": self.img[i],
                    "buttons": [{
                        "action": {
                            "type": "open_link",
                            "label": "Открыть",
                            "link": self.link[i],
                            "payload": "{}"
                        }
                    }]
                    }
            elements.append(part)
        template = {"type": "carousel", "elements": elements}
        return template


if __name__ == '__main__':
    Youtube(None)
