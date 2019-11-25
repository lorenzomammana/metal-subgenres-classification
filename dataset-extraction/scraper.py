import requests
import urllib.request
import time
from bs4 import BeautifulSoup
import re
from requests.adapters import ProxyError
from string import ascii_lowercase

proxies = open("proxies.txt", "r").readlines()


def change_proxy(count):
    return {"http": proxies[count].split("\n")[0]}


restart = False

for c in ['19']:
    # proxy = {"http": "157.230.112.218:8080"}
    count_proxy = 0
    url = 'http://www.darklyrics.com/'

    proxy = None

    while True:
        try:
            response = requests.get(url + c + '.html', proxies=proxy)
        except ProxyError:
            proxy = change_proxy(count_proxy)
            count_proxy += 1
            continue
        break

    soup = BeautifulSoup(response.text, "html.parser")

    all_artists_div = soup.find("div", {"class": "cont"})
    all_artists = all_artists_div.findAll('a')

    for artist in all_artists:
        link = artist['href']
        band_name = artist.text.replace(",", " ")

        temp_out = open("temp.csv", "a", encoding="utf-8")
        print(band_name)
        time.sleep(2)

        while True:
            try:
                albums = requests.get(url + link, proxies=proxy)
            except ProxyError:
                proxy = change_proxy(count_proxy)
                count_proxy += 1
                continue
            break

        albums = BeautifulSoup(albums.text, "html.parser")
        all_albums_div = albums.findAll("div", {"class": "album"})

        for album in all_albums_div:
            all_albums = album.findAll('a')

            try:
                link = all_albums[0]['href']
            except IndexError:
                continue

            try:
                album_name = album.find("h2").text.split('"')[1].replace('"', "").replace(",", " ")
                year = album.find("h2").text.split('"')[2].replace(' (', "").replace(")", "")
            except IndexError:
                continue

            print(album_name, year)
            time.sleep(2)

            while True:
                try:
                    songs = requests.get(url + link, proxies=proxy)
                    songs = BeautifulSoup(songs.text, "html.parser")

                    if songs.find("div", {"class": "note"}) is not None:
                        songs.find("div", {"class": "note"}).decompose()

                    if songs.find("div", {"class": "thanks"}) is not None:
                        songs.find("div", {"class": "thanks"}).decompose()
                except ProxyError:
                    proxy = change_proxy(count_proxy)
                    print(proxy)
                    count_proxy += 1
                    continue
                break

            try:
                all_lyrics = songs.find("div", {"class": "lyrics"})
                all_lyrics.findAll("a")[-1].decompose()
            except AttributeError:
                continue

            all_lyrics = all_lyrics.text.replace(",", "")
            all_lyrics = all_lyrics.replace('"', '')
            song_lyrics = ""
            title = ""

            for lyric in all_lyrics.split("\n"):

                if lyric == '':
                    continue

                if re.match("[0-9]*\.", lyric) is not None:
                    if title != "":
                        temp_out.write(band_name + ',' + album_name + ',' + year + ',' + title + ',"' + song_lyrics + '"\n')

                    title = lyric.split(".")[1].strip()
                    song_lyrics = ""
                else:
                    song_lyrics += lyric + " "

            temp_out.write(band_name + ',' + album_name + ',' + year + ',' + title + ',"' + song_lyrics + '"\n')
            time.sleep(2)

        temp_out.close()
