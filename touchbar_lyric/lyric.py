import os
import re
import binascii
import base64
import json
import copy
import requests
from Crypto.Cipher import AES
import requests
import osascript
import hashlib
import time
import math
import requests
from cachier import cachier
import datetime
from typing import *
import pinyin
from hanziconv import HanziConv


class NeteaseRequest:

    session = requests.Session()
    session.headers.update({
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Charset": "UTF-8,*;q=0.5",
        "Accept-Encoding": "gzip,deflate,sdch",
        "Accept-Language": "en-US,en;q=0.8",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
        "referer": "http://music.163.com/",
    })

    @classmethod
    def encode_netease_data(cls, data) -> str:
        data = json.dumps(data)
        key = binascii.unhexlify("7246674226682325323F5E6544673A51")
        encryptor = AES.new(key, AES.MODE_ECB)
        pad = 16 - len(data) % 16
        fix = chr(pad) * pad
        byte_data = (data + fix).encode("utf-8")
        return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

    @classmethod
    def encrypted_request(cls, data) -> dict:
        MODULUS = (
            "00e0b509f6259df8642dbc35662901477df22677ec152b5ff68ace615bb7"
            "b725152b3ab17a876aea8a5aa76d2e417629ec4ee341f56135fccf695280"
            "104e0312ecbda92557c93870114af6c9d05c4f7f0c3685b7a46bee255932"
            "575cce10b424d813cfe4875d3e82047b97ddef52741d546b8e289dc6935b"
            "3ece0462db0a22b8e7"
        )
        PUBKEY = "010001"
        NONCE = b"0CoJUm6Qyw8W8jud"
        data = json.dumps(data).encode("utf-8")
        secret = cls.create_key(16)
        params = cls.aes(cls.aes(data, NONCE), secret)
        encseckey = cls.rsa(secret, PUBKEY, MODULUS)
        return {"params": params, "encSecKey": encseckey}

    @classmethod
    def aes(cls, text, key):
        pad = 16 - len(text) % 16
        text = text + bytearray([pad] * pad)
        encryptor = AES.new(key, 2, b"0102030405060708")
        ciphertext = encryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    @classmethod
    def rsa(cls, text, pubkey, modulus):
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
        return format(rs, "x").zfill(256)

    @classmethod
    def create_key(cls, size):
        return binascii.hexlify(os.urandom(size))[:16]

    @classmethod
    def request(cls, url, method="POST", data=None):
        if method == "GET":
            resp = cls.session.get(url, params=data, timeout=7)
        else:
            resp = cls.session.post(url, data=data, timeout=7)
        if resp.status_code != requests.codes.ok:
            raise RequestError(resp.text)
        if not resp.text:
            raise ResponseError("No response data.")
        return resp.json()


class NeteaseSong:

    def __init__(self, id: int, title: str, artists: str):
        self.id = id
        self.title = title
        self.artists = artists


@cachier(stale_after=datetime.timedelta(days=1))
def get_lyric(id) -> str:
    row_data = {"csrf_token": "", "id": id, "lv": -1, "tv": -1}
    data = NeteaseRequest.encrypted_request(row_data)

    return NeteaseRequest.request(
        "https://music.163.com/weapi/song/lyric", method="POST", data=data
    ).get("lrc", {}).get("lyric", "")


@cachier(stale_after=datetime.timedelta(days=3))
def search(title, artists) -> List[NeteaseSong]:

    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": title, "type": 1, "offset": 0, "limit": 30},
    }
    data = {"eparams": NeteaseRequest.encode_netease_data(eparams)}

    songs_list = []
    res_data = (
        NeteaseRequest.request(
            "http://music.163.com/api/linux/forward", method="POST", data=data
        )
        .get("result", {})
        .get("songs", {})
    )
    artists = artists.replace(' ', '').replace(',', '').replace('-', '').lower()
    artists = pinyin.get(artists, delimiter='', format='strip')
    backup = []

    for item in res_data:

        singers = [pinyin.get(s.get("name", "").replace(' ', ''), delimiter='', format='strip').lower() for s in item.get("ar", [])]
        found = False
        # print(singers, artists)
        for singer in singers:
            if singer in artists:
                found = True

        song = NeteaseSong(
            id=item.get("id", ""),
            title=item.get("name", ""),
            artists="".join(singers),
        )
        if found:
            songs_list.append(song)
        else:
            backup.append(song)
    # print(songs_list, backup)
    return songs_list if songs_list else backup[:1]


def get_lyrics(songs: List[NeteaseSong]) -> List:
    for song in songs:
        lyric = get_lyric(song.id)
        if lyric is not None:
            return lyric


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

        title = HanziConv.toSimplified(title)

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

    if status != 'playing':
        return
    else:

        songs = search(title, artists)
        lyric = get_lyrics(songs)
        words = parse(lyric, position, duration)
        if words is not None:
            print(words)
        elif words == '':
            print('~')
        elif words is None:
            print(f'{application.title()} -- {title} -- {artists}')
        return


if __name__ == "__main__":
    # search.clear_cache()
    main()
