#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2020-03-10 10:54:37
# @Author  : Chenghao Mou (mouchenghao@gmail.com)

"""touchbar-lyric shows synced lyrics with BTT."""

from typing import Dict, List, Tuple

import osascript
import pinyin
import regex as re
from hanziconv import HanziConv
from loguru import logger

# Translate English names into pinyin
TRANSLATION: Dict[str, str] = {
    re.sub(r"[\p{P} ]", "", en).lower(): pinyin.get(zh.replace(" ", ""), delimiter="", format="strip").lower().strip()
    for en, zh in {
        "Bella Yao": "贝拉姚",
        "A-fu": "阿福",
        "Alan Dawa Dolma": "阿兰达瓦卓玛",
        "A-Lin": "黄丽玲",
        "A-mei": "杜诗梅",
        "Priscilla Chan": "陈慧娴",
        "Angela Chang": "张韶涵",
        "Deserts Chang": "沙漠常",
        "Cheer Chen": "陈绮贞",
        "Kelly Chen": "陈慧琳",
        "Sammi Cheng": "郑秀文",
        "Maggie Chiang": "江美琪",
        "Vivian Chow": "周慧敏",
        "Tanya Chua": "蔡健雅",
        "Gillian Chung": "钟欣潼",
        "Ding Dang": "丁当",
        "Christine Fan": "范玮琪",
        "Mavis Fan": "范晓萱",
        "Mavis Hee": "许美静",
        "Denise Ho": "何韵诗",
        "Elva Hsiao": "萧亚轩",
        "Jeannie Hsieh": "谢金燕",
        "Winnie Hsin": "辛晓琪",
        "Evonne Hsu": "许慧欣",
        "Lala Hsu": "徐佳莹",
        "Valen Hsu": "许茹芸",
        "Vivian Hsu": "徐若瑄",
        "Amber Kuo": "郭采洁",
        "Sandy Lam": "林忆莲",
        "Coco Lee": "李玟",
        "Fish Leong": "梁静茹",
        "Gigi Leung": "梁咏琪",
        "Li Yuchun": "李宇春",
        "Rene Liu": "刘若英",
        "Liu Shishi": "刘诗诗",
        "Candy Lo": "卢巧音",
        "Karen Mok": "莫文蔚",
        "Anita Mui": "梅艳芳",
        "Na Ying": "那 英",
        "Kary Ng": "吴雨霏",
        "One-Fang": "一方",
        "Cass Phang": "彭羚",
        "Wanting Qu": "想屈",
        "Sa Dingding": "萨顶顶",
        "Fiona Sit": "薛凯琪",
        "Tarcy Su": "苏慧伦",
        "Stefanie Sun": "孙燕姿",
        "Penny Tai": "戴佩妮",
        "G.E.M. Tang": "邓紫棋",
        "Stephy Tang": "邓丽欣",
        "Teresa Teng": "邓丽君",
        "Hebe Tien": "田馥甄",
        "Tsai Chin": "蔡琴",
        "Jolin Tsai": "蔡依林",
        "Kay Tse": "谢安琪",
        "Cyndi Wang": "王心凌",
        "Joanna Wang": "王若琳",
        "Landy Wen": "温岚",
        "Meng Jia": "孟佳",
        "Faye Wong": "王菲",
        "Ivana Wong": "王菀之",
        "Xidan Girl": "西单女孩",
        "Faith Yang": "杨乃文",
        "Rainie Yang": "杨丞琳",
        "Sally Yeh": "叶倩文",
        "Miriam Yeung": "杨千嬅",
        "Joey Yung": "容祖儿",
        "Jane Zhang": "张靓颖",
        "Jana Chen": "陈嘉娜",
        "Zhao Wei": "赵薇",
        "Fong Fei Fei": "方飞飞",
        "Yangwei Linghua": "阳威凌华",
        "Jenny Tseng": "甄妮",
        "Bibi Zhou": "比比周",
        "Male Artist": "男艺术家",
        "Ao Ziyi": "敖子怡",
        "Li Tianze": "李",
        "Chen Sixu": "陈思旭",
        "Daniel Chan": "陈晓东",
        "Danny Chan": "陈百强",
        "Eason Chan": "陈奕迅",
        "Han Geng": "韩庚",
        "Jackie Chan": "成龙",
        "Jordan Chan": "陈小春",
        "Jeff Chang": "张信哲",
        "Phil Chang": "张宇",
        "Chang Yu-sheng": "张雨生",
        "Wakin Chau": "瓦金洲",
        "Gary Chaw": "曹格",
        "Bobby Chen": "陈升",
        "Chen Chusheng": "陈楚生",
        "Edison Chen": "陈冠希",
        "Ronald Cheng": "郑中基",
        "Dicky Cheung": "张卫健",
        "Hins Cheung": "张敬轩",
        "Hua Chenyu": "华晨宇",
        "Jacky Cheung": "张学友",
        "Leslie Cheung": "张国荣",
        "Chou Chuan-huing": "周传辉",
        "Hsiao Huang-chi": "小黄池",
        "Jay Chou": "周杰伦",
        "Chyi Chin": "齐 秦",
        "Cui Jian": "崔健",
        "Van Fan": "范逸臣",
        "Khalil Fong": "方大同",
        "Jam Hsiao": "萧敬腾",
        "Anson Hu": "胡彦斌",
        "Hu Xia": "胡霞",
        "Z.Tao": "陶喆",
        "Stanley Huang": "黄立行",
        "Yida Huang": "黄义达",
        "Andy Hui": "许志安",
        "Samuel Hui": "许冠杰",
        "Richie Jen": "任贤齐",
        "Leo Ku": "古巨基",
        "Aaron Kwok": "郭富城",
        "Leon Lai": "黎明",
        "Chet Lam": "林一峰",
        "Andy Lau": "刘德华",
        "Hacken Lee": "李克勤",
        "Nicky Lee": "李玖哲",
        "Edmond Leung": "梁汉文",
        "JJ Lin": "林俊杰",
        "Yoga Lin": "林宥嘉",
        "Lay Zhang": "打下张",
        "Liu Huan": "刘欢",
        "Lo Ta-yu": "罗大佑",
        "Crowd Lu": "卢广仲",
        "Luhan": "鲁汉",
        "Show Lo": "罗志祥",
        "Anthony Neely": "倪安东",
        "Pu Shu": "朴树",
        "William So": "苏永康",
        "Sun Nan": "孙楠",
        "Alan Tam": "谭咏麟",
        "Kris Wu": "吴亦凡",
        "David Tao": "陶喆",
        "Nicholas Tse": "谢霆锋",
        "Anthony Wong": "黄秋生",
        "Wang Feng": "王峰",
        "Jiro Wang": "汪东城",
        "Leehom Wang": "王力宏",
        "Roy Wang": "王源",
        "Vision Wei": "魏晨",
        "Dave Wong": "王杰",
        "Michael Wong": "王敏德",
        "Kenji Wu": "吴克群",
        "Xie Hexian": "谢和弦",
        "Xu Song": "许嵩",
        "Xu Wei": "许巍",
        "Evan Yo": "蔡旻佑",
        "Harlem Yu": "庾澄庆",
        "Jason Zhang": "张杰",
        "Zeng Yi": "曾益",
        "Jackson Yi": "易烊千玺",
        "Zuoxiao Zuzhou": "左小祖咒",
        "Yang Pei-An": "杨培安",
        "Joker Xue": "薛之谦",
    }.items()
}

# Rainbow color gradients
RAINBOW: List[Tuple[str, str]] = [
    ("148, 0, 211", "255,255,255"),
    ("75, 0, 130", "255,255,255"),
    ("0, 0, 255", "255,255,255"),
    ("0, 255, 0", "0,0,0"),
    ("255, 255, 0", "0,0,0"),
    ("255, 127, 0", "255,255,255"),
    ("255, 0 , 0", "255,255,255"),
    ("0, 0, 0", "255,255,255"),
]


class Song:
    def __init__(self, title: str = None, artists: str = None, lyric: str = None):
        """
        Abstraction class for a song.

        Parameters
        ----------
        title : str, optional
            Name of the song, by default None
        artists : str, optional
            Names of the artists, by default None
        lyric : str, optional
            String content of the lyric, by default None

        Examples
        --------
        >>> song = Song("test", "singer", "[00:01.12]Hello world!")
        """
        self.title = title
        self.artists = artists
        self.lyric = lyric
        self.lines = self.parse()

    def parse(self) -> List[Tuple[Tuple[float, float], str]]:
        """
        Parse the lyric string into a list of interval ans line pairs.

        Returns
        -------
        List[Tuple[Tuple[float, float], str]]
            List of interval ans line pairs

        Examples
        --------
        >>> song = Song("test", "singer", "[00:01.12]Hello world!")
        >>> song.parse()
        [((1.012, inf), 'Hello world!')]
        """
        lines: List[str] = [line.strip() for line in self.lyric.split("\n") if line.strip()]
        result: List[Tuple[float, str]] = []
        for line in lines:
            words = line.rsplit("]", 1)[-1]
            if not words:
                continue
            for stamp in re.findall(r"(\[[0-9]+:[0-9]+\.[0-9]+\])", line):
                stamp = stamp.strip("[]")
                minute, second, milisecond = re.split(r"\.|\:", stamp)
                result.append((int(minute) * 60 + int(second) + int(milisecond) / 1000, words))
        ordered = sorted(result, key=lambda x: x[0])
        intervals: List[Tuple[Tuple[float, float], str]] = []
        for i, (start, words) in enumerate(ordered):
            if i == len(ordered) - 1:
                intervals.append(((start, float("inf")), words))
            else:
                intervals.append(((start, ordered[i + 1][0]), words))
        return intervals

    def current(self, timestamp: int, traditional: bool = False) -> str:
        """
        Find the current line in the lyrics.

        Parameters
        ----------
        timestamp : int
            Current timestamp
        traditional : bool, optional
            Convert the line into traditional Chinese or not, by default False

        Returns
        -------
        str
            A line in the lyrics

        Examples
        --------
        >>> song = Song("test", "singer", "[00:01.12]原谅我这一生不羁放纵爱自由")
        >>> song.current(2)
        '原谅我这一生不羁放纵爱自由'
        >>> song.current(2, True)
        '原諒我這一生不羈放縱愛自由'
        """
        low, high = 0, len(self.lines)
        while low < high:
            mid = (low + high) // 2
            if self.lines[mid][0][0] <= timestamp <= self.lines[mid][0][1]:
                if traditional:
                    return HanziConv.toTraditional(self.lines[mid][1])
                return self.lines[mid][1]
            elif self.lines[mid][0][0] > timestamp:
                high = mid
            else:
                low = mid
        return

    @staticmethod
    def artist_text(artists: str) -> str:
        """
        Return cleaned artists names.

        Parameters
        ----------
        artists : str
            Names of artists

        Returns
        -------
        str
            Cleaned up names

        Examples
        --------
        >>> Song.artist_text('Jay Chou')
        'zhoujielun'
        >>> Song.artist_text('The Wanted')
        'the wanted'
        >>> Song.artist_text('周杰伦')
        'zhoujielun'
        """
        result = []
        for name in artists.split(","):
            name = name.strip()
            name = re.sub(r" +", " ", name)
            alt = "".join(c for c in name if c.isalnum()).lower()
            if alt in TRANSLATION:
                name = TRANSLATION[alt]
            name = pinyin.get(name, delimiter="", format="strip").lower().strip()
            result.append(name)
        return ",".join(result)

    @staticmethod
    def title_text(title) -> str:
        """
        Return cleaned title.

        Parameters
        ----------
        title : [type]
            Original song title

        Returns
        -------
        str
            Cleaned up title

        Examples
        --------
        >>> Song.title_text("南山南（原唱 马頔）")
        '南山南'
        """
        text = re.sub(r"[[《<(（【「{].*?[]】）」}>)》]", "", title).strip()
        text = re.sub(r"feat\..*?$", "", text, flags=re.IGNORECASE)
        return text

    def __str__(self) -> str:  # pragma: no cover
        return f"{self.title} {self.artists}"

    def __repr__(self) -> str:  # pragma: no cover
        return self.__str__()


def get_info(app: str = "Spotify") -> Tuple[str, str, float, str, float]:
    """
    Get information about the track in play.

    Parameters
    ----------
    app : str, optional
        Name of the app, by default "Spotify"

    Returns
    -------
    Tuple[str, str, float, str, float]
        Title, artists, position, status, duration of the track

    Examples
    --------
    >>> title, artists, position, status, duration = get_info("Spotify")
    >>> status in [None, "playing", "paused"]
    True
    """

    template = f"""
    on run
        if application "{app}" is running then
            tell application "{app}"
                set currentInfo to {{name of current track, "|", artist of current track, "|", player position, "|", player state, "|", duration of current track}}
            end tell
        end if
        return currentInfo
    end run
    """

    code, res, error = osascript.run(template, background=False)
    title = artists = position = status = duration = None
    if code == 0:
        segments = res.split("|")
        title, artists, position, status, duration = map(lambda x: x.strip(' ,"'), segments)
        if all(x is not None for x in [title, artists, position, status, duration]):
            position = float(position)
            duration = float(duration)
            if duration <= 1200:
                duration = duration
            else:
                duration /= 1000
            title = HanziConv.toSimplified(title)
            title = re.sub(r"[[《<(（【「{].*?[]】）」}>)》]", "", title)
            title = title.rsplit("-", 1)[0]
    else:
        logger.debug(error)

    return title, artists, position, status, duration


def interpolate(start: str, goal: str, steps: int = 10) -> List[str]:
    """
    Generate gradient colors from start to goal.

    Parameters
    ----------
    start : str
        Start color in RGB format. e.g 255,255,255
    goal : str
        Goal color in RGB format. e.g 0,0,0
    steps : int, optional
        Number of steps, by default 10

    Returns
    -------
    List[str]
        List of colors

    Examples
    --------
    >>> interpolate("0,0,0", "255,255,255", 5)
    ['0,0,0', '51,51,51', '102,102,102', '153,153,153', '204,204,204', '255,255,255']
    """
    R, G, B = list(map(int, start.split(",")))
    targetR, targetG, targetB = list(map(int, goal.split(",")))
    diffR, diffG, diffB = targetR - R, targetG - G, targetB - B

    return [
        f"{int(R + (diffR * i / steps))},{int(G + (diffG * i / steps))},{int(B + (diffB * i / steps))}"
        for i in range(steps + 1)
    ]
