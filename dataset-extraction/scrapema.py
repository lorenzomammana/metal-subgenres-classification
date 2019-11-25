import requests
import time
from bs4 import BeautifulSoup
import re
from requests.adapters import ProxyError
from string import ascii_lowercase
from urllib.request import Request, urlopen
from selenium.webdriver.support.ui import WebDriverWait
import selenium.webdriver
from selenium.webdriver.firefox.options import Options


proxies = open("proxies.txt", "r").readlines()


def change_proxy(count):
    return {"http": proxies[count].split("\n")[0]}


restart = True

missingbands = open('out.txt', 'r', encoding='utf-8')
missingbandslines = missingbands.read().splitlines()
missingbands.close()

options = Options()
options.headless = True
driver = selenium.webdriver.Firefox(options=options,
                                    executable_path='C:\\Users\\loren\\Desktop\\geckodriver-v0.26.0-win64'
                                                    '\\geckodriver.exe')

for band in missingbandslines:
    # proxy = {"http": "157.230.112.218:8080"}
    count_proxy = 0
    url = 'https://www.metal-archives.com/search?searchString='

    if band == "Infected rain":
        restart = False

    if restart:
        continue

    proxy = None

    while True:
        try:
            driver.get(url + band + '&type=band_name')
            time.sleep(3)
        except ProxyError:
            proxy = change_proxy(count_proxy)
            count_proxy += 1
            continue
        break

    soup = BeautifulSoup(driver.page_source, "html.parser")

    if soup.find("h1", {"class": "band_name"}) is not None:
        temp_out = open("manewgenres.csv", "a", encoding="utf-8")
        print(band)

        time.sleep(1)

        albums = BeautifulSoup(driver.page_source, "html.parser")

        band_stats = albums.find("div",  {"id": "band_stats"})

        band_genre_d = band_stats.findAll("dl")[1]
        genre = band_genre_d.findAll("dd")[0].text.replace(",", "")

        all_albums_table = albums.find("table", {"class": "display discog"})
        all_albums_tbody = all_albums_table.find("tbody")
        all_albums_rows = all_albums_tbody.findAll("tr")

        album_names = []
        year = -1000

        for album_row in all_albums_rows:
            all_albums_el = album_row.findAll('td')

            album_name = all_albums_el[0].text
            year = all_albums_el[2].text

            print(album_name, year, genre)

            album_names.append("'" + album_name.replace("'", "") + "'")

        if year != -1000:
            temp_out.write(band + ',"[' + ','.join(album_names) + ']",' + year + ',' + genre + '\n')

        temp_out.close()
        continue

    all_artists_table = soup.find("table", {"id": "searchResults"})

    if all_artists_table is None:
        continue

    all_artists = all_artists_table.findAll('a')

    for artist in all_artists[0:min(10, len(all_artists))]:
        link = artist['href']

        temp_out = open("manewgenres.csv", "a", encoding="utf-8")
        print(band)

        while True:
            try:
                driver.get(link)
                time.sleep(3)
            except ProxyError:
                proxy = change_proxy(count_proxy)
                count_proxy += 1
                continue
            break

        albums = BeautifulSoup(driver.page_source, "html.parser")

        band_stats = albums.find("div",  {"id": "band_stats"})

        try:
            band_genre_d = band_stats.findAll("dl")[1]
        except AttributeError:
            break

        genre = band_genre_d.findAll("dd")[0].text

        all_albums_table = albums.find("table", {"class": "display discog"})
        all_albums_tbody = all_albums_table.find("tbody")
        all_albums_rows = all_albums_tbody.findAll("tr")

        album_names = []
        year = -1000

        for album_row in all_albums_rows:
            all_albums_el = album_row.findAll('td')

            album_name = all_albums_el[0].text

            try:
                year = all_albums_el[2].text
            except IndexError:
                break

            album_names.append("'" + album_name.replace("'", "") + "'")
            print(album_name, year, genre)

        if year != -1000:
            temp_out.write(band + ',"[' + ','.join(album_names) + ']",' + year + ',' + genre + '\n')

        temp_out.close()
