#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-14 14:37:35
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import html
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

import regex as re

from touchbar_lyric.utility import search_intervals


@dataclass
class Song:

    title: str
    artists: str
    target_title: str
    target_artists: str
    lyric: str
    lines: Optional[List[Tuple[float, str]]] = None
    intervals: Optional[List[float]] = None

    def __post_init__(self):

        lyric = self.lyric
        lyric = html.unescape(lyric)

        self.lines = []
        self.intervals = []
        for line in lyric.split("\n"):
            info, *words = line.rsplit("]", 1)
            timestamp = re.search(r"\[([0-9]+):([0-9]+)\.([0-9]+)\]", info + "]")
            if not timestamp:
                continue
            minute, second, subsecond = (
                timestamp.group(1),
                timestamp.group(2),
                timestamp.group(3),
            )
            curr_stamp = int(minute) * 60 + int(second) + \
                int(subsecond) / (10**len(subsecond))
            self.lines.append((curr_stamp, "".join(words)))
            self.intervals.append(curr_stamp)

    def anchor(self, timestamp: float) -> Optional[str]:
        """Find current timestamp for this song.

        Parameters
        ----------
        timestamp : float
            Current timestamp

        Returns
        -------
        Optional[str]
            A line or None

        Examples
        --------
        >>> song = Song("Hello", "Adele", "Hello", "Adele", "[01:12.34]Hello")
        >>> song.anchor(60)
        'Hello'
        >>> song.anchor(120)
        'Hello'
        >>> song = Song("Hello", "Adele", "Hello", "Adele", "")
        >>> song.anchor(10) is None
        True
        """
        if not self.intervals or not self.lines:
            return None

        idx = search_intervals(self.intervals, timestamp)
        if idx != -1:
            return self.lines[idx][-1]

        return None
