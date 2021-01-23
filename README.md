<center><h1>Synced Lyric on TouchBar</h1></center>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77de523131f9441997db18c608b3c54e)](https://app.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Grade_Dashboard) [![Build Status](https://travis-ci.com/ChenghaoMou/touchbar-lyric.svg?branch=master)](https://travis-ci.com/ChenghaoMou/touchbar-lyric) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/aadeca6117a14aa6b655e21d5bbc09ea)](https://www.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Coverage) [![PyPI version](https://badge.fury.io/py/touchbar-lyric.svg)](https://badge.fury.io/py/touchbar-lyric)

Show synced lyric in the touch-bar with BetterTouchTool and NetEase/QQ Music APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

## Preview

![Preview](./preview1.png)
![Preview](./preview2.png)

## Features

-   **Synced lyrics**;
-   Support **Spotify** (Recommend) & **Music(Only your playlists)**;
-   Support for **English/Spanish/Chinese(Simplified/Traditional)/Japanese** and more;
-   Support background color, font color, and font size configuration. And `rainbow` mode!

## Instruction

### 1. Dependencies

First check your macOS python (the programming language this plugin is written in) version, which should be 3.7+. All commands should be executed in your terminal.

```shell
python3 --version
```

#### pip

pip is a package management tool for python.

```shell
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

You might want to restart your terminal. Then we can install this plugin by

```shell
pip3 install touchbar_lyric --upgrade
```

### Python Path

Take a note for the python3 path. We will refer it as `${PYTHONPATH}`

```shell
which python3
```

### 2. Configuration in BetterTouchTool

Same as Kashi:

1.  Copy&paste the content in `lyric.json` in _Meun Bar > Touch Bar_;
2.  Change the python path `/Users/chenghaomou/Anaconda/bin/python` to your own python path `${PYTHONPATH}` in the script area;
3.  Change any parameters as you like: `fc`(font color in RGB), `bg`(background color in RGB), and `fs`(font size)

```shell
${PYTHONPATH} -m touchbar_lyric --app Music
```

or use Spotify(default)

```shell
${PYTHONPATH} -m touchbar_lyric --app Spotify
```

Show Traditional Chinese lyrics

```shell
${PYTHONPATH} -m touchbar_lyric --app Spotify --traditional
```

Use accurate mode to skip less ideal matches

```shell
${PYTHONPATH} -m touchbar_lyric --accurate
```

You can also add `--rainbow` flag at the end of the command to have a nice rainbow specturm as the background.

**Be careful with typing double hyphens in BTT. It automatically change it to em slash. Use copy & paste instead!**

# 中文指南

## 背景知识

-   脚本运行需要 BTT + Python3.7+。
-   仅支持系统自带的 Music 和 Spotify，推荐使用 Spotify。

## Python 设置

-   检查 macOS 系统自带的 Python3 ，在系统自带的 Terminal 应用中输入以下命令

```bash
which python3
```

\*返回输出的路径信息后面会使用

-   安装 `pip`

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

-   安装 `touchbar-lyric`

```bash
pip3 install touchbar_lyric --upgrade
```

## BTT设置

-   复制 `lyric.json` 里面的内容，在BTT的Touch Bar 配置界面**直接**粘贴
-   在右侧脚本区域， 把 `/Users/chenghaomou/Anaconda/bin/python` 换成第一步中的路径
-   可以在命令最后添加 `--rainbow` 使用彩虹渐变背景
-   可以在命令最后添加 `--traditional` 显示繁体歌词信息
-   可以在命令最后添加 `--accurate` 忽略匹配度较差的歌词
-   在 Spotify/Music 运行时，应该出现歌词挂件
-   可以更改参数 `fc`(RGB 字体颜色), `bg`(RGB 背景颜色), 和 `fs`(字体大小)
