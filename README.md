<center><h1>Synced Lyric on TouchBar</h1></center>
<br></br>

[![Build Status](https://travis-ci.com/ChenghaoMou/touchbar-lyric.svg?branch=master)](https://travis-ci.com/ChenghaoMou/touchbar-lyric)

Show synced lyric in the touch-bar with BetterTouchTool and NetEase APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

## Features

1. Netease music web apis for **synced lyrics**;
2. cachier to **cache** function calls and reduce the need to call webapis;
3. Apple script for Spotify & **Music** background track information;
4. Support for **English/Chinese**;

Note: I am using Catalina, so 'iTunes' in previous macOS is now 'Music'. You can change the 'Music' back to 'iTunes'.

## Instruction

### 1. Denpendencies

It is advised to set up a new python environment with 3.6+.

```shell
pip install touchbar_lyric
```

### 2. Configuration in BetterTouchTool

Same as Kashi:

1. Copy&paste the content in `lyric.json` in _Meun Bar > Touch Bar_;
2. Change the python path to your own python path in the script area;
3. Optional: You can use pubproxy api to remedy netease's anti-crawler mechanism.

```shell
${PYTHONPATH} -m touchbar_lyric --api ${PUBPROXY_API}
```

## Preview

![Preview](./preview1.png)
![Preview](./preview2.png)

Note: In case there is no synced lyric, each sentence will be displayed at an evenly time interval.
