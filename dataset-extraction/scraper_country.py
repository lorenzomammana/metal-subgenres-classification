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

for c in list(ascii_lowercase) + ['19']:
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

    artist_country = list(filter(None, all_artists_div.text.split("\n")))
    count = 0

    for artist in all_artists:
        link = artist['href']
        band_name = artist_country[count]
        count += 1
        country = "NONE"
        if "(" in band_name and ")" in band_name:
            country = band_name.split("(")[1].split(")")[0]
            band_name = band_name.split("(")[0].strip()
        else:
            continue

        if country == "USA":
            country = "United states"

        temp_out = open("bandalbum.csv", "a", encoding="utf-8")
        print(band_name, "(", country, ")")
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
            temp_out.write(band_name + "," + album_name + "," + country + "\n")
            time.sleep(2)

        temp_out.close()
