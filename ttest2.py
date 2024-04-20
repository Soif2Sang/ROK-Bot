from time import sleep
from typing import Literal

import pyautogui
import win32api
import win32con
import win32gui
import win32process
from cv2 import (COLOR_BGR2HSV, COLOR_BGR2RGB, TM_CCOEFF_NORMED, cvtColor,
                 inRange, matchTemplate, minMaxLoc)
from numpy import array, ndarray, where

from ttest import game_screenshot
from utils.resources import ImageSingleton


def click(x, y):
    # Get current cursor position
    x1, y1 = win32api.GetCursorPos()

    # Set cursor position to the desired coordinates
    win32api.SetCursorPos((x, y))

    # Send a left mouse button down event
    handle = win32gui.FindWindow(None, 'Rise of Kingdoms')
    print("Window `{0:s}` handle: 0x{1:016X}".format('Rise of Kingdoms', handle))
    if not handle:
        print("Invalid window handle")
        return
    remote_thread, _ = win32process.GetWindowThreadProcessId(handle)
    win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
    prev_handle = win32gui.SetFocus(handle)

    for i in range(2):
        sleep(0.2)
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y)

        # Send a left mouse button up event
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y)

    # Restore cursor position
    pyautogui.scroll(-1000)
    win32api.SetCursorPos((x1, y1))


# Call the click function with desired coordinates
# click(500, 500)

images = ImageSingleton()
def find_img(filename, confidence, pil_image=None):
    if not pil_image:
        pil_image = game_screenshot()
    cv_image = array(pil_image)
    cv_image = cvtColor(cv_image, COLOR_BGR2RGB)
    img_to_find = images.get_file_name(filename)
    result = matchTemplate(cv_image, img_to_find, TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = minMaxLoc(result)
    if max_val > confidence:
        return max_loc[0], max_loc[1]
    else:
        return


def get_game_pos():
    left, top, right, bot = win32gui.GetWindowRect(get_game_handle())
    return left + 5, top + 30, right + 5, bot + 30
def get_game_handle():
    return win32gui.FindWindow(None, 'Rise of Kingdoms')

def set_game_focus(handle):
    print("Window `{0:s}` handle: 0x{1:016X}".format('Rise of Kingdoms', handle))
    if not handle:
        print("Invalid window handle")
        return
    remote_thread, _ = win32process.GetWindowThreadProcessId(handle)
    win32process.AttachThreadInput(win32api.GetCurrentThreadId(), remote_thread, True)
    prev_handle = win32gui.SetFocus(handle)

def zoom_out():
    left, top, right, bot = get_game_pos()
    pyautogui.moveTo(left + 1280/2, top + 720/2)
    set_game_focus(get_game_handle())
    pyautogui.scroll(-1000)

# while find_img("pc\\loop", 0.8):
#     zoom_out()


def swipe(direction: Literal['up', 'down', 'left', 'right']):
    left, top, right, bot = get_game_pos()

    pyautogui.moveTo(left + 1280 / 2, top + 720 / 2)
    set_game_focus(get_game_handle())
    x, y = left + 1280 / 2, top + 720 / 2
    if direction == 'up':
        y += 400
    elif direction == 'down':
        y -= 400
    elif direction == 'left':
        x -= 500
    elif direction == 'right':
        x += 500
    pyautogui.dragTo(button='left', x=x,y=y, duration=0.4)

icons = []

if __name__ == '__main__':
    # game_screenshot()
    print(find_img(filename="pc\\checkpoint_star", confidence=0.9))
#
# for i in range(14):
#     c = find_img(filename=f"GemDeposit{i}", pil_image=s, confidence=0.75)
#     print(c)
#     if c:
#         cord = c
#
#
# cord = find_img(filename=f"pc\\gem_icon_mid", pil_image=s, confidence=0.75)
#
# print(f"{cord=}")
# left, top, right, bot = get_game_pos()
# pyautogui.moveTo(left, top)
# pyautogui.moveRel(xOffset=cord[0], yOffset=cord[1])
# pyautogui.click()
# game_screenshot()
#
# swipe("up")
# swipe("right")
#
