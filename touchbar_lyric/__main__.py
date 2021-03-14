#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:29:12
# @Author  : Chenghao Mou (chenghao@gmail.com)

import typer

from loguru import logger
from touchbar_lyric.utility import get_info
from touchbar_lyric.service import universal_search

def run(
    app: str = typer.Option(default="Spotify", help="Application to track"),
    debug: bool = typer.Option(default=False, is_flag=True, help="To show debug messages or not")
): # pragma: no cover
    {
        True: logger.enable,
        False: logger.disable
    }[debug]("touchbar_lyric")
    
    media_info = get_info(app)
    if media_info is None:
        return
    
    songs = universal_search(media_info.name, media_info.artists)
    for song in songs:
        if song.anchor(media_info.position):
            print(song.anchor(media_info.position))
            break

if __name__ == "__main__": # pragma: no cover
    typer.run(run)