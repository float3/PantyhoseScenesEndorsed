from bs4 import BeautifulSoup as BS
import requests
import shutil
import os
import sys

def Result(res, index, chapter):
    if res.status_code == 200:
        with open('ch' + str(chapter) + '\\' + str(index) + ".png", 'wb') as f:
            shutil.copyfileobj(res.raw, f)
        print('Image sucessfully Downloaded: ', str(index) + ".png")
    else:
        print('Image Couldn\'t be retrieved: ', str(index) + ".png")


input = str(sys.argv[1])
chapters = int(sys.argv[2])

for chapter in range(1, chapters):
    os.mkdir('ch' + str(chapter))
    html = requests.get(input + str(chapter))
    soup = BS(html.content, features="html.parser")
    index = 0

    for imgtag in soup.find_all('img'):
        res = requests.get(imgtag['src'], stream=True)

        Result(res, index, chapter)
        index += 1
