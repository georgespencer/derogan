import requests
from bs4 import BeautifulSoup
import json

list_of_urls = []

def parse_track_links():  # opens a .txt file of Spotify URLs (new line separated), strips line feeds, and populates a list with each URL
    with open('path/to/your/plain/text/playlist.txt') as f:
        for line in f:
            d = line.strip('\n')
            list_of_urls.append(d)
            print(d)
    return len(list_of_urls)

def ingest_page(url):     # receives a Spotify URL and returns the markup from Spotify's web player with beautiful soup
    reqs = requests.get(url)
    soup = BeautifulSoup(reqs.text, 'html.parser')
    return soup

def populate_artists(soup): # receives the beautiful soup markup and strips the artist from the <title> tag
    page_title = soup.find('title').get_text()
    left = 'by '
    right = ' |'
    return page_title[page_title.index(left)+len(left):page_title.index(right)]

def populate_title(soup): # receives the beautiful soup markup and returns the contents of the meta 'og:title' tag -- either the title of the track or the record
    return soup.find(property="og:title")['content']

def ingest_album_page(soup):  # receives the beautiful soup markup for a track, locates the meta 'music:album' tag, ingests the album page, and returns the beautiful soup markup for it
    album_link = soup.find(property="music:album")['content']
    d = ingest_page(album_link)
    return d

def crawl_spotify():  # uses a plain text list of Spotify URLs to crawl spotify's web player, strip out useful metadata, and save sensibly-organised JSON to a plain text file
    list_of_iterated_artists = []
    list_of_iterated_albums = []
    counter = parse_track_links()
    final_dict = {}
    i = 0
    while len(list_of_urls) >= 1:
        try:
            for count, value in enumerate(list_of_urls):
                i += 1
                try:
                    progress = round((100 * i / counter),2)
                    ingested_page = ingest_page(value)
                    ingested_album_page = ingest_album_page(ingested_page)
                    artist = populate_artists(ingested_page)
                    track = populate_title(ingested_page)
                    album = populate_title(ingested_album_page)
                    uid = f"{artist}-{album}"
                    if artist in list_of_iterated_artists:
                        if uid in list_of_iterated_albums:
                            final_dict[artist][album]["Tracks"].append(track)
                        else:
                            album_and_track = { album: { "Tracks": [track] }}
                            final_dict[artist].update(album_and_track)
                            list_of_iterated_albums.append(uid)
                    else:
                        artist_and_album_and_track = { artist: { album: { "Tracks": [track] }}}
                        final_dict.update(artist_and_album_and_track)
                        list_of_iterated_artists.append(artist)
                        list_of_iterated_albums.append(uid)
                    print(f'{progress}%')
                    list_of_urls.pop(count)
                except Exception as booboo:
                    print(f"Exception at {count} for {value}: {booboo}")
                    pass
        except KeyboardInterrupt:
            pass
    f = open('path/to/your/blank/file.txt', "w")
    f.write(json.dumps(final_dict))
    f.close()
    return(final_dict)
