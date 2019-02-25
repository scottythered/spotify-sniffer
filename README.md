# Spotify Sniffer
Spotify Sniffer is a lightweight script that sniffs out new releases on Spotify.

## What For?
Each time the script is run, Sniffer uses Spotify's web API to check up on the latest album, single, and complilation released by any artist you ask for. If something new has been released since you last ran it, you'll get an email with links to the new music. Use it with crontab or some other scheduling software to sniff out new music on a regular basis.

## Requirements
Sniffer was written for Python 3.6+. The only library used that isn't a part of the standard library is **Requests**.

You'll also need an email account, a Spotify account with authorization credentials (see below), and a passing interest in music.

## Quickstart
1. **Download/clone this repo.** Make sure you have Requests installed and Python 3.6+.
2. **Add your credentials.** In the ```config.json``` file, enter your Spotify account authorization credentials in the ```AUTHENTIFY``` object. Sniffer uses Spotify's *Client Credentials Flow* API. (If you don't know what this is, [see here](https://developer.spotify.com/documentation/general/guides/authorization-guide/).)
3. **Add your email account.** You'll also need an email address to send/receive each update; in the ```config``` file, enter your sending-from address (```from_addr```), sending-to address (```to_addr```), email account login (```em_login```), password (```em_password```), and your SMTP email server (```serv_loc```). (Gmail's SMTP server is there by default; if you use a different email service, use [this link](https://serversmtp.com/what-is-my-smtp/) to find out what it is.)
4. **Start adding artists.** Sniffer uses Spotify's *Client Credentials Flow* API, which gives us a considerably higher API rate limit than its other methods; unfortunately, this track does not allow us to access user accounts. Thus, you will need to load Sniffer with a selection of your favorite artists to check up on before you get started. Spotify artists each have a unique 22-character alphanumeric ID; place your artist IDs in the ```spotify_artists.txt``` file, separated by commas. (For convenience, I have provided a text file with some 8,700 Spotify artist IDs (```bands.tsv```) that I ripped from Wikidata.)
5. **Run ```sniffer-setup.py```.** The setup script needs only be run once; it creates a JSON file that will store the latest releases of your artists in ```spotify_artists.txt```.
6. **Run ```sniffer.py``` as often as you want and get updates about new music.**

You can always add more artists to ```spotify_artists.txt```, even after running the setup script. Each time you run ```sniffer.py```, new artist IDs will be added to your local JSON data and will be checked in your next Sniffer run.
