from typing import List
from urllib import parse, request

import regex
import requests
from bs4 import BeautifulSoup

from touchbar_lyric import Song

UA = "Mozilla/5.0 (Maemo; Linux armv7l; rv:10.0.1) Gecko/20100101 Firefox/10.0.1 Fennec/10.0.1"


def name_comparison(title: str, artists: str, target_title: str, target_artists: str) -> bool:
    """
    Compare the name of the song and the name of the artist.

    Parameters
    ----------
    title : str
        Name of the song
    artists : str
        Names of the artists
    target_title : str
        Name of the song to compare
    target_artists : str
        Names of the artists to compare

    Returns
    -------
    bool
        Whether the name of the song and the name of the artist are the same

    Examples
    --------
    >>> name_comparison("海阔天空", "Beyond", "海阔天空", "Beyond")
    True
    >>> name_comparison("I`m not the only one", "Sam Smith", "I'm not the only one", "Sam Smith")
    True
    """
    def preprocess(text):
        return "".join(regex.findall(r"\w+", text.lower()))

    return preprocess(target_title) in preprocess(title) and preprocess(target_artists) in preprocess(artists)


def rentanadviser_music_search(title: str, artists: str) -> List[Song]:
    proxy = request.getproxies()
    search_url = f'''https://www.rentanadviser.com/en/subtitles/subtitles4songs.aspx?{
        parse.urlencode({
            "src": f"{artists} {title}"
        })
    }'''
    search_results = requests.get(search_url, proxies=proxy)
    soup = BeautifulSoup(search_results.text, 'html.parser')
    container = soup.find(id="tablecontainer")
    if not container:
        return []
    result_links = container.find_all("a")

    for result_link in result_links:
        if result_link["href"] != "subtitles4songs.aspx":
            info = result_link.get_text()
            if not name_comparison(info, info, title, artists):
                continue
            url = f'https://www.rentanadviser.com/en/subtitles/{result_link["href"]}&type=lrc'
            possible_text = requests.get(url, proxies=proxy)
            soup = BeautifulSoup(possible_text.text, 'html.parser')
            event_validation = soup.find(id="__EVENTVALIDATION")
            if not event_validation:
                continue
            event_validation = event_validation.get("value")

            view_state = soup.find(id="__VIEWSTATE")
            if not view_state:
                continue
            view_state = view_state.get("value")

            lrc = requests.post(
                possible_text.url,
                {
                    "__EVENTTARGET": "ctl00$ContentPlaceHolder1$btnlyrics",
                    "__EVENTVALIDATION": event_validation,
                    "__VIEWSTATE": view_state
                },
                headers={"User-Agent": UA, "referer": possible_text.url},
                proxies=proxy,
                cookies=search_results.cookies
            )
            return [Song(
                title=info,
                artists=info,
                target_title=title,
                target_artists=artists,
                lyric=lrc.text
            )]
    return []


def lyricsify_music_search(title: str, artists: str) -> List[Song]:
    proxy = request.getproxies()
    search_url = f'''https://www.lyricsify.com/search?{
        parse.urlencode({
            "q": f"{artists} {title}"
        })
    }'''
    search_results = requests.get(search_url, proxies=proxy, headers={"User-Agent": UA})
    soup = BeautifulSoup(search_results.text, 'html.parser')

    result_container = soup.find("div", class_="sub")
    if not result_container:
        return []

    result_list = result_container.find_all("div", class_="li")
    if not result_list:
        return []

    for result in result_list:
        result_link = result.find("a")
        name = result_link.get_text()
        if not name_comparison(name, name, title, artists):
            continue

        url = f"https://www.lyricsify.com{result_link['href']}?download"
        lyrics_page = requests.get(url, proxies=proxy, headers={"User-Agent": UA})
        soup = BeautifulSoup(lyrics_page.text, 'html.parser')
        element = soup.find(id="iframe_download")
        if not element:
            continue
        download_link = element.get("src")
        if not download_link:
            continue
        lrc = requests.get(download_link, proxies=proxy,
                           cookies=lyrics_page.cookies, headers={"User-Agent": UA}).text
        return [Song(
            title=name,
            artists=name,
            target_title=title,
            target_artists=artists,
            lyric=lrc
        )]
    return []


def rclyricsband_music_search(title: str, artists: str) -> List[Song]:
    proxy = request.getproxies()
    search_results = requests.get(
        "https://rclyricsband.com/", params={"s": "%s %s" % (artists, title)}, proxies=proxy)
    search_soup = BeautifulSoup(search_results.text, 'html.parser')
    main = search_soup.find(id="main")
    if not main:
        return []
    articles = main.find_all("article")
    if not articles:
        return []
    for result in articles:
        try:
            title_link = result.find(class_="elementor-post__title").find("a")
        except Exception:
            continue
        info = title_link.get_text()
        if not name_comparison(info, info, title, artists):
            continue
        song_page = requests.get(title_link["href"])
        song_page_soup = BeautifulSoup(song_page.text, 'html.parser')
        lrc_download_button = song_page_soup.find(
            lambda tag: tag.name == "a" and "LRC Download" in tag.text)
        if not lrc_download_button:
            continue
        response = requests.get(lrc_download_button["href"], proxies=proxy)
        if not response.status_code == 200:
            continue
        return [Song(
            title=info,
            artists=info,
            target_title=title,
            target_artists=artists,
            lyric=response.text
        )]
    return []


def megalobiz_music_search(title: str, artists: str) -> List[Song]:
    proxy = request.getproxies()
    search_url = "https://www.megalobiz.com/search/all?%s" % parse.urlencode({
        "qry": f"{artists} {title}",
        "display": "more"
    })
    search_results = requests.get(search_url, proxies=proxy)
    soup = BeautifulSoup(search_results.text, 'html.parser')
    container = soup.find(id="list_entity_container")
    if not container:
        return []
    result_links = container.find_all(
        "a", class_="entity_name")

    for result_link in result_links:
        info = result_link.get_text()
        if not name_comparison(info, info, title, artists):
            continue
        url = f"https://www.megalobiz.com{result_link['href']}"
        possible_text = requests.get(url, proxies=proxy)
        soup = BeautifulSoup(possible_text.text, 'html.parser')

        div = soup.find("div", class_="lyrics_details")
        if not div:
            continue
        try:
            lrc = div.span.get_text()
        except Exception:
            continue

        return [Song(
            title=info,
            artists=info,
            target_title=title,
            target_artists=artists,
            lyric=lrc
        )]
    return []


if __name__ == "__main__":
    print(rentanadviser_music_search("I'm Not The Only One", "Sam Smith"))
    print(lyricsify_music_search("I'm Not The Only One", "Sam Smith"))
    print(rclyricsband_music_search("I'm Not The Only One", "Sam Smith"))
    print(megalobiz_music_search("I'm Not The Only One", "Sam Smith"))
