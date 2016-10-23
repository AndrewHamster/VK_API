""" Thanks to OlegWock at codeguida.com for detailed guide """

import vk, os, time, math
from urllib import request
import json

#if exists token.json it will try to use its "access_token"
try:
    token = json.load(open('token.json'))
    if not token['access_token'] == 'your_token':
        session = vk.Session(token['access_token'])
    else:
        session = vk.Session()
#otherwise, standart session will begin
except Exception:
    session = vk.Session()

api = vk.API(session)

#reading url
url = input('Album urll: ')

#getting album_id and owner_id
a_id = url.split('/')[-1].split('_')[1].replace(' ', '')
o_id = url.split('/')[-1].split('_')[0].replace('album', '')

photos_count = api.photos.getAlbums(owner_id=o_id, album_id=a_id)[0]['size']

counter = 0
breaked = 0
time_of_start = time.time()

#creating folders if necessary
if not os.path.exists('pics'):
    os.mkdir('pics')

folder = 'pics/album{0}_{1}'.format(o_id, a_id)

if not os.path.exists(folder):
    os.mkdir(folder)
    
#api allows up to 1000 photos per one request
req_count = math.ceil(photos_count / 1000)

for j in range(req_count):

    photos = api.photos.get(owner_id=o_id, album_id=a_id, count=1000, offset=j*1000)

    for photo in photos:
        counter += 1
        url = photo['src_big']

        print('Loading photo #{} of {}'.format(counter, photos_count))
        try:
            pth = folder + '/' + os.path.split(url)[1]
            request.urlretrieve(url, pth)
        except Exception:
            print('Error, skipping file...')
            breaked += 1
            continue

delta_time = time.time() - time_of_start

print('\nTargets: {}\nSuccess: {}\nSkipped: {}\nTime spent: {} s'.format(photos_count, counter, breaked, round(delta_time, 1)))


