from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con
import pytesseract
from PIL import Image


# DOES NOT RUN ON VSCODE OR PYCHARM. ONLY RUNS ON IDLE

items_of_interest = ["gnoll"]

while True:
    if keyboard.is_pressed('p'):
        search_bar = pyautogui.locateOnScreen('resources/searchbar.png')
        search_button = pyautogui.locateOnScreen('resources/searchbutton.png')
        time.sleep(0.5)

        if search_bar != None and search_button != None:
            for item in items_of_interest:
                
                # Entering search parametres and clicking search
                pyautogui.click((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))  # moves mouse to X, Y coords then clicks
                time.sleep(0.3)
                pyautogui.doubleClick((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))
                pyautogui.write(item)
                pyautogui.click((search_button.left + search_button.width / 2), (search_button.top + search_button.height / 2))
                print("Sleeping for 4 seconds")
                time.sleep(4)
                
                # Checking top search results against PNG file
                item_location = pyautogui.locateOnScreen(f'resources/{item}.png')

                if item_location != None:
                    print(f"i see the {item}")
                    # Pyautogui takes screenshot of price
                    screenshot = pyautogui.screenshot("screenshot.png", region=(item_location.left + item_location.width, item_location.top, 80, 40))
                    print("Screenshot taken")

                    # Converting screenshot into string using pytesseract
                    img_file = "screenshot.png"
                    img = Image.open(img_file)
                    ocr_result = pytesseract.image_to_string(img)
                    print(f"ocr_result = {ocr_result}")

                    # Converting string into list and looking for word: "price"
                    result_as_list = ocr_result.split()
                    print(result_as_list)
                    for word in result_as_list:
                        if word.lower() == "price:":
                            index = result_as_list.index(word)
                            price = result_as_list[index + 1]
                            print(f"the pricerino is {price}")
                            break  # only interested in the first instance of price
                    
                else:
                    print(f"i don't see the {item}")


    
