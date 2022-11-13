### Environment Setup
Download Livesplit [windows link](https://github.com/LiveSplit/LiveSplit/releases/download/1.8.23/LiveSplit_1.8.23.zip)
Extract to a new folder

Download Livesplit Server [windows link](https://github.com/LiveSplit/LiveSplit.Server/releases/download/1.8.19/LiveSplit.Server.zip)
Extract into the "LiveSplit\Components" directory

Download OBS Studio [windows link](https://cdn-fastly.obsproject.com/downloads/OBS-Studio-28.0.3-Full-Installer-x64.exe)

Download OBS Studio Websocket [windows link](https://github.com/obsproject/obs-websocket/releases/download/4.9.1-compat/obs-websocket-4.9.1-compat-Qt6-Windows-Installer.exe). Extract to same location as obs (program files/OBSStudio)

Download this OBS Studio Scene Collection [link]

Run OBS-Studio now, and it should pop up with a webserver first time use notification. Do not set a password.
Go into OBS-studio -> tools -> web sockets server settings (4.x compat) and turn off authentication.
Go into OBS-studio -> tools -> obs-websockets settings and turn off authentication.

Download and Install python3 [windows link](https://www.python.org/ftp/python/3.11.0/python-3.11.0rc1-amd64.exe)

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
pip install obs-scene-transporter
```

Go to resources/Billyfont.ttf and install the font (open -> top left, or right click -> install)

To import the billy relay race scene collection, run
```bash
obs-scene-transporter import BillyRelaySceneCollection.zip
```

Open Livesplit, right click -> Open splits -> from file -> resources/BillyRelayLivesplitSplits.lss
Right click livesplit -> Open Layout -> from file -> resources/BillyRelayLivesplitLayout.lsl

In obs, change scene transition to cut(bottom right)

### Confirm Successful Setup

To confirm the complicated and annoying websockets have successfully been set up, run the following commands:
```bash
python3 .\obsconnectiontest.py
python3 .\livesplitconnectiontest.py
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
    INFO     discord.gateway Shard ID None has connected to Gateway (Session ID: 11653a9388c2294d27dfe5a92018d06e).

Now join the Billy Relay Commentary VC, and the stream should be ready to go.