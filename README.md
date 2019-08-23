# touchbar-lyric

Show synced lyric in the touch-bar with BetterTouchTool and NetEase APIs.

## Implementation

I used netease music web apis for synced lyrics and cachier to reduce the need to crawl the webpage. Apple script for Spotify & **Music** information retrieval.

I am using Catalina, so 'iTunes' in previous macOS is now 'Music'. You can change the 'Music' back to 'iTunes'.

## Instruction

### 1. Denpendencies

```shell
pip install requests osascript bs4 cachier
```

### 2. Configuration in BetterTouchTool

![Basic Configuration](./config.jpg)
![Basic Configuration](./config2.jpg)
![Basic Configuration](./config3.jpg)

## Preview

![Preview](./preview1.png)
![Preview](./preview2.png)

Note: In case there is no synced lyric, each sentence will be displayed at an evenly time interval.
