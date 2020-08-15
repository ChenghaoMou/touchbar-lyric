#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-14 19:51:58
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import datetime
from collections import defaultdict

import requests
from cachier import cachier
from loguru import logger

from touchbar_lyric import Song


@cachier(stale_after=datetime.timedelta(days=7),)
def get_lyric(title: str, artists: str) -> str:
    """Retrieve lyric from gecimi.com based on title and artists.

    Parameters
    ----------
    title : str
        Name of the song
    artists : str
        Names of the artists

    Returns
    -------
    str
        Most poplular choice for the given title and artists

    """

    candidates = defaultdict(list)
    for artist in artists.split(","):
        try:
            r = requests.get(f"http://gecimi.com/api/lyric/{title}/{artist}".replace(" ", "%20")).json()
            code, result = r["code"], r["result"]
            # print(r)
        except Exception as e:
            logger.debug(e)
            code = 404
            result = []

        if code == 0:
            for datum in result:
                try:
                    candidates[(datum["song"], datum["artist_id"])].append(requests.get(datum["lrc"]).text)
                except Exception as e:
                    logger.debug(e)
                    continue
        else:
            logger.debug(code)

    if candidates:
        majority = sorted(candidates.keys(), key=lambda x: len(candidates[x]), reverse=True)[0]
        return candidates[majority][0]

    return None


def current(title: str, artists: str, timestamp: int, traditional: bool = False) -> str:
    lyric = get_lyric(title, artists)

    if lyric is None:
        return None

    return Song(title=title, artist=artists, lyric=lyric, traditional=traditional).current(timestamp=timestamp)


if __name__ == "__main__":
    from touchbar_lyric import get_info

    title, artists, timestamp, status, _ = get_info("Spotify")
    print(title, artists)
    print(current(title, artists, timestamp, False))
