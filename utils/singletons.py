import json
import os
import subprocess
from collections import defaultdict
from datetime import date, datetime
from threading import Lock
from time import sleep
from typing import Literal


class ApiSingleton:
    __instance = None
    FileLock = Lock()
    apikey = ""
    tier = ""

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def getApiKey(self) -> str:
        with self.FileLock:
            return self.apikey

    def setApiKey(self, key: str):
        with self.FileLock:
            self.apikey = key

    def getTier(self) -> str:
        with self.FileLock:
            return self.tier

    def setTier(self, tier: str):
        with self.FileLock:
            self.tier = tier


class EmulatorSingleton:
    __instance = None
    FileLock = Lock()
    EmulatorLock = Lock()
    emulator = ""

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def getEmulator(self) -> Literal["ld", "bluestacks"]:
        with self.FileLock:
            return self.emulator

    def setEmulator(self, mode: Literal["ld", "bluestacks"]):
        with self.FileLock:
            self.emulator = mode

    def startEmulator(self, emulator: str):
        path = FileSingleton().get_path()
        data = FileSingleton().get_data()
        emulator_choice = EmulatorSingleton().getEmulator()

        with self.EmulatorLock:
            if emulator_choice == "ld":
                cmd = f'{path["LD-Console"]} launch --index {data.get(emulator).get("instance")}'
            else:
                cmd = f'{path["HD-Player"]} --instance {data.get(emulator).get("instance")}'

            subprocess.Popen(cmd)

            sleep(5)

class FileSingleton:
    __instance = None
    FileLock = Lock()
    data = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def write(self, name, text: str):
        self.FileLock.acquire()
        if not os.path.exists("./logs"):
            os.mkdir("./logs")
        with open(f"./logs/{name}_logs.txt", "a+", encoding="utf-8") as logger:
            logger.write(f"[ {date.today()} {current_time()} ] [ {name} ] {text}\n")
        self.FileLock.release()

    def get_data(self):
        self.FileLock.acquire()
        with open(f"./user_settings.json", encoding="utf-8") as config_file:
            data = json.load(config_file)
        self.FileLock.release()
        return data

    def getCachedData(self):
        if self.data is None:
            self.data = self.get_data()
        return self.data

    def get_path(self):
        self.FileLock.acquire()
        with open(f"./path.json", encoding="utf-8") as config_file:
            path = json.load(config_file)
        self.FileLock.release()
        return path

    def write_data(self, data):
        self.FileLock.acquire()
        with open(f"./user_settings.json", "w", encoding="utf-8") as config_file:
            config_file.write(json.dumps(data, indent=2))
        self.data = data
        self.FileLock.release()

    def get_default_config(self):
        self.FileLock.acquire()
        with open(f"./default_profile.json", encoding="utf-8") as config_file:
            data = json.load(config_file)
        self.FileLock.release()
        return data


def current_time():
    return datetime.now().strftime("%H:%M:%S")
