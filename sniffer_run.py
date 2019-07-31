import spotSniff
import requests
import json


def main():
    token = spotSniff.authentify()
    headers = {'Authorization': 'Bearer {0}'.format(token)}
    spotify_data = spotSniff.dict_checker()
    spotify_bands_from_txt_file = spotSniff.spotify_band_ids()
    spotify_bands_from_dict = [band['id'] for band in spotify_data['bands']]
    list_check = [x for x in spotify_bands_from_txt_file if x not in spotify_bands_from_dict]
    if len(list_check) == 0:
        pass
    else:
        for new_band in list_check:
            artist_payload = (requests.get('https://api.spotify.com/v1/artists/{0}'.format(new_band), headers=headers).text).json.loads
            artist_id = artist_payload['id']
            artist_name = artist_payload['name']
            latest_single_block = spotSniff.metadata_funnel(headers, new_band, 'single')
            latest_album_block = spotSniff.metadata_funnel(headers, new_band, 'album')
            latest_comp_block = spotSniff.metadata_funnel(headers, new_band, 'compilation')
            spotify_data['bands'].append({'id': artist_id, 'name': artist_name, 'latest_single': latest_single_block,
                                          'latest_album': latest_album_block, 'latest_comp': latest_comp_block})
    new_entries = []
    for band in spotify_data['bands']:
        spotSniff.release_checker(headers, band, 'single', 'latest_single', new_entries)
        spotSniff.release_checker(headers, band, 'album', 'latest_album', new_entries)
        spotSniff.release_checker(headers, band, 'compilation', 'latest_comp', new_entries)
    if len(new_entries) == 0:
        pass
    elif len(new_entries) >= 1:
        temp_list = []
        for entry in new_entries:
            entry_string = '{0} released a new {1} called \"{2}\" on {3}. '\
            'Listen to it here: {4}'.format(entry['artist'], entry['kind'],
                                            entry['title'], entry['date'], entry['url'])
            temp_list.append(entry_string)
        new_spotify_content = '\n\n'.join(temp_list)
        EMAIL_FROM = spotSniff.config_check()['MAILIFY']['EMAIL_FROM']
        EMAIL_TO = spotSniff.config_check()['MAILIFY']['EMAIL_TO']
        EMAIL_SUBJECT = 'New Music is Waiting for You at Spotify'
        EMAIL_CONTENT = 'Greetings! I\'m the kindly old robot that watches over your favorite music. '\
        'There\'s new stuff over at Spotify by some of your favorite artists!\n\n{0}\n\nHappy listening!\n\n'\
        'Cordially,\nThe Robot That Runs Spotify Sniffer'.format(new_spotify_content)
        service = spotSniff.mail()
        message = spotSniff.create_message(EMAIL_FROM, EMAIL_TO, EMAIL_SUBJECT, EMAIL_CONTENT)
        spotSniff.send_message(service, 'me', message)
    if len(list_check) == 0 and len(new_entries) == 0:
        pass
    else:
        with open('sniffer_data.json', 'w') as f:
            json.dump(spotify_data, f)


if __name__ == "__main__":
    main()
