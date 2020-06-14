
from touchbar_lyric import NeteaseRequest, get_lyric, search, pinyinfy


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
    assert pinyinfy("Jay Chou") == "Jay Chou"
