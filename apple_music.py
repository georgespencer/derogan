from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from getpass4 import getpass
import time
import json

def get_user_credentials():
    apple_music_email = str(input("Enter the email address associated with your Apple Music account:\n"))
    apple_music_password = str(getpass("Enter the password associated with your Apple Music account:\n"))
    return (apple_music_email, apple_music_password)

def gimme_dat_json():
    with open('app/static/dump.txt') as f:
        json_data = json.load(f)
    return json_data

def create_session():
    driver = webdriver.Chrome(service_args=["--verbose", "--log-path=apple_music_automaton.log"])
    driver.get("https://beta.music.apple.com/includes/commerce/authenticate?product=music")
    return driver

def login_to_apple_music(driver, username, password):
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title^='Sign In with your Apple']")))
    user_name_field = driver.find_element_by_css_selector("input#account_name_text_field")
    user_name_field.send_keys(username)
    time.sleep(5)
    user_name_field.send_keys(Keys.ENTER)
    time.sleep(5)
    password_field = driver.find_element_by_css_selector("input[type='password']")
    password_field.send_keys(password)
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

def verify_presence_of_playlist(driver):
    playlist_name = accept_playlist_name_as_input()
    sidebar = driver.find_element_by_css_selector("div.navigation__scrollable-container")
    list_of_playlists = sidebar.find_elements_by_css_selector("ul[aria-label='Playlists'] > li")
    for list_item in list_of_playlists:
        my_span = list_item.find_element_by_css_selector("span")
        if my_span.text.lower() == playlist_name.lower():
            my_message = 'Playlist Found'
            break
        else:
            pass
    if my_message != 'Playlist Found':
        return (False, playlist_name)
    else:
        return (True, playlist_name)

def accept_playlist_name_as_input():
    playlist_name = str(input("Enter the name of your Apple Music playlist:\n"))
    return playlist_name

def find_album_listings(driver):
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

def select_best_match(driver, album, album_container):
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
        return True
    except Exception as booboo:
        return booboo

def add_song_to_playlist(driver, song, playlist_name):
    try:
        this_song = identify_song(driver, song)
        click_more_button(driver, this_song)
        click_contextual_menu_button(driver, 'Add to Playlist')
        click_contextual_menu_button(driver, playlist_name)
        time.sleep(1)
        return True
    except Exception as booboo:
        return booboo

def search_for_string(driver, search_query):
    search_input = driver.find_element_by_class_name("search-input__text-field")
    search_input.send_keys(search_query)
    search_input.send_keys(Keys.ENTER)
    time.sleep(2)
    return driver

def load_matching_album(driver, album_name):
    album_container = find_album_listings(driver)
    match = select_best_match(driver, album_name, album_container)
    match.click()
    return driver

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
        my_json_playlist[artist][album].remove("Tracks")
        my_json_playlist[artist].remove(album)
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
    my_apple_music_playlist = verify_presence_of_playlist(driver)
    if my_apple_music_playlist[0] == False:
        return f'Error: Playlist {my_apple_music_playlist[1]} not found'
    else:
        for artist in my_json_playlist.keys():
            for album in my_json_playlist[artist].keys():
                album_search_string = f'{artist} - {album}'
                search_for_string(driver, album_search_string)
                wait_for_css_selector(driver, "main.svelte-xqntb3")
                load_matching_album(driver, album)
                for song in my_json_playlist[artist][album]["Tracks"]:
                    add_song_to_playlist(driver, song, my_apple_music_playlist[1])
                    remove_song_from_json(my_json_playlist, artist, album, song)
