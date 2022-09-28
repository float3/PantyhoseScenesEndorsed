from bs4 import BeautifulSoup
import requests
import shutil
import os
import sys


def iterate_images(result, i, chapter):
    if result.status_code == 200:
        with open('ch' + str(chapter) + '\\' + str(i) + ".png", 'wb') as f:
            shutil.copyfileobj(result.raw, f)
        print('Image sucessfully Downloaded: ', str(i) + ".png")
    else:
        print('Image Couldn\'t be retrieved: ', str(i) + ".png")


def main():
    for chapter in range(1, chapters + 1):
        print("starting chapter: " + str(chapter))
        os.mkdir('ch' + str(chapter))
        html = requests.get(source + str(chapter))
        soup = BeautifulSoup(html.content, features="html.parser")
        index = 0

        for imgtag in soup.find_all('img'):
            res = requests.get(imgtag['src'], stream=True)
            iterate_images(res, index, chapter)
            index += 1


source = str(sys.argv[1])
chapters = int(sys.argv[2])
main()
