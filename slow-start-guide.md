# Slowstart Guide for Code Newbies
This guide tries to take it slow and easy for people who want to use Sniffer but haven't done much of this scripting stuff.

## 1. Do you have Python?

Python is a programming language you'll need to run Sniffer. Check to see if Python is installed by going into your command line interface (or CLI) -- on Mac, this is the Terminal app; on Windows, this is Command Prompt, which you can find by typing *cmd* into the task bar. Try typing ```python --version``` into your CLI and hitting enter. The CLI will either return a program version or an error message if it's not installed.

```
C:\Windows\System32> python --version
Python 3.5.2
```

Note: You'll need Python 3.6 or later to run Sniffer, and in some systems, this is installed as ```python3```, so also try:

```
bash:~$ python3 --version
Python 3.6.6
```

If you don't have Python 3.6, there's lots of resources out there if you need to install it on your machine.

## 2. Do you have a Spotify account and API credentials?

For Sniffer to fetch data from Spotify, you'll need authorization to use their application programming interface (API). In layman's terms, this means getting permission to access their data points that do not touch user information. Yes, this means we can't grab any information from our personal accounts, but this also means we can get more data from Spotify without having our transactions rate-limited, or throttled.

To do this, you'll need a **Client ID** and a **Secret Key**. Visit [https://developer.spotify.com/dashboard/](https://developer.spotify.com/dashboard/) and click *Create Client ID*. Give your client any name and description you want, but select *I Don't Know* for "What are you building?" Then tick the next boxes confirming *CREATE A NON-COMMERCIAL APP*. You'll be taken to a detail page for your new app, which will have your Client ID and a button to show your Client Secret.

Once you have these, go back to your repo folder, edit ```config.json```, and enter these credentials into the ```AUTHENTIFY``` object.

## 3. Setting Up Gmail

You'll also need a Gmail address to send each Sniffer update. In the config file, enter your sending-from and sending-to addresses in the ```MAILIFY``` object. Next, run the ```gmail-token.py``` script:

```
C:\Windows\System32> python gmail-token.py
```

This script was scrobbled from Google's own documentation; it generates Gmail API credentials so you can send email with your Gmail account. The script will open up a browser window and ask you to sign in -- be sure to use your mail-from address! Once you successfully sign in, the script will close down and save your Gmail credentials in a local file that Sniffer will access each time it runs.

Note: I strongly advise you to create a secondary Gmail account used solely to send Sniffer emails!

## 4. Find Artists You Want to Track

Because our API usage does not allow us to access user accounts, you will need to pre-load Sniffer with a selection of your favorite artists before you run the script. Spotify artists each have a unique 22-character alphanumeric ID; you find this by looking at the Spotify web player URL for an artist. For example, the Spotify ID of Guided By Voices is: ```https://open.spotify.com/artist/4oV5EVJ0XFWsJKoOvdRPvl ---> 4oV5EVJ0XFWsJKoOvdRPvl```

Place your artist IDs in the ```spotify_artists.txt``` file, separated by commas. I have preloaded some of my favorites as an example:

```
2Sp19cOHSqAUlE64hekARW, 6AXXiSvB6R7MpYsXW1inOx, 1DFr97A9HnbV3SKTJFu62M, 3r9TXuXfOUxXjgYgAR0fP8, 2DaxqgrOhkeH0fpeiQq2f4, 2P560DaOMNDUACoH8ZhOCR
```

Looking up a hundred of your favorite artists does sound like a laborious task, so for convenience, I have provided a text file with about 8,700 Spotify artist IDs (```bands.tsv```) ripped from Wikidata.

## 5. Run Sniffer

While in Sniffer's directory, run:

```
python3 sniffer_run.py
```

This creates a JSON file in the directory that will store the latest releases of the artists you put in ```spotify_artists.txt```. Run ```sniffer_run.py``` as often as you want to get updates about new music.

### "What if I Want to Add More Artists After Running the Script?"

You totally can! The script checks for new additions each time (though note that you won't get *new* notifications from these artists until the next time you run the script).

## 6. Scheduling Sniffer

Instead of running the script manually, you can use scheduling software to run it automatically.

### Mac & Unix/Linux

**Cron** can be used on Unix-based machine to set up a regular process. You can access it by executing ```crontab -e``` in your CLI.

This sample cron job will run at 6 am every morning, provided the computer is on and running:

```
0 6 * * * /usr/bin/python3 /path/to/your/directory/sniffer_run.py
```

### Windows

Visit [this site](https://docs.microsoft.com/en-us/windows/desktop/taskschd/about-the-task-scheduler) for information on **Task Scheduler** in Windows 10.
