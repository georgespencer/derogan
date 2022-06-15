import os
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from getpass4 import getpass
import time
import json
import difflib

def get_user_credentials():
    #apple_music_email = str(input("Enter the email address associated with your Apple Music account:\n"))
    #apple_music_password = str(getpass("Enter the password associated with your Apple Music account:\n"))
    #playlist_name = accept_playlist_name_as_input()
    apple_music_email = os.environ.get('APPLE_MUSIC_EMAIL')
    apple_music_password = os.environ.get('APPLE_MUSIC_PASSWORD')
    playlist_name = os.environ.get('SPOTIFY_PLAYLIST')
    return (apple_music_email, apple_music_password, playlist_name)

def gimme_dat_json():
    with open('app/static/dump.txt') as f:
        json_data = json.load(f)
    return json_data

def create_session():
    driver = webdriver.Chrome(service_args=["--verbose", "--log-path=apple_music_automaton.log"])
    driver.set_window_size(1100,750) # makes a smaller window
    #driver.set_window_position(1500,0) # moves it to my second screen
    driver.get("https://beta.music.apple.com/includes/commerce/authenticate?product=music")
    return driver

def login_to_apple_music(driver, username, password):
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title^='Sign In with your Apple']")))
    user_name_field = driver.find_element_by_css_selector("input#account_name_text_field")
    user_name_field.send_keys(username)
    time.sleep(1)
    user_name_field.send_keys(Keys.ENTER)
    time.sleep(1)
    password_field = driver.find_element_by_css_selector("input[type='password']")
    password_field.send_keys(password)
    time.sleep(1)
    password_field.send_keys(Keys.ENTER)
    twofa = str(input("Enter your 6-digit code\n"))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#char0")))
    input_field_one, input_field_two, input_field_three, input_field_four, input_field_five, input_field_six = driver.find_element_by_id("char0"), driver.find_element_by_id("char1"), driver.find_element_by_id("char2"), driver.find_element_by_id("char3"), driver.find_element_by_id("char4"), driver.find_element_by_id("char5")
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
    time.sleep(5)
    return driver

def verify_presence_of_playlist(driver, playlist_name):
    wait_for_css_selector(driver, 'div.navigation__scrollable-container')
    sidebar = driver.find_element_by_css_selector("div.navigation__scrollable-container")
    list_of_playlists = sidebar.find_elements_by_css_selector("ul[aria-label='Playlists'] > li")
    for list_item in list_of_playlists:
        my_span = list_item.find_element_by_css_selector("span")
        if my_span.text.lower() == playlist_name.lower():
            print("Playlist found")
            return True
        else:
            pass
    return False

def accept_playlist_name_as_input():
    playlist_name = str(input("Enter the name of your Apple Music playlist:\n"))
    return playlist_name

def find_album_listings(driver):
    main_page = driver.find_element_by_css_selector("main[data-testid='main']")
    section_divs = main_page.find_elements_by_css_selector("div[class^='section']")
    print(f'Found {len(section_divs)} section divs')
    for counter, div in enumerate(section_divs):
        try:
            all_h2s = div.find_elements_by_css_selector("h2")
            for heading in all_h2s:
                if heading.text == 'Albums':
                    return section_divs[counter]
                else:
                    print(f'Not {heading.text}')
                    pass
        except Exception as booboo:
            print(f'Error: {booboo}')
            pass

def scroll_next_page(driver):
    scroll_button = driver.find_element_by_css_selector("button[aria-label='Next Page']")
    scroll_button.click()

def evaluate_match(target_name, match_name):
    return (match_name, difflib.SequenceMatcher(None, target_name, match_name).ratio())

def pick_best_album_match(driver, album, album_container):
    matches = album_container.find_elements_by_css_selector("div.product-lockup__title ")
    analysed_matches = []
    for counter, match in enumerate(matches):
        this_match = evaluate_match(album, match.text)
        this_analysed_match = (this_match[0], this_match[1])
        analysed_matches.append(this_analysed_match)
    analysed_matches.sort(key=lambda x:x[1], reverse=True)
    if analysed_matches[0][1] < 0.9:
        scroll_next_page(driver)
    for counter, match in enumerate(matches):
        if match.text == analysed_matches[0][0]:
            print(f'Found {analysed_matches[0][0]}, {(analysed_matches[0][1])*100}% match for {album}')
            return matches[counter]
        else:
            pass

def identify_song(driver, song):
    elements_containing_songs = driver.find_elements_by_css_selector("div[data-testid='track-list-item']")
    song_name = song.lower()
    for counter, element in enumerate(elements_containing_songs):
        song_title = element.find_element_by_css_selector("div[data-testid='track-title']")
        if song_title.text.lower() == song_name:
            my_song_row = elements_containing_songs[counter]
            break
        else:
            pass
    if my_song_row != None or '':
        return my_song_row
    else:
        for counter, element in enumerate(elements_containing_songs):
            song_title = element.find_element_by_css_selector("div[data-testid='track-title']")
            if song_name in song_title.text.lower():
                my_song_row = elements_containing_songs[counter]
                break
            else:
                pass
        return my_song_row

def click_more_button(driver, song_row):
    button = song_row.find_element_by_css_selector("button.more-button")
    button.click()
    return ("Button clicked")

def verify_presence_of_context_menu(driver):
    try:
        context_menu = WebDriverWait(driver,10).until(EC.presence_of_element_located((By.XPATH, "/html/body/amp-contextual-menu")))
        return context_menu
    except Exception as booboo:
        return booboo

def click_contextual_menu_button(driver, button_title_text):
    try:
        context_menu = verify_presence_of_context_menu(driver)
        shadow_root_object = expand_shadow_element(driver, context_menu)
        interpolated_string = f"button[title=\'{button_title_text}\']"
        button = shadow_root_object.find_element(By.CSS(interpolated_string))
        button.click()
        print(f"Clicked button for {button_title_text}")
        return True
    except Exception as booboo:
        return booboo

def add_songs_to_playlist(driver, songs, playlist_name): # return
    elements_containing_songs = driver.find_elements_by_css_selector("div[data-testid='track-list-item']")
    for song in songs:
        for counter, element in enumerate(elements_containing_songs):
            potential_match = element.find_element_by_css_selector("div[data-testid='track-title']")





def add_song_to_playlist(driver, song, playlist_name):
    try:
        this_song = identify_song(driver, song)
        print("Identified song")
        click_more_button(driver, this_song)
        print("clicked more button")
        click_contextual_menu_button(driver, 'Add to Playlist')
        print("click contextual menu button")
        click_contextual_menu_button(driver, playlist_name)
        time.sleep(1)
        return True
    except Exception as booboo:
        return booboo

def search_for_string(driver, search_query):
    search_input = driver.find_element_by_class_name("search-input__text-field")
    search_input.clear()
    search_input.send_keys(search_query)
    print(f"Entered {search_query}")
    time.sleep(2)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    return driver

def load_matching_album(driver, album_name):
    album_container = find_album_listings(driver)
    analysed_matches = pick_best_album_match(driver, album_name, album_container)
    analysed_matches.click()

def expand_shadow_element(driver, element):
    shadow_root = driver.execute_script('return arguments[0].shadowRoot', element)
    return shadow_root

def wait_for_css_selector(driver, element):
    time.sleep(5)
    my_element = WebDriverWait(driver,20).until(EC.presence_of_element_located((By.CSS_SELECTOR,element)))
    return my_element.tag_name

def remove_song_from_json(my_json_playlist, artist, album, song):
    if len(my_json_playlist[artist][album]["Tracks"]) > 1:
        my_json_playlist[artist][album]["Tracks"].remove(song)
        return f'Removed {artist} - {song} from JSON'
    elif len(my_json_playlist[artist][album]["Tracks"]) == 1:
        my_json_playlist[artist][album]["Tracks"].remove(song)
        my_json_playlist[artist][album].pop("Tracks")
        my_json_playlist[artist].pop(album)
        my_return_string = f'Removed {artist} - {song} and {album} from JSON'
        if my_json_playlist[artist].keys() == 0:
            my_json_playlist.remove(artist)
            my_return_string = f'Removed {artist}, {song}, and {album} from JSON'
        else:
            pass
        return my_return_string

def migrate_songs():
    user_credentials = get_user_credentials()
    driver = create_session()
    login_to_apple_music(driver, user_credentials[0], user_credentials[1])
    my_json_playlist = gimme_dat_json()
    copy_of_json_playlist = my_json_playlist
    time.sleep(10)
    my_apple_music_playlist = verify_presence_of_playlist(driver, user_credentials[2])
    if my_apple_music_playlist == False:
        return f'Error: Playlist {user_credentials[2]} not found'
    else:
        for artist in list(my_json_playlist.keys()):
            for album in list(my_json_playlist[artist].keys()):
                album_search_string = f'{artist} - {album}'
                search_for_string(driver, album_search_string)
                print(f"Searched for {album_search_string}")
                wait_for_css_selector(driver, "main.svelte-xqntb3")
                print(f"Finished waiting for results to load")
                this_album = load_matching_album(driver, album)
                tracks_from_this_album = [ d for d in my_json_playlist[artist][album]["Tracks"] ]
                print(f"Finding {len(tracks_from_this_album)} tracks")
                for song in list(my_json_playlist[artist][album]["Tracks"]):
                    add_song_to_playlist(driver, song, user_credentials[2])
                    remove_song_from_json(copy_of_json_playlist, artist, album, song)
