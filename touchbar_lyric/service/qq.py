#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-16 09:10:24
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


import json
from asyncio.log import logger
from typing import List

from QQMusicAPI import QQMusic

from touchbar_lyric import Song


def qq_music_search(title: str, artists: str) -> List[Song]:
    """
    Search from QQ Music with artists and title.
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
    >>> songs = qq_music_search("海阔天空", "Beyond")
    >>> len(songs) > 0
    True
    >>> any(s.anchor(10) is not None for s in songs)
    True
    """
    try:
        response = QQMusic.search(title)
    except json.decoder.JSONDecodeError as e:
        logger.error(e)
        return []
    songs = []
    top: int = 3
    for song in response.data:
        lyric = song.lyric
        lyric.extract()
        if lyric.lyric or lyric.trans:
            content = lyric.lyric or lyric.trans
            songs.append(
                Song(
                    title=song.name,
                    artists=",".join([x.name for x in song.singer]),
                    target_title=title,
                    target_artists=artists,
                    lyric=content,
                )
            )
            top -= 1
            if top == 0:
                break
    return songs
