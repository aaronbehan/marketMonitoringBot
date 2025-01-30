from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import pytesseract
from PIL import Image
import requests

# DOES NOT RUN ON VSCODE OR PYCHARM. ONLY RUNS ON IDLE


def send_discord_message(message):
    url = "****************************************************************" # censored

    # The message to send
    payload = {
        "content" : message
    }

    # Needed to pass security check possibly
    headers = {
        "Authorization" : "**********************************************************************" # censored
    }

    res = requests.post(url, payload, headers=headers)


furni_of_interest = {
    "skeleton raider" : 1000,
    "kraken" : 1000,
    "scorching dragon": 1000,
    "gnoll": 10,
    "dynamite crate": 60,
    "forever prom queen" : 100,
    "user clicks furni" : 3,
    "bear owl" : 5,
    "lucifer's hellhound": 35,
    "bigfoot": 25,
    "royal tea lady" : 45,
    "mummy pharaoh" : 10
    }

iterations = 0

while keyboard.is_pressed("p") == False:

    search_bar = pyautogui.locateOnScreen('resources/searchbar.png')
    search_button = pyautogui.locateOnScreen('resources/searchbutton.png')
    time.sleep(0.5)

    if search_bar != None and search_button != None:
        for key, item in furni_of_interest.items():
            
            # Entering search parametres and clicking search
            pyautogui.click((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))  # moves mouse to X, Y coords then clicks
            time.sleep(0.3)
            pyautogui.doubleClick((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))
            pyautogui.write(key)
            pyautogui.click((search_button.left + search_button.width / 2), (search_button.top + search_button.height / 2))
            print("Sleeping for 4 seconds")
            time.sleep(7)
            
            # Checking top search results against PNG file
            if pyautogui.locateOnScreen(f'resources/no items found.png') != None:
                print(f"No search results for {key}")
                continue

            try:
                item_screen_loc = pyautogui.locateOnScreen(f'resources/{key}.png')  # PUT THIS INSIDE TRY EXCEPT AND SEND A NOTIFICATION IF IT FAILS
            except OSError:  # error occurs when folder does not find the corresponding image 
                item_screen_loc = None
                print(f"No image could be found for this furni in resources folder. This error may indicate that {key} is listed.")
                send_discord_message(f"Search results for {key} in marketplace has returned something.")
                screenshot = pyautogui.screenshot(f"{key}screenshot.png")


            if item_screen_loc != None:
                print(f"i see the {key.upper()}")
                # Pyautogui takes screenshot of price
                screenshot = pyautogui.screenshot(f"{key}screenshot.png", region=(item_screen_loc.left + item_screen_loc.width, item_screen_loc.top, 80, 40))
                print("Screenshot taken")

                # Converting screenshot into string using pytesseract
                img_file = f"{key}screenshot.png"
                img = Image.open(img_file)
                ocr_result = pytesseract.image_to_string(img)

                # Convert string into list and look for word: "price"
                result_as_list = ocr_result.split()
                print(f"OCR result = {result_as_list}")
                for word in result_as_list:
                    if "ice" in word.lower():  # sometimes the whole word is not successfully read by pytesseract
                        index = result_as_list.index(word)
                        price = result_as_list[index + 1]
                        print(f"discovered price: {price}")

                        # Comparing price to desired amount to pay
                        try:  # Sometimes OCR will mistake numbers for alphabetical characters.
                            price = int(price)
                            if price <= item:
                                print(f"{key} - Current price of {price} is lower asking price of {item} ")
                                send_discord_message(f"{key} currently listed for {price} on marketplace.")
                                furni_of_interest[key] -= 10000  # not such an elegant way of removing the item from the equation
                        except ValueError:
                            print("The price was not interpreted as a number to be casted into an integer.")
                    elif "ave" in word.lower():
                        break  # we do not want to risk the for loop mistaking "average price" as the actual current price and mistakenly sending me a notification
                
            else:
                print(f"Search results returned do not contain {key}")

    iterations += 1
    print(f"number of {iterations}")
