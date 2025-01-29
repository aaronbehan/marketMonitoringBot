from pyautogui import *
import pyautogui
import time
import keyboard
import random
import win32api, win32con

# DOES NOT RUN ON VSCODE OR PYCHARM. ONLY RUNS ON IDLE

items_of_interest = ["goose friend", "gnoll", "forever prom queen", "crate of dynamite"]

while True:
    if keyboard.is_pressed('p'):
        search_bar = pyautogui.locateOnScreen('resources/searchbar.png')
        search_button = pyautogui.locateOnScreen('resources/searchbutton.png')
        time.sleep(0.5)

        if search_bar != None and search_button != None:
            for item in items_of_interest:

                pyautogui.click((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))  # moves mouse to X, Y coords then clicks
                time.sleep(0.3)
                pyautogui.doubleClick((search_bar.left + search_bar.width * 2), (search_bar.top + search_bar.height / 2))
                pyautogui.write(item)
                pyautogui.click((search_button.left + search_button.width / 2), (search_button.top + search_button.height / 2))  # moves mouse to X, Y coords then clicks
                
                time.sleep(2)
                if pyautogui.locateOnScreen(f'resources/{item}.png'):
                    print(f"i see the {item}")
                else:
                    print(f"i don't see the {item}")
    