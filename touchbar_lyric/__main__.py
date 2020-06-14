#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-15 15:09:54
# @Author  : Chenghao Mou (mouchenghao@gmail.com)


import argparse
from touchbar_lyric import main


if __name__ == '__main__':
    parser = argparse.ArgumentParser('TouchBar Lyric script')
    parser.add_argument('--app', default='Spotify',
                        choices=['Spotify', 'Music'], help='Music application')
    parser.add_argument('--debug', action='store_true',
                        help='Turn on debug mode', default=False)

    args = parser.parse_args()
    main(app=args.app, debug=args.debug)
