import re
import requests
import json
import osascript
import hashlib
from bs4 import BeautifulSoup
from io import open
import time
import math
import requests
from cachier import cachier
import datetime


def get_info():
    code, res, error = osascript.run('''
            on run
                if application "Spotify" is running then
                    tell application "Spotify"
                        set currentInfo to {"Spotify", artist of current track, "###", name of current track, player position, player state, duration of current track}
                    end tell
                else if application "Music" is running then
                    tell application "Music"
                        set currentInfo to {"Music", artist of current track, "###", name of current track, player position, player state, duration of current track}
                    end tell
                end if
                return currentInfo
            end run
    ''', background=False)
    # print(res)
    if res:
        info = res.split('###')
        application, *artists = map(lambda x: x.strip(), info[0].strip(' ,').split(','))
        artists = ','.join(artists)
        *title, position, status, duration = map(lambda x: x.strip(), info[1].strip(' ,').split(','))
        title = ','.join(title)
        if float(duration) <= 1200:
            duration = float(duration)
            position = float(position)
        else:
            duration = float(duration) / 3600
            position = float(position)

        return application, artists, title, position, status, duration
    else:
        return None


def parse(lyric, position, duration):
    if lyric is None:
        return
    # print(position)
    lines = [line for line in lyric.split('\n') if line.strip()]

    def parse_line(line):

        if not re.findall('\[([0-9]+):([0-9])+\.([0-9]+)\]', line):
            return 0, line
        # print(re.findall('\[([0-9]+):([0-9])+\.([0-9]+)\]', line))
        minute, second, _ = re.findall('\[([0-9]+):([0-9]+)\.([0-9]+)\]', line)[0]
        curr = int(minute) * 60 + int(second)
        words = re.sub('\[.*?\]', '', line)
        # print(minute, second)
        return curr, words

    lines = list(map(parse_line, lines))

    if all(line[0] == 0 for line in lines):
        _, words = lines[min(int(len(lines) * position / duration), len(lines)-1)]
        return '❌ ' + words

    starts = [0] + [line[0] for line in lines][:-1]
    ends = [line[0] for line in lines]
    lines = [line[-1] for line in lines]

    for start, end, words in zip(starts, ends, [""] + lines):
        if start <= position <= end:
            return words


def main():

    res = get_info()
    if res is None:
        print('404 No lyric found')
        return
    else:
        application, artists, title, position, status, duration = res

    if status != 'playing':   # Return nothing if player is paused
        return
    else:

        ids = get_id(title, artists)
        lyric = get_lyrics(ids)
        words = parse(lyric, position, duration)
        if words is not None:
            print(words)
        elif words == '':
            print('~')
        elif words is None:
            print(f'{application.title()} -- {title} -- {artists}')
        return


@cachier(stale_after=datetime.timedelta(days=3))
def get_lyric(id):
    url = f"http://music.163.com/api/song/lyric?m&id={id}&lv=-1&kv=1&tv=1"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    data = r.json()

    if 'lrc' in data:
        return data['lrc']['lyric']
    else:
        return None

# @cachier(stale_after=datetime.timedelta(days=3))


def get_lyrics(ids):

    for id in ids:
        lyric = get_lyric(id)
        if lyric:
            return lyric
    return None


@cachier(stale_after=datetime.timedelta(days=3))
def get_id(name, artists):
    url = f"https://music.aityp.com/search?keywords={name}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    r = requests.get(url, headers=headers)
    data = r.json()
    ids = []
    if 'songs' in data['result']:
        for song in data['result']['songs']:
            if 'artists' in song:
                # print(song)
                name = re.findall('([a-z A-Z]+)', song['artists'][0]['name'])
                if name:
                    name = name[0]
                    name = name.replace(' ', '').lower()
                else:
                    continue

                if name in artists.replace(' ', '').replace(',', '').replace('-', '').lower():
                    ids.append(song['id'])
    return ids


if __name__ == "__main__":
    main()
    # print(search_song_by_name('Merry Christmas'))
    # get_lyric(409830420)
    # ids = get_id('My hert will go on')
    # lyric = get_lyric(ids)
    # print(lyric)
