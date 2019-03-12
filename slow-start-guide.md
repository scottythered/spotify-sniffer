# Slowstart Guide for Code Newbies
This guide tries to take it slow and easy for people who want to use Sniffer but haven't done much of this coding or scripting stuff.

## Set Up and Yak Shaving

1. **Do you have Python?**

Python is a programming language you'll need to run Sniffer. Check to see if Python is installed by going into your command line interface (or CLI; on Mac, this is 'Terminal' and on Windows, this is 'Command Prompt', or *cmd*), typing in ```python --version```, and hitting enter. The CLI will either return a program version or an error message if it's not installed.

```
C:\Windows\System32> python --version
Python 3.5.2
```

Note: You'll need Python 3.6 or later to run Sniffer, and in some systems, this is installed as ```python3```, so also try:

```
scottythered:~$ python3 --version
Python 3.6.6
```

If you don't have Python 3.6, there's lots of resources out there if you need to install it on your machine.

2. **Do you have a Spotify account and API credentials?**

To have Sniffer fetch data from Spotify, you'll need authorization to use their application programming interface (API). In layman's terms, this means getting permission to only access their datapoints that do not touch user information. Yes, this means we can't grab any information from our personal accounts, but this also means we can get more data from Spotify without having our transactions throttled.

To do this, you'll need a **Client ID** and a **Secret Key**. Visit [https://developer.spotify.com/dashboard/](https://developer.spotify.com/dashboard/) and click *Create Client ID*. Give your client any name and description you want, but select *I Don't Know* for "What are you building?" Then tick the next boxes confirming *CREATE A NON-COMMERCIAL APP*. You'll be taken to a detail page for your new Sniffer-related app, which will have your Client ID and a button to show your Client Secret

Once you have these, go back to your repo folder, open ```config.json```, and enter these credentials in the ```AUTHENTIFY``` object.

3. **Add Your Email Account**

You'll need an email address to send/receive each update. In the config file, enter your sending-from address (```from_addr```), sending-to address (```to_addr```), email account login (```em_login```), password (```em_password```), and your SMTP email server (```serv_loc```).

Gmail's SMTP server is in ```serv_loc``` by default; if you use a different email service, have a look at [this link](https://serversmtp.com/what-is-my-smtp/) to find out what it is.

Note: if you use Gmail and your account is fairly secure, you'll probably get an error response saying that you need to log in to continue. You can circumvent this by visiting [Account Security Settings](https://www.google.com/settings/security/lesssecureapps) and enabling *Access for Less Secure Apps*. This will allow you to use the Gmail SMTP for our script; it also has the side effect of slightly making your account less secure. **I strongly advise you to create a secondary Gmail account used solely to send Sniffer emails!**

4. **Find Artists You Want to Track**

Because our API usage does not allow us to access user accounts, you will need to pre-load Sniffer with a selection of your favorite artists before you run the script.

Spotify artists each have a unique 22-character alphanumeric ID; you find this by looking at the Spotify web player URL for an artist. For example, the Spotify ID of Guided By Voices is: ```https://open.spotify.com/artist/4oV5EVJ0XFWsJKoOvdRPvl ---> 4oV5EVJ0XFWsJKoOvdRPvl```

Place your artist IDs in the ```spotify_artists.txt``` file, separated by commas. I have preloaded some of my favorites as an example:

```
2Sp19cOHSqAUlE64hekARW, 6AXXiSvB6R7MpYsXW1inOx, 1DFr97A9HnbV3SKTJFu62M, 3r9TXuXfOUxXjgYgAR0fP8, 2DaxqgrOhkeH0fpeiQq2f4, 2P560DaOMNDUACoH8ZhOCR
```

Looking up a hundred of your favorite artists does sound like a labrious task, so for convenience, I have provided a text file with about 8,700 Spotify artist IDs (```bands.tsv```) ripped from Wikidata.

## Let's Punch it

5. **Run the Setup Script**

While in Sniffer's directory, run:

```
python3 sniffer-setup.py
```

This setup script needs only be run once; it creates a JSON file in the directory that will store the latest releases of your artists in ```spotify_artists.txt```.

6. **Run the Regular Script**

Run ```sniffer.py``` as often as you want to get updates about new music.

### "What if I Want to Add More Artists After Running the Setup Script?"

You totally can! The regular script checks for new additions each time (though note that you won't get *new* notifications from these artists until the next time you run the script).

## Scheduling Sniffer

Instead of running the script manually, you can use scheduling software to run it automatically.

### Mac & Unix/Linux

**Cron** can be used on Unix-based machine to set up a regular process. You can access it by executing ```crontab -e``` in your CLI.

This sample cron job will run at 6 am every morning, provided the computer is on and running:

```
0 6 * * * /usr/bin/python3 /path/to/your/directory/sniffer.py
```

### Windows

Visit [this site](https://docs.microsoft.com/en-us/windows/desktop/taskschd/about-the-task-scheduler) for information on **Task Scheduler** in Windows 10.
