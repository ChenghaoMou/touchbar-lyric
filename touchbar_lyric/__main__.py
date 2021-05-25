#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 15:29:12
# @Author  : Chenghao Mou (chenghao@gmail.com)

import typer
import logging.config

from hanziconv import HanziConv
from loguru import logger
from touchbar_lyric.utility import get_info
from touchbar_lyric.service import universal_search

logging.config.dictConfig(
    {
        "version": 1,
        "disable_existing_loggers": True,
    }
)


def run(
    app: str = typer.Option(default="Spotify", help="Application to track"),
    debug: bool = typer.Option(
        default=False, is_flag=True, help="To show debug messages or not"
    ),
    traditional: bool = typer.Option(
        default=False,
        is_flag=True,
        help="Translate lyrics into Traditional Chinese if possible",
    ),
):  # pragma: no cover
    {True: logger.enable, False: logger.disable}[debug]("touchbar_lyric")

    if not debug:
        logger.disable("touchbar_lyric")
        logger.disable("__main__")

    media_info = get_info(app)
    if media_info is None:
        return

    songs = universal_search(media_info.name, media_info.artists)

    for song in songs:
        if song.anchor(media_info.position):
            line: str = song.anchor(media_info.position)
            if traditional:
                line = HanziConv.toTraditional(line)
            print(line)
            break


if __name__ == "__main__":  # pragma: no cover
    typer.run(run)
