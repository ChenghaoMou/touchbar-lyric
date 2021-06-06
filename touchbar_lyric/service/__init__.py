#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:54:40
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import os
import logging.config
from typing import List

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)

from strsimpy.normalized_levenshtein import NormalizedLevenshtein
from touchbar_lyric import Song
from touchbar_lyric.service.netease import netease_music_search
from touchbar_lyric.service.qq import qq_music_search
from diskcache import FanoutCache

CACHE = os.path.join(os.path.expanduser("~"), ".cache")

if not os.path.exists(CACHE):
    os.mkdir(CACHE)

cache = FanoutCache(CACHE, timeout=2)


@cache.memoize(typed=True, expire=None, tag="lyric")
def universal_search(title: str, artists: str) -> List[Song]:  # pragma: no cover
    songs = []
    songs.extend(qq_music_search(title, artists))
    songs.extend(netease_music_search(title, artists))

    songs = sorted(
        songs,
        key=lambda s: (
            NormalizedLevenshtein().similarity(s.title, s.target_title)
            + NormalizedLevenshtein().similarity(s.artists, s.target_artists),
        ),
        reverse=True,
    )

    return songs
