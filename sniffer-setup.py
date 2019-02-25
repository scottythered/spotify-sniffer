#!/usr/bin/env python
# coding: utf-8

import requests
import json
import os
import re
import sys


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
        return os.path.join(path, 'sniffer_data.json')
    else:
        try:
            with open(os.path.join(path, 'sniffer_data.json'), 'w'):
                pass
            return os.path.join(path, 'sniffer_data.json')
        except:
            print('Something is wrong. You may not have sufficient privileges to make a file. Bogus!')
            sys.exit()


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
                print('Looks like you got some Spotify artist IDs that, uh, aren\'t formulated well. I\'m gonna shut this down, and you should look at these artist IDs: {0}'.format(bad_ids))
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

spotify_data = dict_checker()

spotify_bands = spotify_band_ids()

spotify_data_list = []

for band in spotify_bands:
    artist_payload = requests.get('https://api.spotify.com/v1/artists/{0}'.format(band), headers=headers)
    artist_id = json.loads(artist_payload.text)['id']
    artist_name = json.loads(artist_payload.text)['name']
    latest_single_block = metadata_funnel(band, 'single')
    latest_album_block = metadata_funnel(band, 'album')
    latest_comp_block = metadata_funnel(band, 'compilation')
    whole_entry = {'id': artist_id, 'name': artist_name, 'latest_single': latest_single_block, 'latest_album': latest_album_block, 'latest_comp': latest_comp_block}
    spotify_data_list.append(whole_entry)

all_data = {'bands': spotify_data_list}

with open(spotify_data, 'w') as f:
    json.dump(all_data, f)
