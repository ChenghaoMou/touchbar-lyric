#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-15 15:09:54
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


import argparse

from loguru import logger

from touchbar_lyric.netease_music import main

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser("TouchBar Lyric Script for BTT")
    parser.add_argument(
        "--app", default="Spotify", choices=["Spotify", "Music"], help="Music application. Spotify has a better support",
    )

    parser.add_argument("--rainbow", default=False, action="store_true", help="Rainbow backgroud colors")
    parser.add_argument("--minimal", default=False, action="store_true", help="Deprecated")
    parser.add_argument(
        "--traditional", default=False, action="store_true", help="Use traditional Chinese",
    )
    parser.add_argument("--verbose", action="store_true", help="Turn on debug mode", default=False)

    parser.add_argument("--bg", default="51,204,153", type=str, help="Background color in RGB")
    parser.add_argument("--fs", default=12, type=int, help="Font size")
    parser.add_argument("--fc", default="255,255,255", type=str, help="Font color in RGB")

    args = parser.parse_args()
    if args.verbose:
        logger.enable("touchbar_lyric")
        logger.enable("__main__")
    else:
        logger.disable("touchbar_lyric")
        logger.disable("__main__")

    logger.debug(args)

    main(
        app=args.app,
        minimal=args.minimal,
        rainbow=args.rainbow,
        background_color=args.bg,
        font_size=args.fs,
        font_color=args.fc,
        traditional=args.traditional,
    )
