#!/usr/bin/env python
# coding: utf-8

import requests
import json
import os
import sys
import smtplib
from email.message import EmailMessage
import re


def config_check():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'config.json')):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:
        print('No config file! Come back when you get one.')
        sys.exit()


def dict_checker():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'sniffer_data.json')):
        with open('sniffer_data.json', 'r') as f:
            return json.load(f)
    else:
        print('No Spotify data! Come back when you get some.')
        sys.exit()


def send_email(em_message):
    em_login = config_check()['MAILIFY']['em_login']
    em_password = config_check()['MAILIFY']['em_password']
    serv_loc = config_check()['MAILIFY']['serv_loc']
    msg = EmailMessage()
    msg.set_content(em_message)
    msg['Subject'] = 'New Music is Waiting for You at Spotify'
    msg['From'] = config_check()['MAILIFY']['from_addr']
    msg['To'] = config_check()['MAILIFY']['to_addr']
    server = smtplib.SMTP(serv_loc)
    server.starttls()
    server.login(em_login, em_password)
    problems = server.send_message(msg)
    server.quit()
    if problems:
        return problems


def spotify_band_ids():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'spotify_artists.txt')):
        with open('spotify_artists.txt', 'r') as inputter:
            temp_list = []
            band_ids = inputter.read().split(', ')
            for band_id in band_ids:
                matcher = re.fullmatch('[0-9A-Za-z]{22}', band_id)
                if matcher:
                    pass
                else:
                    temp_list.append(band_id)
            if len(temp_list) >= 1:
                bad_ids = ', '.join(temp_list)
                print('Looks like you got some Spotify artist IDs that, uh, '
                      'aren\'t formulated well. I\'m gonna shut this down and '
                      'you should look at these artists: {0}'.format(bad_ids))
                sys.exit()
            elif len(temp_list) == 0:
                return band_ids
    else:
        print('You don\'t have any artists to check on! Now I have to quit!')
        sys.exit()


def metadata_funnel(x, y):
    try:
        latest_album = requests.get('https://api.spotify.com/v1/artists/{0}/albums?include_groups={1}'.format(x, y), headers=headers)
        latest_album_id = json.loads(latest_album.text)['items'][0]['id']
        latest_album_name = json.loads(latest_album.text)['items'][0]['name']
        latest_album_rd = json.loads(latest_album.text)['items'][0]['release_date']
        latest_album_url = 'https://open.spotify.com/album/{0}'.format(latest_album_id)
        latest_album_block = {'id': latest_album_id, 'name': latest_album_name, 'date': latest_album_rd, 'url': latest_album_url}
    except:
        latest_album_block = {'id': 'n/a', 'name': 'n/a', 'date': 'n/a', 'url': 'n/a'}
    return latest_album_block


def release_checker(xx, yy, zz, new_entries_list):
    band_id = xx['id']
    try:
        band_release = requests.get('https://api.spotify.com/v1/artists/{0}/albums?include_groups={1}'.format(band_id, yy), headers=headers)
        newest_release_id = json.loads(band_release.text)['items'][0]['id']
        last_release_pulled_from_spotify = xx[zz]['id']
        if last_release_pulled_from_spotify == newest_release_id:
            pass
        else:
            newest_release_name = json.loads(band_release.text)['items'][0]['name']
            newest_release_rd = json.loads(band_release.text)['items'][0]['release_date']
            newest_release_url = 'https://open.spotify.com/album/{0}'.format(newest_release_id)
            xx[zz]['id'] = newest_release_id
            xx[zz]['name'] = newest_release_name
            xx[zz]['date'] = newest_release_rd
            xx[zz]['url'] = newest_release_url
            new_entries_list.append({'artist': xx['name'], 'kind': yy, 'title': newest_release_name, 'date': newest_release_rd, 'url': newest_release_url})
    except IndexError:
        pass


def authentify():
    client_id = config_check()['AUTHENTIFY']['client_id']
    client_secret = config_check()['AUTHENTIFY']['client_secret']
    grant_type = 'client_credentials'
    body_params = {'grant_type': grant_type}
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url, data=body_params, auth=(client_id, client_secret))
    resp_json = json.loads(response.text)
    token = resp_json['access_token']
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    response = requests.get('https://api.spotify.com/v1/artists/2Sp19cOHSqAUlE64hekARW/albums', headers=headers)
    if response.status_code == 200:
        print('Authenticated like a motherfucker! Your saved token is: {0}'.format(token))
        return token
    else:
        print('Could not authenticate!')


token = authentify()

headers = {'Authorization': 'Bearer {0}'.format(token)}

spotify_bands = spotify_band_ids()

spotify_data = dict_checker()

spotify_bands_from_data = []

for band in spotify_data['bands']:
    spotify_bands_from_data.append(band['id'])

list_checker = [x for x in spotify_bands if x not in spotify_bands_from_data]

if len(list_checker) == 0:
    pass
else:
    for new_band in list_checker:
        artist_payload = requests.get('https://api.spotify.com/v1/artists/{0}'.format(new_band), headers=headers)
        artist_id = json.loads(artist_payload.text)['id']
        artist_name = json.loads(artist_payload.text)['name']
        latest_single_block = metadata_funnel(new_band, 'single')
        latest_album_block = metadata_funnel(new_band, 'album')
        latest_comp_block = metadata_funnel(new_band, 'compilation')
        whole_entry = {'id': artist_id, 'name': artist_name, 'latest_single': latest_single_block, 'latest_album': latest_album_block, 'latest_comp': latest_comp_block}
        spotify_data['bands'].append(whole_entry)

new_entries = []

for band in spotify_data['bands']:
    release_checker(band, 'single', 'latest_single', new_entries)
    release_checker(band, 'album', 'latest_album', new_entries)
    release_checker(band, 'compilation', 'latest_comp', new_entries)

with open('sniffer_data.json', 'w') as f:
    json.dump(spotify_data, f)

if len(new_entries) == 0:
    pass
elif len(new_entries) >= 1:
    temp_list = []
    for entry in new_entries:
        entry_string = '{0} released a new {1} called \"{2}\" on {3}. Listen to it here: {4}'.format(entry['artist'], entry['kind'], entry['title'], entry['date'], entry['url'])
        temp_list.append(entry_string)
    new_spotify_content = '\n\n'.join(temp_list)
    em_message = 'Greetings! I\'m the kindly old robot that watches over your favorite music. There\'s new stuff over at Spotify by some of your favorite artists!\n\n{0}\n\nHappy listening!\n\nCordially,\nThe Robot That Runs Spotify Sniffer'.format(new_spotify_content)
    send_email(em_message)
