#!/usr/bin/env python3

import urllib3
import urllib.request
import json
import os
import subprocess as sp

directory = '/home/cydonia/Pictures/apod/'
url = 'https://api.nasa.gov/planetary/apod?api_key=zaVObY9zGhMh20jhIaTwqUkrgdAeftR8MltzY5ye'
http = urllib3.PoolManager()

response = http.request('GET', url)
print("Information retrieved...")

response = json.loads(response.data.decode('utf-8'))

if response['media_type'] == 'image':
    imgurl = response['hdurl']
    imgname = imgurl.strip().split('/')[-1]
    saveAs = directory + response['date'] + '_' + imgname
    urllib.request.urlretrieve(imgurl, saveAs)
    print("Image retrieved...")

    # TODO: search for a possibly better way to do this (fit in the windows options etc)
    os.system('gsettings set org.gnome.desktop.background picture-uri file://' + saveAs)
    notification = ['notify-send', response['explanation']]
    sp.run(notification)

else:
    os.system('notify-send \'No new picture for today :( \'')
