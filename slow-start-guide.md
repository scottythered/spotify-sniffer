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

To do this, you'll need a **Client ID** and a **Secret Key**. Visit (https://developer.spotify.com/dashboard/)[https://developer.spotify.com/dashboard/] and click *Create Client ID*. Give your client any name and description you want, but select *I Don't Know* for "What are you building?" Then tick the next boxes confirming *CREATE A NON-COMMERCIAL APP*. You'll be taken to a detail page for your new Sniffer-related app, which will have your Client ID and a button to show your Client Secret

Once you have these, go back to your repo folder, open ```config.json```, and enter these credentials in the ```AUTHENTIFY``` object.

3. **Add Your Email Account**

You'll need an email address to send/receive each update. In the config file, enter your sending-from address (```from_addr```), sending-to address (```to_addr```), email account login (```em_login```), password (```em_password```), and your SMTP email server (```serv_loc```).

Gmail's SMTP server is in ```serv_loc``` by default; if you use a different email service, have a look at (this link)[https://serversmtp.com/what-is-my-smtp/] to find out what it is.
