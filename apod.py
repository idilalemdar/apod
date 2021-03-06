#!/usr/bin/env python3

from urllib3 import PoolManager, exceptions
from urllib.request import urlretrieve
from json import loads
from subprocess import Popen

# Set the directory you want to save the pictures in
DIRECTORY = '/home/cydonia/Pictures/apod/'
URL = 'https://api.nasa.gov/planetary/apod?api_key=zaVObY9zGhMh20jhIaTwqUkrgdAeftR8MltzY5ye'


def notify(message):
    # TODO: Not the notification type I wanted. Do research
    p = Popen(['notify-send', ' ', message])
    p.wait()


def setWallpaper(saveAs):
    args = ['gsettings', 'set', 'org.gnome.desktop.background', 'picture-uri', 'file://' + saveAs]
    q = Popen(args)
    q.wait()
    print('Wallpaper set.')


def getInfo(url):
    try:
        http = PoolManager()
        response = http.request('GET', url)
        print("Information retrieved...")
        return loads(response.data.decode('utf-8'))
    except exceptions.MaxRetryError:
        notify('APOD: No Internet connectivity found.')
        exit(0)


def downloadImage(response):
    assert response['media_type'] == 'image'
    imgUrl = response['hdurl']
    imgName = imgUrl.strip().split('/')[-1]
    saveAs = DIRECTORY + response['date'] + '_' + imgName
    urlretrieve(imgUrl, saveAs)
    print("Image retrieved...")
    return saveAs, response['explanation']


def run():
    response = getInfo(URL)
    try:
        saveAs, explanation = downloadImage(response)
        setWallpaper(saveAs)
        notify(explanation)
    except AssertionError:
        notify('APOD: Media type not supported.')
    except KeyError:
        notify('APOD: Service not available.')


if __name__ == '__main__':
    run()
    exit(0)

