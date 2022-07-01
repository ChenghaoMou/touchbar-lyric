#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2021-03-01 19:51:54
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

import bisect
from collections import namedtuple
from typing import List, Optional

import applescript
from loguru import logger

MediaInformation = namedtuple(
    "MediaInformation", ["name", "artists", "position", "state", "durantion"]
)


def get_info(app: str) -> Optional[MediaInformation]:
    """Get media information with apple script.

    Parameters
    ----------
    app : str
        The name of the application

    Returns
    -------
    Optional[MediaInformation]
        MediaInformation object

    Examples
    --------
    >>> ans = get_info("Spotify")
    >>> assert ans is None or isinstance(ans, MediaInformation)
    """

    script: str = f"""
    on run
        if application "{app}" is running then
            tell application "{app}"
                set currentInfo to {{name of current track, "|||", artist of current track, "|||", player position, "|||", player state, "|||", duration of current track}}
            end tell
        else
            set currentInfo to "Empty"
        end if
        return currentInfo
    end run
    """

    r = applescript.run(script)

    logger.debug(r.out)

    ans: Optional[MediaInformation] = None
    if r.code == 0 and r.out != "Empty":
        segments = r.out.split(", |||, ")
        segments = [s.strip(', ') for s in segments]
        if len(segments) != 5:
            return ans
        ans = MediaInformation(
            segments[0],
            segments[1],
            float(segments[2]),
            {"playing": 2, "paused": 1, "stopped": 0}.get(segments[3], 0),
            float(segments[4]) // 1000
            if "." not in segments[4]
            else float(segments[4]),
        )

    logger.debug(ans)

    return ans


def search_intervals(
    intervals: List[float], position: float
) -> int:  # pragma: no cover
    """Search a timestamp in a list of intervals.

    Parameters
    ----------
    intervals : List[float]
        List of timestamps
    position : float
        Current timestamp

    Returns
    -------
    int
        Index of the interval

    Examples
    --------
    >>> search_intervals([12, 15], 13)
    0
    >>> search_intervals([12, 15], 7)
    0
    >>> search_intervals([12, 15], 16)
    1
    """
    idx = max(0, bisect.bisect_left(intervals, position) - 1)

    if len(intervals) > idx >= 0 and (
        idx == 0
        or idx == len(intervals) - 1
        or (intervals[idx] <= position <= intervals[idx + 1])
    ):
        return idx

    return -1
