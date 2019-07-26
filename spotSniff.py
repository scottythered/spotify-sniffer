import requests
import json
import os
import re
import sys
import pickle
from googleapiclient.discovery import build
from email.mime.text import MIMEText
import base64


def config_check():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'config.json')):
        with open('config.json', 'r') as f:
            return json.load(f)
    else:
        print('No config file! Come back when you get one.')
        sys.exit()


def authentify():
    client_id = config_check()['AUTHENTIFY']['client_id']
    client_secret = config_check()['AUTHENTIFY']['client_secret']
    grant_type = 'client_credentials'
    body_params = {'grant_type' : grant_type}
    url = 'https://accounts.spotify.com/api/token'
    response = requests.post(url, data=body_params, auth = (client_id, client_secret))
    resp_json = json.loads(response.text)
    token = resp_json['access_token']
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    response = requests.get('https://api.spotify.com/v1/artists/2Sp19cOHSqAUlE64hekARW/albums', headers=headers)
    if response.status_code == 200:
        return token
    else:
        print('Could not authenticate!')


def spotify_band_ids():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'spotify_artists.txt')):
        with open('spotify_artists.txt', 'r') as inputter:
            temp_list = []
            band_ids = inputter.read().split(', ')
            for band_id in band_ids:
                matcher = re.fullmatch('[0-9A-Za-z]{22}', band_id.strip())
                if matcher:
                    pass
                else:
                    temp_list.append(band_id)
            if len(temp_list) >= 1:
                bad_ids = ', '.join(temp_list)
                print('Looks like you got some Spotify artist IDs that, uh, aren\'t formulated well. ' \
                      'I\'m gonna shut this down, and you should look at these artist IDs: {0}'.format(bad_ids))
                sys.exit()
            elif len(temp_list) == 0:
                return band_ids
    else:
        print('You don\'t have any artists to check on! Now I have to quit!')
        sys.exit()


def metadata_funnel(h, x, y):
    try:
        latest_album = requests.get('https://api.spotify.com/v1/artists/{0}/albums?include_groups={1}'.format(x, y), headers=h)
        latest_album_id = json.loads(latest_album.text)['items'][0]['id']
        latest_album_name = json.loads(latest_album.text)['items'][0]['name']
        latest_album_rd = json.loads(latest_album.text)['items'][0]['release_date']
        latest_album_url = 'https://open.spotify.com/album/{0}'.format(latest_album_id)
        latest_album_block = {'id': latest_album_id, 'name': latest_album_name, 'date': latest_album_rd, 'url': latest_album_url}
    except:
        latest_album_block = {'id': 'n/a', 'name': 'n/a', 'date': 'n/a', 'url': 'n/a'}
    return latest_album_block


def dict_checker():
    path = os.getcwd()
    if os.path.exists(os.path.join(path, 'sniffer_data.json')):
        with open(os.path.join(path, 'sniffer_data.json'), 'r') as f:
            return json.load(f)
    else:
        try:
            token = authentify()
            headers = {'Authorization': 'Bearer {0}'.format(token)}
            spotify_bands = spotify_band_ids()
            spotify_data_list = []
            for band in spotify_bands:
                artist_payload = requests.get('https://api.spotify.com/v1/artists/{0}'.format(band), headers=headers)
                artist_id = json.loads(artist_payload.text)['id']
                artist_name = json.loads(artist_payload.text)['name']
                latest_single_block = metadata_funnel(band, 'single')
                latest_album_block = metadata_funnel(band, 'album')
                latest_comp_block = metadata_funnel(band, 'compilation')
                whole_entry = {'id': artist_id, 'name': artist_name, 'latest_single': latest_single_block,
                               'latest_album': latest_album_block, 'latest_comp': latest_comp_block}
                spotify_data_list.append(whole_entry)
                all_data = {'bands': spotify_data_list}
            with open(os.path.join(path, 'sniffer_data.json'), 'w') as f:
                json.dump(all_data, f)
            print('We just created a data profile based on your list of Spotify '\
                  'artists. Run Spotify Sniffer tomorrow to see if anyone drops '\
                  'new music!')
            sys.exit()
        except:
            print('Something is wrong. You may not have sufficient privileges '\
                  'to make a file. Bogus!')
            sys.exit()


def release_checker(h, xx, yy, zz, new_entries_list):
    band_id = xx['id']
    try:
        band_release = requests.get('https://api.spotify.com/v1/artists/{0}/albums?include_groups={1}'.format(band_id, yy), headers=h)
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
            new_entries_list.append({'artist': xx['name'], 'kind': yy, 'title': newest_release_name,
                                     'date': newest_release_rd, 'url': newest_release_url})
    except IndexError:
        pass


def mail():
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    service = build('gmail', 'v1', credentials=creds)
    return service


def create_message(sender, to, subject, message_text):
    message = MIMEText(message_text)
    message['to'] = to
    message['from'] = sender
    message['subject'] = subject
    return {'raw': base64.urlsafe_b64encode(message.as_string().encode()).decode()}


def send_message(service, user_id, message):
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
        print('Message Id: %s' % message['id'])
        return message
    except HttpError as error:
        print(error)
