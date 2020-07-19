#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-10 10:54:37
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

"""Touchbar lyric widget for BTT."""

import base64
import binascii
import datetime
import string
import json
import os
import regex as re
from typing import Any, Dict, List, Tuple

import requests
from Crypto.Cipher import AES

import osascript
import pinyin
from cachier import cachier
from hanziconv import HanziConv
from loguru import logger

# Translate English names into pinyin
translation: Dict[str, str] = {
    "Bella Yao": "贝拉姚",
    "A-fu": "阿福",
    "Alan Dawa Dolma": "阿兰达瓦卓玛",
    "A-Lin": "黄丽玲",
    "A-mei": "杜诗梅",
    "Priscilla Chan": "陈慧娴",
    "Angela Chang": "张韶涵",
    "Deserts Chang": "沙漠常",
    "Cheer Chen": "陈绮贞",
    "Kelly Chen": "陈慧琳",
    "Sammi Cheng": "郑秀文",
    "Maggie Chiang": "江美琪",
    "Vivian Chow": "周慧敏",
    "Tanya Chua": "蔡健雅",
    "Gillian Chung": "钟欣潼",
    "Ding Dang": "丁当",
    "Christine Fan": "范玮琪",
    "Mavis Fan": "范晓萱",
    "Mavis Hee": "许美静",
    "Denise Ho": "何韵诗",
    "Elva Hsiao": "萧亚轩",
    "Jeannie Hsieh": "谢金燕",
    "Winnie Hsin": "辛晓琪",
    "Evonne Hsu": "许慧欣",
    "Lala Hsu": "徐佳莹",
    "Valen Hsu": "许茹芸",
    "Vivian Hsu": "徐若瑄",
    "Amber Kuo": "郭采洁",
    "Sandy Lam": "林忆莲",
    "Coco Lee": "李玟",
    "Fish Leong": "梁静茹",
    "Gigi Leung": "梁咏琪",
    "Li Yuchun": "李宇春",
    "Rene Liu": "刘若英",
    "Liu Shishi": "刘诗诗",
    "Candy Lo": "卢巧音",
    "Karen Mok": "莫文蔚",
    "Anita Mui": "梅艳芳",
    "Na Ying": "那 英",
    "Kary Ng": "吴雨霏",
    "One-Fang": "一方",
    "Cass Phang": "彭羚",
    "Wanting Qu": "想屈",
    "Sa Dingding": "萨顶顶",
    "Fiona Sit": "薛凯琪",
    "Tarcy Su": "苏慧伦",
    "Stefanie Sun": "孙燕姿",
    "Penny Tai": "戴佩妮",
    "G.E.M. Tang": "邓紫棋",
    "Stephy Tang": "邓丽欣",
    "Teresa Teng": "邓丽君",
    "Hebe Tien": "田馥甄",
    "Tsai Chin": "蔡琴",
    "Jolin Tsai": "蔡依林",
    "Kay Tse": "谢安琪",
    "Cyndi Wang": "王心凌",
    "Joanna Wang": "王若琳",
    "Landy Wen": "温岚",
    "Meng Jia": "孟佳",
    "Faye Wong": "王菲",
    "Ivana Wong": "王菀之",
    "Xidan Girl": "西单女孩",
    "Faith Yang": "杨乃文",
    "Rainie Yang": "杨丞琳",
    "Sally Yeh": "叶倩文",
    "Miriam Yeung": "杨千嬅",
    "Joey Yung": "容祖儿",
    "Jane Zhang": "张靓颖",
    "Jana Chen": "陈嘉娜",
    "Zhao Wei": "赵薇",
    "Fong Fei Fei": "方飞飞",
    "Yangwei Linghua": "阳威凌华",
    "Jenny Tseng": "甄妮",
    "Bibi Zhou": "比比周",
    "Male Artist": "男艺术家",
    "Ao Ziyi": "敖子怡",
    "Li Tianze": "李",
    "Chen Sixu": "陈思旭",
    "Daniel Chan": "陈晓东",
    "Danny Chan": "陈百强",
    "Eason Chan": "陈奕迅",
    "Han Geng": "韩庚",
    "Jackie Chan": "成龙",
    "Jordan Chan": "陈小春",
    "Jeff Chang": "张信哲",
    "Phil Chang": "张宇",
    "Chang Yu-sheng": "张雨生",
    "Wakin Chau": "瓦金洲",
    "Gary Chaw": "曹格",
    "Bobby Chen": "陈升",
    "Chen Chusheng": "陈楚生",
    "Edison Chen": "陈冠希",
    "Ronald Cheng": "郑中基",
    "Dicky Cheung": "张卫健",
    "Hins Cheung": "张敬轩",
    "Hua Chenyu": "华晨宇",
    "Jacky Cheung": "张学友",
    "Leslie Cheung": "张国荣",
    "Chou Chuan-huing": "周传辉",
    "Hsiao Huang-chi": "小黄池",
    "Jay Chou": "周杰伦",
    "Chyi Chin": "齐 秦",
    "Cui Jian": "崔健",
    "Van Fan": "范逸臣",
    "Khalil Fong": "方大同",
    "Jam Hsiao": "萧敬腾",
    "Anson Hu": "胡彦斌",
    "Hu Xia": "胡霞",
    "Z.Tao": "陶喆",
    "Stanley Huang": "黄立行",
    "Yida Huang": "黄义达",
    "Andy Hui": "许志安",
    "Samuel Hui": "许冠杰",
    "Richie Jen": "任贤齐",
    "Leo Ku": "古巨基",
    "Aaron Kwok": "郭富城",
    "Leon Lai": "黎明",
    "Chet Lam": "林一峰",
    "Andy Lau": "刘德华",
    "Hacken Lee": "李克勤",
    "Nicky Lee": "李玖哲",
    "Edmond Leung": "梁汉文",
    "JJ Lin": "林俊杰",
    "Yoga Lin": "林宥嘉",
    "Lay Zhang": "打下张",
    "Liu Huan": "刘欢",
    "Lo Ta-yu": "罗大佑",
    "Crowd Lu": "卢广仲",
    "Luhan": "鲁汉",
    "Show Lo": "罗志祥",
    "Anthony Neely": "倪安东",
    "Pu Shu": "朴树",
    "William So": "苏永康",
    "Sun Nan": "孙楠",
    "Alan Tam": "谭咏麟",
    "Kris Wu": "吴亦凡",
    "David Tao": "陶喆",
    "Nicholas Tse": "谢霆锋",
    "Anthony Wong": "黄秋生",
    "Wang Feng": "王峰",
    "Jiro Wang": "汪东城",
    "Leehom Wang": "王力宏",
    "Roy Wang": "王源",
    "Vision Wei": "魏晨",
    "Dave Wong": "王杰",
    "Michael Wong": "王敏德",
    "Kenji Wu": "吴克群",
    "Xie Hexian": "谢和弦",
    "Xu Song": "许嵩",
    "Xu Wei": "许巍",
    "Evan Yo": "蔡旻佑",
    "Harlem Yu": "庾澄庆",
    "Jason Zhang": "张杰",
    "Zeng Yi": "曾益",
    "Jackson Yi": "易烊千玺",
    "Zuoxiao Zuzhou": "左小祖咒",
    "Yang Pei-An": "杨培安",
    "Joker Xue": "薛之谦"
}
names: Dict[str, str] = {}
for en, zh in translation.items():
    names[re.sub(r"[\p{P} ]", "", en).lower()] = zh.replace(" ", "")


def pinyinfy(name: str) -> str:
    """
    Returns the pinyin of the input name.

    Args:
        name (str): Input name string

    Returns:
        str: Pinyin or english of the input name

    """
    return pinyin.get(name, delimiter='', format='strip').lower()


class NeteaseRequest:

    """A request wrapper for Netease music."""

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
    def encode_netease_data(cls, data) -> str:  # pragma: no cover
        data = json.dumps(data)
        key = binascii.unhexlify("7246674226682325323F5E6544673A51")
        encryptor = AES.new(key, AES.MODE_ECB)
        pad = 16 - len(data) % 16
        fix = chr(pad) * pad
        byte_data = (data + fix).encode("utf-8")
        return binascii.hexlify(encryptor.encrypt(byte_data)).upper().decode()

    @classmethod
    def encrypted_request(cls, data) -> dict:  # pragma: no cover
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
    def aes(cls, text, key):  # pragma: no cover
        pad = 16 - len(text) % 16
        text = text + bytearray([pad] * pad)
        encryptor = AES.new(key, 2, b"0102030405060708")
        ciphertext = encryptor.encrypt(text)
        return base64.b64encode(ciphertext)

    @classmethod
    def rsa(cls, text, pubkey, modulus):  # pragma: no cover
        text = text[::-1]
        rs = pow(int(binascii.hexlify(text), 16),
                 int(pubkey, 16), int(modulus, 16))
        return format(rs, "x").zfill(256)

    @classmethod
    def create_key(cls, size):  # pragma: no cover
        return binascii.hexlify(os.urandom(size))[:16]

    @classmethod
    def request(cls, url: str, data: Dict[str, Any], method: str = "POST") -> Dict[str, Any]:

        results = {}
        status = requests.codes.ok
        text = ""

        try:
            if method == "GET":
                resp = cls.session.get(url, params=data, timeout=20)
            else:
                resp = cls.session.post(url, data=data, timeout=20)
            results = resp.json()
            text = resp.text
            status = resp.status_code
        except Exception as e:
            results = {}
            logger.debug(e)

        if status != requests.codes.ok or not text:
            results = {}

        return results


class NeteaseSong:

    def __init__(self, idx: int, title: str, artists: str):
        """
        Netease song wrapper class.

        Args:
            idx (int): Index
            title (str): Title of the song
            artists (str): String of artists

        """
        self.id = idx
        self.title = title
        self.artists = artists


@cachier(stale_after=datetime.timedelta(days=7))
def get_lyric(idx) -> str:
    row_data = {"csrf_token": "", "id": idx, "lv": -1, "tv": -1}
    data = NeteaseRequest.encrypted_request(row_data)
    return NeteaseRequest.request(url="https://music.163.com/weapi/song/lyric", method="POST", data=data).get("lrc", {}).get("lyric", "")


@cachier(stale_after=datetime.timedelta(days=3))
def search(title, artists) -> List[NeteaseSong]:

    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": title, "type": 1, "offset": 0, "limit": 30},
    }
    data = {"eparams": NeteaseRequest.encode_netease_data(eparams)}

    res_data = (
        NeteaseRequest.request(
            "http://music.163.com/api/linux/forward", method="POST", data=data
        )
        .get("result", {})
        .get("songs", {})
    )
    songs_list: List[NeteaseSong] = []
    backup: List[NeteaseSong] = []

    logger.debug(artists)

    # John Doe -> johndoe
    # 张三 -> zhangsan
    # Jay Zhou -> zhoujielun

    artists = re.sub(r"[\p{P} ]", "", artists.lower())
    artists = pinyinfy(artists)
    for artist in names:
        if artist in artists:
            artists = artists.replace(artist, pinyinfy(names[artist]))

    for item in res_data:

        singers = [pinyinfy(s.get("name", "").replace(' ', ''))
                   for s in item.get("ar", [])]
        found = False
        for singer in singers:
            if singer in artists:
                found = True

        song = NeteaseSong(
            idx=item.get("id", ""),
            title=re.sub(r" +", " ", re.sub(r"[[《<(（【「{].*?[]】）」}>)》]",
                                            " ", item.get("name", ""))),
            artists=",".join(
                map(lambda x: re.sub(r" +", " ", re.sub(r"\p{P}", " ", x.get("name", "Unknown"))), item.get("ar", []))),
        )
        if found:
            songs_list.append(song)
        else:
            backup.append(song)
    logger.debug([s.artists for s in songs_list])
    logger.debug([s.artists for s in backup])
    return songs_list if songs_list else backup


def get_lyrics(songs: List[NeteaseSong]) -> List[Any]:
    """
    Retrieve a list of lyric from given songs.

    Args:
        songs (List[NeteaseSong]): List of NeteaseSong
        debug (bool, optional): Debugging mode. Defaults to False.

    Returns:
        List: (List[Any])
    """
    results: List[Any] = []
    for song in songs[:3]:
        lyric = get_lyric(idx=song.id)
        if lyric:
            results.append((song, lyric))
    return results


def get_info(app: str = "Spotify") -> Tuple[str, str, str, float, str, float]:
    template = """
    on run
        if application "%s" is running then
            tell application "%s"
                set currentInfo to {"Music", artist of current track, "###", name of current track, player position, player state, duration of current track}
            end tell
        end if
        return currentInfo
    end run
    """ % (app, app)

    code, res, error = osascript.run(template, background=False)

    logger.debug(res, error, code)
    if res:
        meta1, meta2 = res.split('###')
        meta1, meta2 = meta1.strip(" ,"), meta2.strip(" ,")
        application, *artists = map(str.strip, meta1.strip(" ,").split(','))
        artists = ','.join(artists)

        *title, position, status, duration = map(str.strip, meta2.split(','))
        title = ','.join(title)

        if float(duration) <= 1200:
            duration = float(duration)
        else:
            duration = float(duration) / 3600
        
        position = float(position)
        title = HanziConv.toSimplified(title)
        return application, artists, title, position, status, duration
    else:
        return None, None, None, None, None, None


def parse_line(line):
    words = re.sub(r'\[.*?\]', '', line)
    if not re.findall(r'\[([0-9]+):([0-9])+\.([0-9]+)\]', line):
        return 0, words
    minute, second, _ = re.findall(
        r'\[([0-9]+):([0-9]+)\.([0-9]+)\]', line)[0]
    curr = int(minute) * 60 + int(second)
    return curr, words


def parse(lyrics, position, duration, minimal: bool = False):
    if not lyrics:
        return ""
    song, lyric = lyrics[0]
    for song, lyric in lyrics:
        logger.debug(song.title + "|" + song.artists)
        lines = [line for line in lyric.split('\n') if line.strip()]

        lines = list(map(parse_line, lines))

        if all(line[0] == 0 for line in lines):
            continue

        starts = [0] + [line[0] for line in lines][:-1]
        ends = [line[0] for line in lines]
        lines = [line[-1] for line in lines]

        for start, end, words in zip(starts, ends, [""] + lines):
            words = words.lower().capitalize()
            words = re.sub(r", *", ", ", words).strip(string.punctuation + " ")
            if start <= position <= end:
                if minimal:
                    return words
                return f"[{song.title}/{song.artists}] " + words
    return ""


def main(app: str = "Spotify", minimal: bool = False, background_color: str = "51,204,153", font_color: str = "255,255,255", font_size: int = 12, traditional: bool = False):

    style = {
        "text": "",
        "background_color": background_color,
        "font_color": font_color,
        "font_size": font_size
    }

    meta = get_info(app=app)
    logger.debug("|".join(map(str, meta)))

    application, artists, title, position, status, duration = meta

    if any(x is None for x in meta):
        logger.debug('Not playing')
        return

    if status != 'playing':
        logger.debug('Paused')
        return
    else:
        songs = search(title, artists)
        lyrics = get_lyrics(songs)
        words = parse(lyrics, position, duration, minimal=minimal)
        if words is not None:
            if traditional:
                words = HanziConv.toTraditional(words)
            style["text"] = words
        else:
            style["text"] = f'{application.title()} -- {title} -- {artists}'
        logger.debug(style)
        print(json.dumps(style))

    return
