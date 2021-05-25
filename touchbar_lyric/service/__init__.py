#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:54:40
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import datetime
from typing import List

from cachier import cachier
import logging.config

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


@cachier(next_time=True)
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
