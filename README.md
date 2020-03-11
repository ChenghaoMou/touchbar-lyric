<center><h1>Synced Lyric on TouchBar</h1></center>
<br></br>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77de523131f9441997db18c608b3c54e)](https://app.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Grade_Dashboard)
[![Build Status](https://travis-ci.com/ChenghaoMou/touchbar-lyric.svg?branch=master)](https://travis-ci.com/ChenghaoMou/touchbar-lyric)

Show synced lyric in the touch-bar with BetterTouchTool and NetEase APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

\#Note:
Only tested with Catalina. If you are on Mojave, please clone the repo and change the the following code:

edit `touchbar_lyric/__init__.py`
change the code in `get_info` (basically change `Music` to `iTunes`)

```python
else if application "Music" is running then
    tell application "Music"
        set currentInfo to {"Music", artist of current track, "###", name of current track, player position, player state, duration of current track}
    end tell
end if
```

to

```python
else if application "iTunes" is running then
    tell application "iTunes"
        set currentInfo to {"iTunes", artist of current track, "###", name of current track, player position, player state, duration of current track}
    end tell
end if
```

the execute the following command in the directory of the repo:

```bash
pip install --editable .
```

## Features

1.  Netease music web apis for **synced lyrics**;
2.  cachier to **cache** function calls and reduce the need to call webapis;
3.  Apple script for Spotify & iTunes/Music background track information;
4.  Support for **English/Chinese**;

## Instruction

### 1. Denpendencies

First check your python version, which should be 3.6+. All commands should be executed in your terminal.

```shell
python3 --version
```

#### pip

```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
```

```Shell
python3 get-pip.py
```

You might want to restart your terminal.

```shell
pip3 install touchbar_lyric
```

### Python Path

Take a note for the python3 path. We will refer it as `${PYTHONPATH}`

```shell
whereis python3
```

### 2. Configuration in BetterTouchTool

Same as Kashi:

1.  Copy&paste the content in `lyric.json` in _Meun Bar > Touch Bar_;
2.  Change the python path `/Users/chenghaomou/Anaconda/bin/python` to your own python path in the script area;
3.  Optional: You can use pubproxy api to remedy netease's anti-crawler mechanism.

```shell
${PYTHONPATH} -m touchbar_lyric --api ${PUBPROXY_API}
```

Where `--api ${PUBPROXY_API}` is optional.

## Preview

![Preview](./preview1.png)
![Preview](./preview2.png)

Note: In case there is no synced lyric, each sentence will be displayed at an evenly time interval.
