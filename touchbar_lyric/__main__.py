
import argparse
import os
import re
import binascii
import base64
import json
import copy
import requests
from Crypto.Cipher import AES
import requests
import osascript
import hashlib
import time
import math
import requests
from cachier import cachier
import datetime
from typing import *
import pinyin
from hanziconv import HanziConv
from touchbar_lyric import *


if __name__ == '__main__':
    # get_proxy.clear_cache()
    parser = argparse.ArgumentParser('Lyric script')
    parser.add_argument('--api', type=str, help='Random proxy for netease', default=None)
    parser.add_argument('--debug', action='store_true', help='Debug mode', default=False)

    args = parser.parse_args()
    main(api=args.api, debug=args.debug)
