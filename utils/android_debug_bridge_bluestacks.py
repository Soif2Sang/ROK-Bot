import subprocess
from time import time

import pytesseract as tess
from cv2 import COLOR_BGR2HSV, COLOR_BGR2RGB, TM_CCOEFF_NORMED, cvtColor, inRange, matchTemplate, minMaxLoc
from numpy import array, ndarray, where
from PIL import Image
from ppadb.client import Client as PPADBClient

from utils.android_debug_bridge import Adb, DeviceNotFoundException
from utils.functions import accurate_sleep, current_time, get_dic_instances, get_name
from utils.resources import ImageSingleton
from utils.singletons import ss

bridge = None


class AdbBluestacks(Adb):
    def __init__(self, instance: str, host="127.0.0.1", port=5037, task_reference=None):
        super().__init__(instance, host, port, task_reference)

    def update_port(self, instances=None):
        instances = get_dic_instances()
        super().update_port(instances)

    def connect_to_device(self, host="127.0.0.1"):
        super().connect_to_device(host)

    @get_name
    def wait_boot_complete(self, timeout=100, timedelta=1):
        """
        :param timeout: second
        :param timedelta: second
        """
        cmd = "getprop sys.boot_completed"

        end_time = time() + timeout

        while True:
            if time() > end_time:
                raise TimeoutError()
            try:
                result = self.shell(cmd)
            except RuntimeError as e:
                self.print("RuntimeError", str(e))
                accurate_sleep(3)
                continue
            except DeviceNotFoundException as e:
                self.print("DeviceNotFoundException", str(e))
                accurate_sleep(3)
                continue

            if result.strip() == "1":
                return True

            elif timedelta > 0:
                accurate_sleep(timedelta)

    @get_name
    def get_device(self, host="127.0.0.1", max_attempts=10, timeout=2):
        self.port = str(ss.emulator_settings.emulators[str(self.instance)].port)

        for attempt in range(max_attempts):
            device = self.client.device(f"{host}:{self.port}")

            if device is not None:
                return device

            self.print(f"Device Not Found")
            self.update_port()
            self.connect_to_device()

            cmd = f"{ss.application_settings.paths.bluestacks.player.replace('Player', 'Adb')} -s {host}:{self.port} shell eco i"
            subprocess.run(cmd)
            accurate_sleep(timeout)

        raise DeviceNotFoundException(f"{host}:{self.port}")

    @get_name
    def stop_server(self):
        cmd = f"{ss.application_settings.paths.bluestacks.player.replace('Player', 'Adb')} kill-server"
        subprocess.run(cmd)

    @get_name
    def start_server(self):
        cmd = f"{ss.application_settings.paths.bluestacks.player.replace('Player', 'Adb')} start-server"
        subprocess.run(cmd)

    def is_game_alive(self):
        # string = "dumpsys activity activities | grep mFocusedActivity"
        a = self.get_device().get_top_activity()
        if a:
            return "lilithgame" in str(a) or "rok" in str(a) or "lilithgames" in str(a)
        return False
