# Environment Setup
Download [Livesplit](https://github.com/LiveSplit/LiveSplit/releases/tag/1.8.25) & Extract to a new folder

~~Download [Livesplit Server](https://github.com/LiveSplit/LiveSplit.Server/releases/tag/1.8.19) & Extract into the "LiveSplit\Components" directory~~

Download [OBS Studio](https://obsproject.com/download)

Download OBS Studio Websocket:

> [For OBS Studio version < 28.0](https://github.com/obsproject/obs-websocket/releases/tag/5.0.1)

> [For OBS Studio version >= 28.0](https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat)
 
For windows, you want the Windows-Installer.exe file

Run the installer and extract to same location as obsstudio (ex. program files/OBSStudio)

Run OBS-Studio now, and it should pop up with a webserver first time use notification. Do not set a password.
For OBS-studio version >= 28.0, go into OBS-studio -> tools -> web sockets server settings (4.x compat) and turn off authentication.
Go into OBS-studio -> tools -> obs-websockets settings and turn off authentication.

Download and Install [python3](https://www.python.org/downloads/)

And the python package manager, pip, by running the following commands:
```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python get-pip.py
pip --version
```

Now install the OBS python interface using
```bash
pip install obs-websocket-py
```

Install other dependencies:
```bash
# pip install pynput
pip install discord.py
pip install livesplit
pip install pandas
```

Go to resources/Billyfont.ttf and install the font (open -> top left, or right click -> install)

To import the billy relay race scene collection, go into OBS, click Scene Collection -> import, and choose the BillyRelayRace.json file in resources. You will probably get many warnings about missing resources, in which case you should 

Open Livesplit, right click -> Open splits -> from file -> resources/BillyRelayLivesplitSplits.lss
Right click livesplit -> Open Layout -> from file -> resources/BillyRelayLivesplitLayout.lsl

In obs, change scene transition to cut(bottom right)

Add a file containing the server token for your server in resources as token.txt. Exeloar can provide this for the billy speedrunning server.

Lastly, you may need to switch the fonts used on a few things. Check out the OBS layout to make sure the billy font is being used for each, and also make sure the timer looks correct too.

# Confirm Successful Setup

To confirm the complicated and annoying websockets have successfully been set up, run the following commands:
```bash
python3 .\obsconnectiontest.py
# python3 .\livesplitconnectiontest.py
```

### Startup

Open Livesplit & OBS

run 
```bash
python3 .\relaybot.py
```
in the BillyRelayBot folder.

This should activate the bot, who should say "bot initialized" in the discord relay race discussion chat.

Now wait just small bit until python says:
> INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 11653a9388c2294d27dfe5a92018d06e).

Now join the Billy Relay Commentary VC, and the stream should be ready to go.