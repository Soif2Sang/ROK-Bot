from ctypes import windll

import win32gui
import win32ui
from PIL import Image


def game_screenshot():
    hwnd = win32gui.FindWindow(None, 'Rise of Kingdoms')

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #left, top, right, bot = win32gui.GetClientRect(hwnd)
    left, top, right, bot = win32gui.GetWindowRect(hwnd)
    print(win32gui.GetWindowRect(hwnd))
    if left<0:
        left=int(left*96/120)
        right=int(right*96/120)
        top=int(top*96/120)
        bot=int(bot*96/120)

    right=right-(15*96/120)
    bot=bot- (35*96/120)

    print(left,right)
    w = right - left
    h = bot - top

    # w *= 1.25
    # h *= 1.25
    w = int(w)
    h = int(h)

    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC  = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    saveBitMap = win32ui.CreateBitmap()
    saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)

    saveDC.SelectObject(saveBitMap)

    # Change the line below depending on whether you want the whole window
    # or just the client area.
    #result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 1)
    result = windll.user32.PrintWindow(hwnd, saveDC.GetSafeHdc(), 3)
    print(result)

    bmpinfo = saveBitMap.GetInfo()
    bmpstr = saveBitMap.GetBitmapBits(True)

    im = Image.frombuffer(
        'RGB',
        (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
        bmpstr, 'raw', 'BGRX', 0, 1)

    win32gui.DeleteObject(saveBitMap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
    print(result)
    if result == 1:
        print("#PrintWindow Succeeded")
        im.save("screenshot.png")

    return im


if __name__ == '__main__':
    game_screenshot()