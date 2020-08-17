#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-16 09:10:24
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import datetime
from typing import List

import textdistance
from cachier import cachier
from loguru import logger
from QQMusicAPI import QQMusic

from touchbar_lyric import Song


@cachier(stale_after=datetime.timedelta(days=30))
def qq_music_search(title: str, artists: str) -> List[Song]:
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
    >>> len(qq_music_search("海阔天空", "Beyond")) > 0
    True
    """
    response = QQMusic.search(title)
    songs = []
    for i, song in enumerate(response.data[:3]):
        lyric = song.lyric
        lyric.extract()
        if lyric.lyric or lyric.trans:
            content = lyric.lyric or lyric.trans
            s = Song(title=song.name, artists=",".join([x.name for x in song.singer]), lyric=content.replace("&apos;", "'"),)
            logger.debug(f"{Song.artist_text(s.artists)} VS {Song.artist_text(artists)}")
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
