#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-15 15:09:54
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


import argparse
import json
import math

from loguru import logger

from touchbar_lyric import RAINBOW, get_info, interpolate
from touchbar_lyric.netease_music import netease_music_search
from touchbar_lyric.qq_music import qq_music_search

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser("TouchBar Lyric Script for BTT")
    parser.add_argument(
        "--app", default="Spotify", choices=["Spotify", "Music"], help="Music application. Spotify has a better support",
    )

    parser.add_argument("--rainbow", default=False, action="store_true", help="Rainbow background colors")
    parser.add_argument("--minimal", default=False, action="store_true", help="Deprecated")
    parser.add_argument(
        "--traditional", default=False, action="store_true", help="Use traditional Chinese",
    )
    parser.add_argument("--verbose", action="store_true", help="Turn on debug mode", default=False)
    parser.add_argument("--accurate", action="store_true", help="Turn on accurate mode, skipping less ideal matches", default=False)

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

    style = {
        "text": "",
        "background_color": args.bg,
        "font_color": args.fc,
        "font_size": args.fs,
    }

    title, artists, position, status, duration = get_info(app=args.app)

    if args.rainbow:
        steps = int(duration // 6)
        base = math.floor(position / duration * 6)
        delta = int(steps * (position / duration * 6 - base))
        target = base + 1
        style["background_color"] = interpolate(RAINBOW[base][0], RAINBOW[target][0], steps)[min(delta, steps - 1)]
        style["font_color"] = interpolate(RAINBOW[base][1], RAINBOW[target][1], steps)[min(delta, steps - 1)]

    if status != "playing":
        logger.debug("Paused")
    else:
        songs = netease_music_search(title, artists)
        backup = qq_music_search(title, artists)
        songs.extend(backup)
        songs = sorted(songs, key=lambda x: x[:-1])
        logger.debug(songs)
        if args.accurate:
            songs = [s for s in songs if s[0] == 0 and s[1] <= 3]
        logger.debug(songs)
        for *_, song in songs:
            line = song.current(position, traditional=args.traditional)
            if line:
                style["text"] = line.strip()
                print(json.dumps(style))
                break
