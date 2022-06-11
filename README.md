# Derogan: Export Spotify Playlists to Apple Music

After overcoming the social stigma of ditching Spotify -- snappy, light, simple, well-designed -- for Apple Music -- slow, bloated, overwhelming, thrown-together -- I was surprised to find that both Spotify and Apple make it very difficult to migrate to a different service, or even to get a simple export of your tracks which can be imported to another service.

Nonetheless, Joe Rogan is a great incentive to not be on Spotify, so after realising that the cottage industry of web services designed to help you migrate (SongShift, TuneMyMusic, et al.) are unreliable and expensive, I figured out a quick hack.

Firstly we drag and drop all the tracks from a Spotify playlist to a plain text file. They turn into URLs. Then we crawl each link and strip out the metadata needed to identify the track with reasonable certainty in Apple Music's library. Then we use Selenium to authenticate with Apple Music's web player, and automatically add each track to our library one at a time.

## Prerequisites

* Python 3.x
* BeautifulSoup
* Selenium
* Chrome webdriver
* GetPass4

## Setup

1. Go to your Spotify playlist of choice.
2. Select all of the tracks.
3. Drag them to an empty text file.
4. The tracks will convert to Spotify URLs.
5. `$ pip install bs4`
6. `$ pip install selenium`
7. `$ pip install getpass4`
8. `$ brew install chromedriver --cask`

## spotify.py

Tell this file where your list of Spotify URLs is stored, and where you want your nicely-formatted JSON to go. Then run it in your terminal.

## apple_music.py

In your Python shell enter `from apple_music.py import *`, and then `migrate_songs()`
