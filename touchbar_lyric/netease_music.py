#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-10 10:54:37
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

"""Touchbar lyric widget for BTT."""

import base64
import binascii
import datetime
import json
import os
from typing import Any, Dict, List

import requests
import textdistance
from cachier import cachier
from Crypto.Cipher import AES
from loguru import logger

from touchbar_lyric import Song


class NeteaseRequest:  # pragma: no cover
    """A request wrapper for Netease music."""

    session = requests.Session()
    session.headers.update(
        {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Charset": "UTF-8,*;q=0.5",
            "Accept-Encoding": "gzip,deflate,sdch",
            "Accept-Language": "en-US,en;q=0.8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:60.0) Gecko/20100101 Firefox/60.0",
            "referer": "http://music.163.com/",
        }
    )

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
        rs = pow(int(binascii.hexlify(text), 16), int(pubkey, 16), int(modulus, 16))
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


@cachier(stale_after=datetime.timedelta(days=30))  # pragma: no cover
def netease_music_get_lyric(idx) -> str:
    data = NeteaseRequest.encrypted_request({"csrf_token": "", "id": idx, "lv": -1, "tv": -1})
    return (
        NeteaseRequest.request(url="https://music.163.com/weapi/song/lyric", method="POST", data=data)
        .get("lrc", {})
        .get("lyric", "")
    )


@cachier(stale_after=datetime.timedelta(days=30))
def netease_music_search(title: str, artists: str) -> List[Song]:
    """
    Search from Netease Music with artists and title.

    Parameters
    ----------
    title : str
        Name of the song
    artists : str
        Names of the artists

    Returns
    -------
    List[Song]
        List of songs

    Examples
    --------
    >>> len(netease_music_search("海阔天空", "Beyond")) > 0
    True
    """

    eparams = {
        "method": "POST",
        "url": "http://music.163.com/api/cloudsearch/pc",
        "params": {"s": Song.title_text(title), "type": 1, "offset": 0, "limit": 30},
    }
    data = {"eparams": NeteaseRequest.encode_netease_data(eparams)}

    res_data = (
        NeteaseRequest.request("http://music.163.com/api/linux/forward", method="POST", data=data)
        .get("result", {})
        .get("songs", {})
    )
    songs = []
    for i, item in enumerate(res_data[:3]):
        if item.get("id", None) is not None:
            s = Song(
                title=item.get("name", ""),
                artists=",".join([x["name"] for x in item.get("ar", []) if "name" in x]),
                lyric=netease_music_get_lyric(idx=item["id"]),
            )
            logger.debug(f"{item.get('id')} {Song.artist_text(s.artists)} VS {Song.artist_text(artists)}")
            songs.append(
                (
                    textdistance.levenshtein.distance(s.title, title),
                    textdistance.levenshtein.distance(s.artists, artists),
                    textdistance.levenshtein.distance(Song.title_text(s.title), title),
                    textdistance.levenshtein.distance(Song.artist_text(s.artists), Song.artist_text(artists)),
                    i,
                    s,
                )
            )
    songs = sorted(songs, key=lambda x: x[:-1])
    return songs
