
from touchbar_lyric import NeteaseRequest, get_lyric, search, pinyinfy, get_info, get_lyrics, NeteaseSong, parse_line


def test_request():
    assert NeteaseRequest.request("", {}, True) == {}


def test_get_lyric():
    res = get_lyric(idx="1448183660", debug=True)
    assert res != ""


def test_search():
    title = "Tonight I Celebrate My Love"
    artists = "Peabo Bryson"
    assert search(title, artists, debug=True) != []


def test_pinyinfy():
    assert pinyinfy("周杰伦") == "zhoujielun"
    assert pinyinfy("Jay Chou") == "jay chou"


def test_get_info():

    assert len(get_info("Spotify")) == 6
    assert len(get_info("Music")) == 6


def test_get_lyrics():
    lyrics = get_lyrics([
        NeteaseSong(
            idx="1448183660",
            title="don't matter",
            artists="Who?"
        )
    ])

    assert len(lyrics) == 1
    song, lyric = lyrics[0]
    assert len(lyric.split('\n')) == 47


def test_parse_line():
    assert parse_line(
        "[12:13.50] This is a line that should be parsed") == (733, ' This is a line that should be parsed')
