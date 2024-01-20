import json
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
    emulator = ""
    limit = 0


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

    def getEmulatorLimit(self) -> int:
        with self.FileLock:
            return self.limit

    def setEmulatorLimit(self, limit: int):
        with self.FileLock:
            self.limit = limit

    def startEmulator(self, emulator: str):
        path = FileSingleton().get_path()
        data = FileSingleton().get_data()
        emulator_choice = EmulatorSingleton().getEmulator()

        with self.FileLock:
            if emulator_choice == "ld":
                cmd = f'{path["LD-Console"]} launch --index {data.get(emulator).get("instance")}'
            else:
                cmd = f'{path["HD-Player"]} --instance {data.get(emulator).get("instance")}'

            subprocess.Popen(cmd)

            sleep(4)


class CaptchaSingleton:
    __instance = None
    FileLock = Lock()
    captchas = defaultdict(int)
    tier = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def setTier(self, tier: str) -> None:
        with self.FileLock:
            self.tier = tier

    def getTier(self) -> str:
        with self.FileLock:
            return self.tier

    def getCaptchas(self) -> dict:
        with self.FileLock:
            return self.captchas

    def setCaptchas(self, captchas: dict):
        with self.FileLock:
            self.captchas = captchas

    def addCaptcha(self):
        with self.FileLock:
            self.captchas[datetime.now().date().strftime("%Y-%m-%d")] += 1


class LinkSingleton:
    __instance = None
    FileLock = Lock()
    sellix = ""
    stripe = ""
    allLinks = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def getStripeLink(self) -> str:
        with self.FileLock:
            return self.stripe

    def setStripeLink(self, link: str):
        with self.FileLock:
            self.stripe = link

    def getSellixLink(self) -> str:
        with self.FileLock:
            return self.sellix

    def setSellixLink(self, link: str):
        with self.FileLock:
            self.sellix = link

    def setAllLinks(self, allLinks):
        with self.Filelock:
            self.allLinks = allLinks

    def getAllLinks(self):
        with self.FileLock:
            return self.allLinks

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
            print("data is none")
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
