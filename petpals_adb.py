import json
import shutil
from datetime import date
from os.path import exists
from time import sleep

from ppadb.client import Client as PPADBClient
import subprocess
import traceback
from numpy import array, where, ndarray
# noinspection PyProtectedMember
from cv2 import cvtColor, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, COLOR_BGR2HSV, inRange
import io
import pytesseract as tess
from PIL import Image


Image.LOAD_TRUNCATED_IMAGES = True
bridge = None

with open('config.json') as config_file:
    path = json.load(config_file)

adb_path = path['HD-Adb']

class Adb:
    def __init__(self, host='127.0.0.1', port=5037):
        self.client = PPADBClient(host, port)
        self.host = host
        self.port = port

    def connect_to_device(self, host='127.0.0.1'):
        cmd = f"{adb_path} connect {host}:{self.port}"
        subprocess.Popen(cmd)

    def get_client_devices(self):
        return self.client.devices()

    def get_device(self, host='127.0.0.1'):
        try:
            device = self.client.device(f'{host}:{self.port}')
            if device is None:
                self.print(f"INFO : Device is None, trying to reconnect..")

                cmd = f"{adb_path} connect {self.host}:{self.port}"
                subprocess.Popen(cmd)
                sleep(2)

                if device is None:
                    return self.get_device()
            return device
        except Exception as e:
            traceback.print_exc()
            self.print("EXCEPTION : Error in connect to device")

            cmd = f"{adb_path} start-server"
            subprocess.Popen(cmd)

            self.print(f"Adb restarting.. waiting 20s")
            sleep(20)
            self.print(f"Connecting to the device..")

            cmd = f"{adb_path} connect {self.host}:{self.port}"
            subprocess.Popen(cmd)

            sleep(5)
            return self.get_device()

    def print(self, text:str):
        print(text)

    def get_curr_device_screen_img_byte_array(self):
        try:
            return self.get_device().screencap()
        except:
            sleep(1)
            return self.get_device().screencap()


    def get_curr_device_screen_img(self):
        try:
            device = self.get_device()
            if device is None:
                print("get_curr_device_screen_img device is null")
                self.connect_to_device()
            output = io.BytesIO(device.screencap())
            # output.seek(0)
            image = Image.open(output)
            # self.print("INFO : Image opened")
            return image
        except Exception as e:
            self.print(f"EXCEPTION : get_screen_device")
            sleep(1)
            self.connect_to_device()
            return self.get_curr_device_screen_img()

    def get_cv2_img(self):
        try:
            screen = self.get_curr_device_screen_img()
            screen = array(screen)
            screen = cvtColor(screen, COLOR_BGR2RGB)
            return screen
        except:
            sleep(1)
            screen = self.get_curr_device_screen_img()
            screen = array(screen)
            screen = cvtColor(screen, COLOR_BGR2RGB)
            return screen

    def save_screen(self, file_name):
        image = Image.open(io.BytesIO(self.get_device().screencap()))
        image.save(f".//{file_name}.png")
        return True

    def click(self, x, y):
        string = f'input tap {x} {y}'
        self.shell(string)
        return

    def shell(self, string):
        device = self.get_device()
        try:
            return device.shell(string)
        except RuntimeError:
            print(RuntimeError)
            sleep(3)
            self.connect_to_device()
            return self.shell(string)

    def home_button(self):
        self.shell('input keyevent KEYCODE_HOME')
