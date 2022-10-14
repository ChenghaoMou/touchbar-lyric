#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:54:40
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import logging.config
import os
from typing import List, Tuple

from diskcache import FanoutCache
from hanziconv import HanziConv
from strsimpy.normalized_levenshtein import NormalizedLevenshtein

from touchbar_lyric import Song
from touchbar_lyric.service.netease import netease_music_search
from touchbar_lyric.service.qq import qq_music_search

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)


CACHE = os.path.join(os.path.expanduser("~"), ".cache")

if not os.path.exists(CACHE):
    os.mkdir(CACHE)

cache = FanoutCache(CACHE, timeout=2)


@cache.memoize(typed=True, expire=None, tag="lyric")
def universal_search(title: str, artists: str) -> List[Song]:  # pragma: no cover
    songs: List[Tuple[int, Song]] = []
    title = HanziConv.toSimplified(title)
    songs.extend((-i, s) for i, s in enumerate(netease_music_search(title, artists)))
    songs.extend((-i, s) for i, s in enumerate(qq_music_search(title, artists)))

    return [s[1] for s in sorted(
        songs,
        key=lambda s: (
            NormalizedLevenshtein().similarity(s[1].title, s[1].target_title)
            + NormalizedLevenshtein().similarity(s[1].artists, s[1].target_artists),
            s[0],
        ),
        reverse=True,
    )]
