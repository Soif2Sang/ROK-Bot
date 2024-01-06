import io
import shutil
import subprocess
import traceback
from datetime import date
from os.path import exists
from time import sleep

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
from utils.android_debug_bridge import Adb

bridge = None


class AdbBluestacks(Adb):
    def __init__(self, number: str, host="127.0.0.1", port=5037):
        super().__init__(number, host, port)

    def update_port(self):
        instances = get_dic_instances()

        if str(self.number) not in instances:
            return

        if self.port != int(instances[str(self.number)]["port"]):
            self.data = self.FileSingleton.get_data()
            self.data[str(self.number)]["instance"] = instances[str(self.number)]["instance"]
            self.data[str(self.number)]["name"] = instances[str(self.number)]["name"]
            self.data[str(self.number)]["port"] = int(instances[str(self.number)]["port"])
            self.port = int(instances[str(self.number)]["port"])
            self.FileSingleton.write_data(self.data)

    def connect_to_device(self, host="127.0.0.1"):
        path = self.FileSingleton.get_path()
        self.update_port()

        adb_path = f"{path['HD-Player'].replace('Player', 'Adb')}"
        cmd = f"{adb_path} connect {host}:{self.port}"
        subprocess.Popen(cmd)

    def get_device(self, host="127.0.0.1", fail=0):
        try:
            self.port = str(self.data[str(self.number)]["port"])
            device = self.client.device(f"{host}:{self.port}")
            if device is None:
                self.print(f"INFO : Device is None, trying to reconnect..")
                self.connect_to_device()
                sleep(2)

                if device is None and fail > 45:
                    return
                if device is None:
                    return self.get_device()

            return device
        except Exception as e:
            traceback.print_exc()
            self.print("EXCEPTION : Error in connect to device")

            self.update_port()
            path = self.FileSingleton.get_path()
            cmd = f"{path['HD-Player'].replace('Player', 'Adb')} start-server"
            subprocess.Popen(cmd)

            self.print(f"Adb restarting..")
            sleep(20)
            self.print(f"Connecting to the device..")

            self.connect_to_device()

            sleep(5)
            return self.get_device()

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

    #
    # def resource_amount_image_to_string(self):
    #     result_list = []
    #     boxes = [
    #         (695, 10, 770, 34), (820, 10, 890, 34), (943, 10, 1015, 34), (1065, 10, 1140, 34)]
    #     for box in boxes:
    #         x0, y0, x1, y1 = box
    #         imsch = imdecode(asarray(self.get_curr_device_screen_img_byte_array(), dtype=uint8),
    #                          IMREAD_COLOR)
    #         imsch = imsch[y0:y1, x0:x1]
    #         resource_image = Image.fromarray(imsch)
    #         try:
    #             result_list.append(abs(int(img_to_string(resource_image)
    #                                        .replace('.', '')
    #                                        .replace('B', '00000000')
    #                                        .replace('M', '00000')
    #                                        .replace('K', '00')
    #                                        ))
    #                                )
    #         except Exception as e:
    #             result_list.append(-1)
    #     return result_list

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

def img_to_string(pil_image):
    # pil_image.save(resource_path("test.png"))
    tess.pytesseract.tesseract_cmd = "tesseract\\tesseract.exe"
    result = tess.image_to_string(pil_image, lang="eng", config="--psm 6").replace("\t", "").replace("\n", "").replace("\f", "")
    return result


def img_remove_background_and_enhance_word(cv_image, lower, upper):
    hsv = cvtColor(cv_image, COLOR_BGR2HSV)
    return inRange(hsv, lower, upper)
