# Twitch plays Tsumego

Twitch bot to play Tsumegos from [Black to Play](https://blacktoplay.com/)

### Set up

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

#### leaderboard.p

This is the pickle file with the players and points. You can initialize it with:
```
import pickle
p = {}
pickle.dump( p, open( "leaderboard.p", "wb" ) )
```

### Execute

When ready, run the bot with `python twitch.py`
