import io
import shutil
import subprocess
import threading
import traceback
from datetime import datetime
from os.path import exists
from time import sleep, time

import pytesseract as tess
from cv2 import COLOR_BGR2HSV, COLOR_BGR2RGB,COLOR_BGR2GRAY, TM_CCOEFF_NORMED, cvtColor, inRange, matchTemplate, minMaxLoc
from numpy import array, ndarray, where
from PIL import Image
from ppadb.client import Client as PPADBClient

from utils.functions import colorize_name, colorize_output, current_time, get_name
from utils.resources import ImageSingleton
from utils.singletons import ss

bridge = None


class DeviceNotFoundException(Exception):
    def __init__(self, device_name):
        self.device_name = device_name
        message = f"Device not found: {device_name}"
        super().__init__(message)


class UnknownDeviceException(Exception):
    def __init__(self, device_number):
        self.device_number = device_number
        message = f"Unknown device with number: {device_number}"
        super().__init__(message)


class TimeSingleton:
    __instance = None
    FileLock = threading.Lock()
    restarted_time = 0

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def getRestartedTime(self) -> float:
        return self.restarted_time

    def setRestartedTime(self):
        self.restarted_time = time()


class Adb:
    adb_restart_lock = threading.Lock()
    last_restart_time = 0

    def __init__(self, instance: str, host="127.0.0.1", port=5037, task_reference=None):
        self.images = ImageSingleton()
        self.client = PPADBClient(host, port)
        self.host: str = host
        self.port: int = port
        self.instance: str = instance
        self.name: str = ss.emulator_settings.emulators[self.instance].name
        self.is_ld = False
        self.task_reference = task_reference

    def __str__(self):
        print(f"JsonNumber:{self.instance} port:{self.port}")
        return f"JsonNumber:{self.instance} port:{self.port}"

    def script_pause(self):
        if not self.task_reference:
            return
        return self.task_reference.script_pause()

    def update_port(self, instances=None):
        if instances is None:
            instances = {}

        if self.instance not in instances:
            raise UnknownDeviceException(f"{self.host}/{self.port}")

        if self.port != int(instances[self.instance]["port"]):
            ss.emulator_settings.emulators[self.instance].port = int(instances[self.instance]["port"])
            ss.emulator_settings.emulators[self.instance].name = instances[self.instance]["name"]
            ss.emulator_settings.emulators[self.instance].instance = instances[self.instance]["instance"]

            ss.write_emulator_settings(ss.emulator_settings)

    def stop_server(self):
        raise NotImplementedError("Method 'stop_server' is not implemented in the base class.")

    def start_server(self):
        raise NotImplementedError("Method 'start_server' is not implemented in the base class.")

    def get_device(self, host="127.0.0.1", fail=0):
        raise NotImplementedError("Method 'get_device' is not implemented in the base class.")

    @get_name
    def restart_adb_server(self):
        with TimeSingleton.FileLock:
            if TimeSingleton().getRestartedTime() + 20 > time():
                return
            self.stop_server()
            sleep(5)
            self.start_server()
            sleep(5)
            self.connect_to_device()

            TimeSingleton().setRestartedTime()

    def wait_boot_complete(self, timeout=100, timedelta=1):
        raise NotImplementedError("Method 'wait_boot_complete' is not implemented in the base class.")

    @get_name
    def connect_to_device(self, host="127.0.0.1"):
        self.update_port()

        if host == "127.0.0.1":
            adb_path = ss.application_settings.paths.adb
            cmd = f"{adb_path} connect {host}:{self.port}"
        else:
            adb_path = ss.application_settings.paths.adb
            cmd = f"{adb_path} connect {host}-{self.port}"

        subprocess.Popen(cmd)

    @get_name
    def get_client_devices(self):
        return self.client.devices()

    @get_name
    def print(self, *args: str):
        timestamp = f"[ \033[1;32m{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\033[0m ]"
        message = f"[ {colorize_name(self.name)} ] {colorize_output(' '.join(map(str, args)))}"

        print(f"{timestamp} {message}")

    @get_name
    def get_curr_device_screen_img_byte_array(self):
        try:
            return self.get_device().screencap()
        except Exception as e:
            print(e)
            sleep(1)
            return self.get_device().screencap()

    def get_curr_device_screen_img_bytesIO(self):
        try:
            return io.BytesIO(self.get_device().screencap())
        except Exception as e:
            print(e)
            self.print("EXCEPTION : get_curr_device_screen_img_bytesIO")
            self.print(e)
            sleep(1)
            return io.BytesIO(self.get_device().screencap())

    @get_name
    def get_curr_device_screen_img(self, deadstop=0):
        try:
            device = self.get_device()
            output = io.BytesIO(device.screencap())
            return Image.open(output)
        except Exception as e:
            self.print(f"EXCEPTION : get_curr_device_screen_img")
            if deadstop == 30:
                raise e
            sleep(1)
            return self.get_curr_device_screen_img(deadstop + 1)

    @get_name
    def get_cv2_img(self):
        screen = self.get_curr_device_screen_img()
        screen = array(screen)
        screen = cvtColor(screen, COLOR_BGR2RGB)
        return screen

    @get_name
    def save_screen(self, file_name):
        image = Image.open(io.BytesIO(self.get_device().screencap()))
        image.save(f".//{file_name}.png")
        return True

    @get_name
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

    @get_name
    def find_img(self, target: str, source: ndarray = None, confidence=0.9):
        try:
            if source is None:
                source = self.get_cv2_img()
            height, width, _ = source.shape

            if height == 720 and width == 1280:
                if target == "new_troops_button":
                    source = source[0:322, 800:1280]
                if target == "gem_search_button":
                    source = source[470:600, 0:150]
                if target == "button_level":
                    source = source[720 // 2 - 50 :, :]
                if target in ["minus_button", "plus_button"]:
                    source = source[720 // 2 :, :]
                if target == "search_button":
                    source = source[720 // 2 :, : 1280 // 4]

            img_to_find = self.images.get_file_name(target)
            # bot.adb.get_cv2_img()
            result = matchTemplate(source, img_to_find, TM_CCOEFF_NORMED)
            min_val, max_val, min_loc, max_loc = minMaxLoc(result)
            if max_val > confidence:
                if target == "new_troops_button":
                    return max_loc[0] + 800, max_loc[1]
                if target == "button_level":
                    return max_loc[0], max_loc[1] + 720 // 2 - 50
                if target in ["minus_button", "plus_button"]:
                    return max_loc[0], max_loc[1] + 720 // 2
                if target == "search_button":
                    return max_loc[0], max_loc[1] + 720 // 2
                return max_loc[0], max_loc[1]
            else:
                return
        except Exception as exception_error:
            self.print("Error occured when using find_image")
            self.print(target)
            traceback.print_exc()
            self.print(exception_error)

    @get_name
    def find_img_src_conf(self, src, target, confidence):
        img_to_find = self.images.get_file_name(target)
        result = matchTemplate(src, img_to_find, TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = minMaxLoc(result)
        if max_val > confidence:
            return max_loc[0], max_loc[1]
        else:
            return

    @get_name
    def find_multiple_img(self, target, source=None, confidence=0.9):
        if source is None:
            pil_image = self.get_curr_device_screen_img()
            cv_image = array(pil_image)
            source = cvtColor(cv_image, COLOR_BGR2RGB)
        cv_image = source


        img_to_find = self.images.get_file_name(target)
        if target == "back_icon":
            cv_image = cv_image[0:720, 1000:1280]
        # print(img_to_find)

        if target == 'close_window3':
            cv_image = cvtColor(cv_image, COLOR_BGR2GRAY)
            img_to_find = cvtColor(img_to_find, COLOR_BGR2GRAY)

        result = matchTemplate(cv_image, img_to_find, TM_CCOEFF_NORMED)
        needle_w = img_to_find.shape[1]
        needle_h = img_to_find.shape[0]

        min_val, max_val, min_loc, max_loc = minMaxLoc(result)
        min_thresh = confidence
        # print(min_thresh>confidence)
        location = where(result >= min_thresh)
        location = list(zip(*location[::-1]))
        # print(location)

        rectangles = []
        for loc in location:
            rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
            rectangles.append(rect)
        # print(rectangles)

        localisations = []

        for i in range(len(rectangles)):
            if target == "back_icon":
                # print(file_name)
                # print(rectangles[i][0])
                # print(rectangles[i][0]+1000)
                localisations.append((rectangles[i][0] + 1000, rectangles[i][1]))
            else:
                localisations.append((rectangles[i][0], rectangles[i][1]))
        element_to_delete = []
        for i in range(len(localisations) - 1):
            if (
                (localisations[i][0] + 1 == localisations[i + 1][0])
                or (localisations[i][0] - 1 == localisations[i + 1][0])
                or (localisations[i][0] == localisations[i + 1][0])
            ) and (
                (localisations[i][1] + 1 == localisations[i + 1][1])
                or (localisations[i][1] - 1 == localisations[i + 1][1])
                or (localisations[i][1] == localisations[i + 1][1])
            ):
                element_to_delete.append(localisations[i])

        # print(element_to_delete)
        for element in element_to_delete:
            localisations.remove(element)
        return localisations

    @get_name
    def is_game_alive(self):
        # string = "dumpsys activity activities | grep mFocusedActivity"
        a = self.get_device().get_top_activity()
        if a:
            return "lilithgame" in str(a) or "rok" in str(a) or "lilithgames" in str(a)
        return False

    def click(self, x, y):
        string = f"input tap {x} {y}"
        self.shell(string)
        return

    @get_name
    def shell(self, string, max_attempts=5, timeout=2):
        for attempt in range(max_attempts):
            try:
                device = self.get_device()
                return device.shell(string)
            except (RuntimeError, DeviceNotFoundException, Exception) as e:
                self.print(f"Cannot use shell: {e}")
                self.restart_adb_server()

        raise DeviceNotFoundException("Unable to execute shell command after multiple attempts")

    # def shell(self, command, fail = 0, timeout=120):
    #     end_time = time() + timeout

    #     while True:
    #         try:
    #             result = self.shell(command)
    #         except RuntimeError as e:
    #             self.print(str(e))
    #             sleep(0.5)
    #             continue
    #         except DeviceNotFoundException as e:
    #             self.print(str(e))
    #             sleep(0.5)
    #             continue

    #         if time() > end_time:
    #             raise TimeoutError()
    #         elif timedelta > 0:
    #             sleep(timedelta)

    def swipe(self, x, y, x2, y2):
        string = f"input swipe {x} {y} {x2} {y2} 420"
        self.shell(string)
        return

    def swipe_arg(self, x, y, x2, y2, arg):
        string = f"input swipe {x} {y} {x2} {y2} {arg}"
        self.shell(string)
        return

    #
    def resource_amount_image_to_string(self):
        result_list = []
        boxes = [(695, 10, 770, 34), (820, 10, 890, 34), (943, 10, 1015, 34), (1065, 10, 1140, 34)]
        for box in boxes:
            x0, y0, x1, y1 = box
            imsch = self.get_cv2_img()
            imsch = imsch[y0:y1, x0:x1]
            resource_image = Image.fromarray(imsch)
            try:
                result_list.append(
                    abs(
                        int(
                            img_to_string(resource_image).replace(".", "").replace("B", "00000000").replace("M", "00000").replace("K", "00")
                        )
                    )
                )
            except Exception as e:
                result_list.append(-1)
        return result_list

    def restart_emulator(self):
        try:
            path = self.FileSingleton.get_path()
            string = path["bluestacks"][:-5] + ".txt"
            if exists(rf'{path["bluestacks"]}'):
                string = path["bluestacks"][:-5] + ".txt"
                shutil.copy(rf'{path["bluestacks"]}', rf"{string}")

            with open(rf"{string}", "r") as file:
                data_instance = file.read().split("\n")
        except:
            print("The pass you provided is wrong ! We are looking for something like : \n C:\ProgramData\BlueStacks_nxt\bluestacks.conf")

        liste_info = []
        for element in data_instance:
            if ((("bst.instance.Nougat64" in element) and ("adb_port" in element)) and "status" not in element) or (
                ("bst.instance.Nougat64" in element) and ("display_name" in element)
            ):
                liste_info.append(element)

        dico_instance = {}
        for i in range(0, len(liste_info), 2):
            string = liste_info[i].split(".adb_port=")
            string[1] = string[1].replace('"', "")
            string[0] = string[0][13:]
            dico_instance[str(len(dico_instance))] = {}
            dico_instance[str(len(dico_instance) - 1)]["instance"] = str(string[0])
            dico_instance[str(len(dico_instance) - 1)]["port"] = string[1]
            string2 = liste_info[i + 1].split(".display_name=")
            string2[1] = string2[1].replace('"', "")
            dico_instance[str(len(dico_instance) - 1)]["name"] = string2[1]

    def home_button(self):
        self.shell("input keyevent KEYCODE_HOME")

    #
    # def enable_adb(self,host='127.0.0.1', port=5037):
    #     adb = None
    #     try:
    #         adb = Adb(host=host, port=port)
    #
    #         version = adb.client.version()
    #
    #         if version != 41:
    #             raise RuntimeError('Error: require adb version 41, but version is {}'.format(version))
    #
    #     except RuntimeError as err:
    #         with open('path.json') as config_file:
    #             path = json.load(config_file)
    #         adb_path = f"{path['HD-Player'].replace('Player', 'Adb')}"
    #         # adb_path = r"C:\Program Files\BlueStacks_nxt\HD-Adb.exe"
    #
    #         ret = subprocess.run(f"{adb_path} -P {port} kill-server {host}", shell=True,
    #                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    #
    #         ret = subprocess.run(f"{adb_path} -P {port} connect {host}", shell=True,
    #                              stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    #
    #         if ret.returncode != 0:
    #             raise RuntimeError('Error: fail to start adb server. \n({})'.format(ret))
    #
    #     return adb


def img_to_string(pil_image):
    # pil_image.save(resource_path("test.png"))
    tess.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"
    result = tess.image_to_string(pil_image, lang="eng", config="--psm 6").replace("\t", "").replace("\n", "").replace("\f", "")
    return result


def img_remove_background_and_enhance_word(cv_image, lower, upper):
    hsv = cvtColor(cv_image, COLOR_BGR2HSV)
    return inRange(hsv, lower, upper)
