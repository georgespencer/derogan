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

def final_selenium_script(): # Logs in to Apple Music using Selenium. Asks the user to enter 2FA code in the Terminal.
    driver = webdriver.Chrome(service_args=["--verbose", "--log-path=apple_music_automaton.log"])
    driver.get("https://beta.music.apple.com/login")
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[src^='/includes/commerce/authenticate?product=music']")))
    WebDriverWait(driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.CSS_SELECTOR,"iframe[title^='Sign In with your Apple']")))
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input#account_name_text_field"))).send_keys("your-apple-music-email-address-here")
    time.sleep(5)
    driver.find_element_by_css_selector("input#account_name_text_field").send_keys(Keys.ENTER)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, "input[type='password']"))).send_keys("your-apple-music-password-here")
    time.sleep(5)
    driver.find_element_by_css_selector("input[type='password']").send_keys(Keys.ENTER)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,"input#char0")))
    print("Input ready!")
    input_field_one, input_field_two, input_field_three, input_field_four, input_field_five, input_field_six = driver.find_element_by_id("char0"), driver.find_element_by_id("char1"), driver.find_element_by_id("char2"), driver.find_element_by_id("char3"), driver.find_element_by_id("char4"), driver.find_element_by_id("char5")
    twofa = str(input("Enter your 6-digit code\n"))
    input_field_one.send_keys(twofa[0])
    input_field_two.send_keys(twofa[1])
    input_field_three.send_keys(twofa[2])
    input_field_four.send_keys(twofa[3])
    input_field_five.send_keys(twofa[4])
    input_field_six.send_keys(twofa[5])
    time.sleep(5)
    trust_button = driver.find_element_by_xpath("//button[contains(@id,'trust-browser')]")
    time.sleep(5)
    trust_button.click()
