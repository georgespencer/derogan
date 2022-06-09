from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
import time
import json

def gimme_dat_json(): # extracts the JSON object saved to text file in spotify.py
    with open('path/to/your/playlist/as/json.txt') as f:
        json_data = json.loads(f)
    return json_data

def create_session(): # creates a session and points it to the Apple Music auth page
    driver = webdriver.Chrome(service_args=["--verbose", "--log-path=apple_music_automaton.log"])
    driver.get("https://beta.music.apple.com/includes/commerce/authenticate?product=music")
    return driver

def login_to_apple_music(driver): # signs in to Apple Music and handles 2FA, redirects WebDriver to the main Apple Music page
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title^='Sign In with your Apple']")))
    user_name_field = driver.find_element_by_css_selector("input#account_name_text_field")
    user_name_field.send_keys("your-apple-music-user-name")
    time.sleep(5)
    user_name_field.send_keys(Keys.ENTER)
    time.sleep(5)
    password_field = driver.find_element_by_css_selector("input[type='password']")
    password_field.send_keys("your-apple-music-password")
    time.sleep(5)
    password_field.send_keys(Keys.ENTER)
    time.sleep(5)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#char0")))
    input_field_one, input_field_two, input_field_three, input_field_four, input_field_five, input_field_six = driver.find_element_by_id("char0"), driver.find_element_by_id("char1"), driver.find_element_by_id("char2"), driver.find_element_by_id("char3"), driver.find_element_by_id("char4"), driver.find_element_by_id("char5")
    twofa = str(input("Enter your 6-digit code\n"))
    input_field_one.send_keys(twofa[0])
    input_field_two.send_keys(twofa[1])
    input_field_three.send_keys(twofa[2])
    input_field_four.send_keys(twofa[3])
    input_field_five.send_keys(twofa[4])
    input_field_six.send_keys(twofa[5])
    time.sleep(5)
    driver.find_element_by_xpath("//button[contains(@id,'trust-browser')]").click()
    time.sleep(10)
    driver.get("https://beta.music.apple.com")
    return driver

def verify_presence_of_playlist(driver): # checks to ensure that there is a playlist to add tracks to
    playlist_name = accept_playlist_name_as_input()
    sidebar = driver.find_element_by_css_selector("div.navigation__scrollable-container")
    list_of_playlists = sidebar.find_element_by_css_selector("ul[aria-label='Playlists'] > li")
    for list_item in list_of_playlists:
        my_span = list_item.find_element_by_css_selector("span")
        if my_span.text.lower() == playlist_name.lower():
            my_message = 'Playlist Found'
            break
        else:
            pass
    if my_message != 'Playlist Found':
        return "Playlist not found"
    else:
        return my_message
    
def accept_playlist_name_as_input(): # asks user to enter the name of their playlist
    playlist_name = str(input("Enter the name of your Apple Music playlist:\n"))
    return playlist_name

def find_album_listings(driver): # finds the container DIV for albums returned by search
    main_page = driver.find_element_by_css_selector("main.svelte-xqntb3")
    section_divs = main_page.find_elements_by_css_selector("div[class^='section']")
    for counter, div in enumerate(section_divs):
        try:
            all_h2s = div.find_elements_by_css_selector("h2")
            for heading in all_h2s:
                if heading.text == 'Albums':
                    my_div = section_divs[counter]
                else:
                    pass
        except:
            pass
    return my_div

def select_best_match(driver, album, album_container): # finds the album which best matches the name from our JSON
    matches = album_container.find_elements_by_css_selector("div.product-lockup__title ")
    album_name = album.lower()
    for counter, match in enumerate(matches):
        if match.text.lower() == album_name:
            best_match = matches[counter]
        else:
            pass
    if best_match != None or '':
        return best_match
    else:
        for counter, match in enumerate(matches):
            if album_name in match.text.lower():
                best_match = matches[counter]
            else:
                pass
    return best_match

def identify_song(driver, song): # finds the song which best matches the song name from our JSON
    elements_containing_songs = driver.find_elements_by_class_name("songs-list-row")
    song_name = song.lower()
    for counter, element in enumerate(elements_containing_songs):
        attempted_match = element.find_elements_by_class_name("songs-list-row__song-name")
        if attempted_match.text.lower() == song_name:
            my_song_row = element[counter]
        else:
            pass
    if my_song_row != None or '':
        return my_song_row
    else:
        for counter, element in enumerate(elements_containing_songs):
            attempted_match = element.find_elements_by_class_name("songs-list-row__song-name")
            if song_name in attempted_match.text.lower():
                my_song_row = element[counter]
            else:
                pass
    return my_song_row

def click_more_button(driver, song_row): # clicks the contextual menu button
    button = song_row.find_elemenet_by_css_selector("button.more-button")
    button.click()
    return ("Button clicked")

# def add_song_to_playlist(driver, song, playlist_name):
#     WebDriverWait(driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR("ul.contextual-menu__items"))))
#     add_to_playlist_button = driver.find_elements_by_css_selector("button[title='Add to Playlist']")
#     add_to_playlist_button.click()
#     WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR("ul.contextual-menu__items--nested-active"))))
#     my_specific_playlist_bitton = driver.find_elements_

# def search_for_albums(driver):
#     my_playlist = gimme_dat_json()
#     search_input = driver.find_element_by_class_name("search-input__text-field")

#     for artist in my_playlist.keys():
#         for album in my_playlist[artist].keys():
#             album_search_string = f'{album} {artist}'
#             print(album_search_string)
#             search_input.send_keys(album_search_string)
#             time.sleep(1)
#             search_input.send_keys(Keys.ENTER)
#             WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR("main.svelte-xqntb3"))))
#             album_container = find_album_listings(driver)
#             match = select_best_match(driver, album, album_container)
#             match.click()
#             for song in my_playlist[artist][album]["Tracks"]:
#                 this_song = identify_song(driver, song)
#                 click_more_button(driver, this_song)
