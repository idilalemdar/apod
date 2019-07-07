#!/usr/bin/env python3

import urllib3
import urllib.request
import json
from subprocess import Popen

directory = '/home/cydonia/Pictures/apod/'
url = 'https://api.nasa.gov/planetary/apod?api_key=zaVObY9zGhMh20jhIaTwqUkrgdAeftR8MltzY5ye'


class InvalidMediaType(Exception):
    """Raised when the media type of that day is not image"""
    pass


def notify(message):
    # TODO: Not the notification type I wanted. Do research
    p = Popen(['notify-send', message])
    p.wait()


def setWallpaper(saveAs):
    args = ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + saveAs]
    q = Popen(args)
    q.wait()
    print('Wallpaper set.')


def getInfo(url):
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    print("Information retrieved...")
    return json.loads(response.data.decode('utf-8'))


def downloadImage(response):
    if response['media_type'] == 'image':
        imgUrl = response['hdurl']
        imgName = imgUrl.strip().split('/')[-1]
        saveAs = directory + response['date'] + '_' + imgName
        urllib.request.urlretrieve(imgUrl, saveAs)
        print("Image retrieved...")
        return saveAs, response['explanation']
    else:
        raise InvalidMediaType


def run():
    response = getInfo(url)
    try:
        saveAs, explanation = downloadImage(response)
        setWallpaper(saveAs)
        notify(explanation)
    except InvalidMediaType:
        notify('Media type not supported.')


if __name__ == '__main__':
    run()
