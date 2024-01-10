import io
import shutil
import subprocess
import traceback
from datetime import date
from os.path import exists
from time import sleep, time

import pytesseract as tess
from cv2 import (
    COLOR_BGR2HSV,
    COLOR_BGR2RGB,
    TM_CCOEFF_NORMED,
    cvtColor,
    inRange,
    matchTemplate,
    minMaxLoc,
)
from numpy import array, ndarray, where
from PIL import Image
from ppadb.client import Client as PPADBClient

from utils.functions import FileSingleton, current_time, get_dic_instances
from utils.resources import ImageSingleton
from utils.android_debug_bridge import Adb, DeviceNotFoundException

bridge = None


class AdbBluestacks(Adb):
    def __init__(self, number: str, host="127.0.0.1", port=5037):
        super().__init__(number, host, port)

    def update_port(self, instances=None):
        instances = get_dic_instances()
        super().update_port(instances)

    def connect_to_device(self, host="127.0.0.1"):
        super().connect_to_device(host)

    def wait_boot_complete(self, timeout=100, timedelta=1):
        """
        :param timeout: second
        :param timedelta: second
        """
        cmd = "getprop sys.boot_completed"

        end_time = time() + timeout

        while True:
            try:
                result = self.shell(cmd)
            except RuntimeError as e:
                self.print(str(e))
                sleep(0.5)
                continue
            except DeviceNotFoundException as e:
                self.print(str(e))
                sleep(0.5)
                continue

            if result.strip() == "1":
                return True

            if time() > end_time:
                raise TimeoutError()
            elif timedelta > 0:
                sleep(timedelta)

    def get_device(self, host="127.0.0.1", fail=0):
        self.port = str(self.data[str(self.number)]["port"])

        device = self.client.device(f"{host}:{self.port}")

        if device is None and fail == 0:
            self.start_server()

            self.connect_to_device()

            return self.get_device(fail=1)
        elif device is None and fail == 1:
            raise DeviceNotFoundException(f"{host}:{self.port}")
        return device

    def start_server(self):
        path = self.FileSingleton.get_path()
        cmd = f"{path['HD-Player'].replace('Player', 'Adb')} start-server"
        subprocess.run(cmd)

    def find_img_cv(self, img_to_find, confidence=0.9):
        pil_image = self.get_curr_device_screen_img()
        cv_image = array(pil_image)
        cv_image = cvtColor(cv_image, COLOR_BGR2RGB)
        result = matchTemplate(cv_image, img_to_find, TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = minMaxLoc(result)
        if max_val > confidence:
            return max_loc[0], max_loc[1]
        else:
            return

    def is_game_alive(self):
        # string = "dumpsys activity activities | grep mFocusedActivity"
        a = self.get_device().get_top_activity()
        if a:
            return "lilithgame" in str(a) or "rok" in str(a) or "lilithgames" in str(a)
        return False
