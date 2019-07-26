# Spotify Sniffer
Spotify Sniffer is a lightweight script that sniffs out new releases on Spotify.

## What For?
Each time the script is run, Sniffer uses Spotify's web API to check up on the latest album, single, and complilation released by any artist you ask for. If something new has been released since you last ran it, you'll get an email with links to the new music. Use it with crontab or some other scheduling software to sniff out new music on a regular basis.

## Requirements
Sniffer was written for Python 3.6+. You'll also need a gmail account, a Spotify account with authorization credentials (see below), and a passing interest in music.

## Quickstart
1. **Download/clone this repo.** Install the dependencies found in the ```requirements.txt``` file.
2. **Add your credentials.** In the ```config.json``` file, enter your Spotify account authorization credentials in the ```AUTHENTIFY``` object. Sniffer uses Spotify's *Client Credentials Flow* API. (If you don't know what this is, [see here](https://developer.spotify.com/documentation/general/guides/authorization-guide/).)
3. **Set up your Gmail token.** You'll also need a gmail address to send/receive each update. Run the ```gmail-token.py``` script (written primarily by Google) to generate pickled Gmail API access credentials. Then, in the ```sniffer_run.py``` file, enter your sending-from and sending-to addresses:

```
EMAIL_FROM = 'XXX@gmail.com'
EMAIL_TO = 'XXX@gmail.com'
```

4. **Start adding artists.** Sniffer uses Spotify's *Client Credentials Flow* API, which gives us a considerably higher API rate limit than its other methods; unfortunately, this track does not allow us to access user accounts. Thus, you will need to load Sniffer with a selection of your favorite artists to check up on before you get started. Spotify artists each have a unique 22-character alphanumeric ID; place your artist IDs in the ```spotify_artists.txt``` file, separated by commas. (For convenience, I have provided a text file with some 8,700 Spotify artist IDs (```bands.tsv```) that I ripped from Wikidata.)
5. **Run ```sniffer_run.py```.** The script will create a JSON file that will store the latest releases of your artists in ```spotify_artists.txt```.
6. **Run ```sniffer_run.py``` as often as you want.** Get updates about new music.

You can always add more artists to ```spotify_artists.txt```, even after running the setup script. Each time you run ```sniffer_run.py```, new artist IDs will be added to your local JSON data and will be checked in your next Sniffer run.

## Slowstart Documentation Guide for Code Newbies
[Now available!](https://github.com/scottythered/spotify-sniffer/blob/master/slow-start-guide.md)

## License
Copyright (c) 2019 Scotty Carlson
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
