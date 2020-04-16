from os import system
from io import BytesIO

from PIL import Image
from requests import get


class Distortion:
    def __init__(self, url):
        if __name__ == '__main__':
            self.path = '/'
        else:
            self.path = 'distortion/'
        self.url = url
        self.pic_download()
        self.distortion()

    def pic_download(self):
        data = get(self.url).content
        with open(self.path + 'picture.jpg', 'wb') as f:
            f.write(data)

    def distortion(self):
        image = Image.open(self.path + 'picture.jpg')
        img_sizes = image.width, image.height
        distort_cmd = f"convert {self.path + 'picture.jpg'} -liquid-rescale 60x60%!" \
                      f" -resize {img_sizes[0]}x{img_sizes[1]}\! {self.path + 'picture.jpg'}"

        system(distort_cmd)

        buf = BytesIO()
        buf.name = 'image.jpeg'

        buf.seek(0)

        return buf
