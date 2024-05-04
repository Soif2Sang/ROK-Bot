import json
import os
import subprocess
import threading
from collections import defaultdict
from datetime import date, datetime
from threading import Lock
from time import sleep
from typing import Literal

from utils.schemas.application_schemas import ApplicationSettingsSchema
from utils.schemas.emulator_schemas import EmulatorListSchema
from utils.schemas.worker_schemas import WorkerTypeSchema


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

    def getEmulatorType(self) -> Literal["ld", "bluestacks"]:
        with self.FileLock:
            return self.emulator

    def setEmulator(self, mode: Literal["ld", "bluestacks"]):
        with self.FileLock:
            self.emulator = mode

    def startEmulator(self, emulator: str):
        path = FileSingleton().get_path()
        data = FileSingleton().get_data()
        emulator_choice = EmulatorSingleton().getEmulatorType()

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
        try:
            if not os.path.exists("./user_settings.json"):
                with open("./user_settings.json", "w", encoding="utf-8") as config_file:
                    json.dump({}, config_file)  # Creates the file with an empty JSON object if it doesn't exist
            with open("./user_settings.json", "r", encoding="utf-8") as config_file:
                data = json.load(config_file)
        finally:
            self.FileLock.release()
        return data

    def getCachedData(self):
        if self.data is None:
            self.data = self.get_data()
        return self.data

    def get_path(self):
        self.FileLock.acquire()
        try:
            if not os.path.exists("./path.json"):
                with open("./path.json", "w", encoding="utf-8") as config_file:
                    json.dump({}, config_file)  # Creates the file with an empty JSON object if it doesn't exist
            with open("./path.json", "r", encoding="utf-8") as config_file:
                path = json.load(config_file)
        finally:
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


class SettingsSingleton:
    _instance = None
    _lock = threading.Lock()
    emulator_settings: EmulatorListSchema = None
    worker_settings: WorkerTypeSchema = None
    application_settings: ApplicationSettingsSchema = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.open_application_settings()
            cls._instance.open_worker_settings()
            cls._instance.open_emulator_settings()
        return cls._instance

    def open_application_settings(self) -> ApplicationSettingsSchema:
        with self._lock:
            if not os.path.exists("application_settings.json"):
                with open("application_settings.json", "w") as f:
                    data = ApplicationSettingsSchema().to_dict()
                    json.dump(data, f, indent=4)
            else:
                with open("application_settings.json", "r") as f:
                    data = ApplicationSettingsSchema.from_dict(json.loads(f.read()))
            self.application_settings = data
            return data

    def open_worker_settings(self) -> WorkerTypeSchema:
        with self._lock:
            if not os.path.exists("worker_settings.json"):
                with open("worker_settings.json", "w") as f:
                    data = WorkerTypeSchema().to_dict()
                    json.dump(data, f, indent=4)
            else:
                with open("worker_settings.json", "r") as f:
                    data = WorkerTypeSchema.from_dict(json.loads(f.read()))
            self.worker_settings = data
            return data

    def open_emulator_settings(self) -> EmulatorListSchema:
        with self._lock:
            if not os.path.exists("emulator_settings.json"):
                with open("emulator_settings.json", "w") as f:
                    data = EmulatorListSchema().to_dict()
                    json.dump(data, f, indent=4)
            else:
                with open("emulator_settings.json", "r") as f:
                    data = EmulatorListSchema.from_dict(json.loads(f.read()))
            self.emulator_settings = data
            return data

    def write_application_settings(self, data: ApplicationSettingsSchema):
        with self._lock:
            with open("application_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.application_settings = data

    def write_worker_settings(self, data: WorkerTypeSchema):
        with self._lock:
            with open("worker_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.worker_settings = data

    def write_emulator_settings(self, data: EmulatorListSchema):
        with self._lock:
            with open("emulator_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.emulator_settings = data


class SettingsSingleton:
    _instance = None
    _lock = threading.Lock()
    emulator_settings: EmulatorListSchema = None
    worker_settings: WorkerTypeSchema = None
    application_settings: ApplicationSettingsSchema = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.open_application_settings()
            cls._instance.open_worker_settings()
            cls._instance.open_emulator_settings()
        return cls._instance

    def open_application_settings(self) -> ApplicationSettingsSchema:
        with self._lock:
            if not os.path.exists("application_settings.json"):
                with open("application_settings.json", "w") as f:
                    data = ApplicationSettingsSchema().to_dict()
                    json.dump(data, f, indent=4)
            with open("application_settings.json", "r") as f:
                data = ApplicationSettingsSchema.from_dict(json.loads(f.read()))
            self.application_settings = data
            return data

    def open_worker_settings(self) -> WorkerTypeSchema:
        with self._lock:
            if not os.path.exists("worker_settings.json"):
                with open("worker_settings.json", "w") as f:
                    data = WorkerTypeSchema().to_dict()
                    json.dump(data, f, indent=4)
            with open("worker_settings.json", "r") as f:
                data = WorkerTypeSchema.from_dict(json.loads(f.read()))
            self.worker_settings = data
            return data

    def open_emulator_settings(self) -> EmulatorListSchema:
        with self._lock:
            if not os.path.exists("emulator_settings.json"):
                with open("emulator_settings.json", "w") as f:
                    data = EmulatorListSchema().to_dict()
                    json.dump(data, f, indent=4)
            with open("emulator_settings.json", "r") as f:
                data = EmulatorListSchema.from_dict(json.loads(f.read()))
            self.emulator_settings = data
            return data

    def write_application_settings(self, data: ApplicationSettingsSchema):
        with self._lock:
            with open("application_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.application_settings = data

    def write_worker_settings(self, data: WorkerTypeSchema):
        with self._lock:
            with open("worker_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.worker_settings = data

    def write_emulator_settings(self, data: EmulatorListSchema):
        with self._lock:
            with open("emulator_settings.json", "w") as f:
                json.dump(data.to_dict(), f, indent=4)
            self.emulator_settings = data


def current_time():
    return datetime.now().strftime("%H:%M:%S")


ss = SettingsSingleton()
