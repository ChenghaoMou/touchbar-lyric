<center><h1>Synced Lyric on TouchBar</h1></center>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77de523131f9441997db18c608b3c54e)](https://app.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Grade_Dashboard) [![Build Status](https://travis-ci.com/ChenghaoMou/touchbar-lyric.svg?branch=master)](https://travis-ci.com/ChenghaoMou/touchbar-lyric) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/aadeca6117a14aa6b655e21d5bbc09ea)](https://www.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Coverage) [![PyPI version](https://badge.fury.io/py/touchbar-lyric.svg)](https://badge.fury.io/py/touchbar-lyric)

Show synced lyric in the touch-bar with BetterTouchTool and NetEase/QQ Music APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

![Preview](./lyric_chinese.png)
![Preview](./lyric_english.png)

## Features

-   **Synced lyrics** from QQ Music and NetEase Music APIs;
-   Support **Spotify** (Recommended) & **Music** (Only songs in your playlists);
-   Support for **English/Spanish/Chinese(Simplified/Traditional)/Japanese** and more;

## Instruction

**If you are not familiar with command line, python ecosystem or having problems understanding this tutorial, find a friend to help you. Issues/DMs are not actively monitored for this project.**

### 1. Installation
```shell
pip3 install touchbar_lyric --upgrade
```

### 2. Configuration in BetterTouchTool

Same as Kashi:

1.  Copy&paste the content in `lyric.json` in _Meun Bar > Touch Bar_;
2.  Change the python path `$PYTHONPATH` to your own python path in the script area;

```shell
$PYTHONPATH -m touchbar_lyric --app Music
```

or use Spotify(default)

```shell
$PYTHONPATH -m touchbar_lyric --app Spotify
```

Show Traditional Chinese lyrics

```shell
$PYTHONPATH -m touchbar_lyric --app Spotify --traditional
```

**Be careful with typing double hyphens in BTT. It automatically change it to an em slash. Use copy & paste instead!**