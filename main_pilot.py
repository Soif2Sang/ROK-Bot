import flet as ft

from src.utils.functions import get_all_vms_running_ld
import cv2
import numpy as np
import subprocess
from PIL import Image
import io
import time
import pygetwindow as gw
import win32gui
import win32con

try:
    # Path to the back.png image
    target_image_path = 'E:/gems by hand/back.png'

    # Full path to ADB executable
    adb_path = "E:/platform-tools/adb.exe"

    # LDPlayer window name
    emulator_window_name = "LDPlayer"


    # Function to capture a screenshot from the emulator using ADB
    def capture_screenshot():
        result = subprocess.run([adb_path, 'exec-out', 'screencap', '-p'], stdout=subprocess.PIPE)
        img_data = result.stdout
        image = Image.open(io.BytesIO(img_data))
        return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)


    # Function to check if the target image is on the screen with a similarity threshold of 0.8
    def is_image_on_screen(screen, target_image, threshold=0.8):
        result = cv2.matchTemplate(screen, target_image, cv2.TM_CCOEFF_NORMED)
        _, max_val, _, _ = cv2.minMaxLoc(result)
        return max_val >= threshold


    # Function to force the emulator window to the front and make it stay there
    def force_window_to_top(window):
        hwnd = window._hWnd

        # Ensure window is not minimized
        if win32gui.IsIconic(hwnd):
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)

        # Force the window to stay on top
        win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 0, 0, 0, 0,
                              win32con.SWP_NOMOVE | win32con.SWP_NOSIZE | win32con.SWP_SHOWWINDOW)

        # Ensure it stays on top
        win32gui.SetForegroundWindow(hwnd)
        win32gui.BringWindowToTop(hwnd)
        win32gui.SetFocus(hwnd)


    # Load the target image
    target_image = cv2.imread(target_image_path, cv2.IMREAD_COLOR)

    while True:
        screen_image = capture_screenshot()
        emulator_window = gw.getWindowsWithTitle(emulator_window_name)[0]

        if is_image_on_screen(screen_image, target_image, threshold=0.8):
            try:
                force_window_to_top(emulator_window)  # Forcefully bring the window to the front and make it stay there
            except Exception as e:
                print(f"Error bringing window to front: {e}")
        else:
            emulator_window.minimize()

        time.sleep(1)

except Exception as e:
    print(f"An error occurred: {e}")
    input("Press Enter to exit...")  # Prevent the window from closing immediately



class PilotedEmulator(ft.Row):
    def __init__(self, vm_index:str,  vm_name: str):
        super().__init__()
        self.vm_index = vm_index
        self.vm_name = vm_name

    def on_click(self, e):
        print(f"Clicked on {self.vm_index} {self.vm_name}")


def main(page: ft.Page):
    def refresh(e):
        page.controls = [page.controls[0]]
        vms = get_all_vms_running_ld()

        for vm in vms:
            page.controls.append(ft.Text(value=vm))
        page.update()

    page.add(
        ft.FilledButton(
            "Refresh",
            on_click=refresh
        )
    )

    refresh(None)


if __name__ == "__main__":
    ft.app(main)