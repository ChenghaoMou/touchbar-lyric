<center><h1>Synced Lyric on TouchBar</h1></center>
<br></br>

[![Codacy Badge](https://api.codacy.com/project/badge/Grade/77de523131f9441997db18c608b3c54e)](https://app.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Grade_Dashboard) [![Build Status](https://travis-ci.com/ChenghaoMou/touchbar-lyric.svg?branch=master)](https://travis-ci.com/ChenghaoMou/touchbar-lyric) [![Codacy Badge](https://app.codacy.com/project/badge/Coverage/aadeca6117a14aa6b655e21d5bbc09ea)](https://www.codacy.com/manual/mouchenghao/touchbar-lyric?utm_source=github.com&utm_medium=referral&utm_content=ChenghaoMou/touchbar-lyric&utm_campaign=Badge_Coverage)

Show synced lyric in the touch-bar with BetterTouchTool and NetEase APIs. Based on the idea of [Kashi](https://community.folivora.ai/t/kashi-show-current-song-lyrics-on-touch-bar-spotify-itunes-youtube/6301).

## Features

1.  Netease music web apis for **synced lyrics**;
2.  cachier to **cache** function calls and reduce the need to call webapis;
3.  Apple script for Spotify & iTunes/Music background track information;
4.  Support for **English/Chinese(Simplified)**;

## Style
It follows the following style to display each line of the lyric:
```
[Title/Author(s)] Lyric
```
See Preview for more.

Note: Netease music itself is not supported as it does not support apple script now.

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

```shell
${PYTHONPATH} -m touchbar_lyric --app Music
```

or use Spotify(default)

```shell
${PYTHONPATH} -m touchbar_lyric --app Spotify
```

## Preview

![Preview](./preview1.png)
![Preview](./preview2.png)

# 中文指南

## 背景知识

-   脚本运行需要 BTT + Python3.6+。
-   仅支持系统自带的 Music 和 Spotify，推荐使用 Spotify。

## Python 设置

-   检查 macOS 系统自带的 Python3 ，在系统自带的 Terminal 应用中输入以下命令

```bash
whereis python3
```

\*返回输出的路径信息后面会使用

-   安装 `pip`

```bash
curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py
python3 get-pip.py
```

-   安装 `touchbar-lyric`

```bash
pip3 install touchbar_lyric
```

## BTT设置

-   复制 `lyric.json` 里面的内容，在BTT的Touch Bar 配置界面直接粘贴
-   在右侧脚本区域， 把 `/Users/chenghaomou/Anaconda/bin/python` 换成第一步中的路径
-   在 Spotify/Music 运行时，应该出现歌词挂件

## 预览
歌词信息按照 `[歌曲名/演唱者] 歌词` 格式，具体效果如图所示：

![Preview](./preview1.png)
![Preview](./preview2.png)
