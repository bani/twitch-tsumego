# Twitch plays Tsumego

Twitch bot to play Tsumegos from [Black to Play](https://blacktoplay.com/)

### Running the bot

You can install the main libraries to run this project with
`pip install -r requirements.txt`

You'll need the following additional files:

#### .venv

```
TMI_TOKEN=oauth:abc
CLIENT_ID=abc
BOT_NICK=abc
BOT_PREFIX=!
CHANNEL=abc
```

#### points.py

Initialize it with:
```
p = {}
```
After streaming, you can copy the last entry from the terminal to this file.

When ready, run the bot with `python twitch.py`
