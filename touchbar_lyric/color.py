#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-08-15 10:29:56
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


def interpolate_tuple(startcolor, goalcolor, steps):
    """Take two RGB color sets and mix them over a specified number of steps."""
    # white

    R = startcolor[0]
    G = startcolor[1]
    B = startcolor[2]

    targetR = goalcolor[0]
    targetG = goalcolor[1]
    targetB = goalcolor[2]

    DiffR = targetR - R
    DiffG = targetG - G
    DiffB = targetB - B

    buffer = []

    for i in range(steps + 1):
        iR = int(R + (DiffR * i / steps))
        iG = int(G + (DiffG * i / steps))
        iB = int(B + (DiffB * i / steps))

        color = f"{iR},{iG},{iB}"
        buffer.append(color)

    return buffer


def interpolate(startcolor, goalcolor, steps):
    """Wrapper for interpolate_tuple that accepts colors."""
    start_tuple = list(map(int, startcolor.split(",")))
    goal_tuple = list(map(int, goalcolor.split(",")))

    return interpolate_tuple(start_tuple, goal_tuple, steps)
