import json
import logging
import os
from datetime import datetime
from functools import wraps
from threading import Lock
from time import perf_counter, sleep
from datetime import date
import win32gui
import win32process
from PIL import Image
from numpy import ndarray, array

if os.path.isdir("./resources"):
    dir = "./"
else:
    dir = "../"

PathLock = Lock()

DataLock = Lock()

LogsLock = Lock()

def write(name,text:str):
    try:
        with LogsLock:
            with open(f"{dir}logs/{name}_logs.txt", "a+", encoding="utf-8") as logger:
                logger.write(f"[ {date.today()} {current_time()} ] [ {name} ] {text}\n")
    except:
        return

def get_data():
    try:
        with DataLock:
            with open(f"{dir}user_settings.json", encoding='utf-8') as config_file:
                data = json.load(config_file)
    except:
        return get_data()
    return data

def get_path():
    with PathLock:
        with open(f"{dir}path.json", encoding='utf-8') as config_file:
            path = json.load(config_file)
    return path

def write_data(data):
    with DataLock:
        with open(f"{dir}user_settings.json",'w', encoding='utf-8') as config_file:
            config_file.write(json.dumps(data,indent=2))

def get_default_config():
    with DataLock:
        with open(f"{dir}default_profile.json", encoding='utf-8') as config_file:
            data = json.load(config_file)
    return data

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def string_to_co(string):
    string = string.replace("coordinates:", "")
    string = string.replace("x=", "")
    string = string.replace("y=", "")
    tmp = string.split(';')
    boolean = True
    for i in range(len(tmp)):
        tmp[i] = tmp[i].split(",")
        tmp[i][0] = int(tmp[i][0]) + 441
        tmp[i][1] = int(tmp[i][1]) + 101
    return tmp

def get_window_pid(title):
    hwnd = win32gui.FindWindow(None, title)
    thread_id, pid = win32process.GetWindowThreadProcessId(hwnd)
    return pid


def get_time(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start_time = perf_counter()
        func_output = func(self, *args, **kwargs)
        end_time = perf_counter()

        if func.__name__ == "check_captcha":
            print(f'[ {date.today()} {current_time()} ] [ {self.name} ] Verification made in {(end_time - start_time):0.1f}')
            self.set_text(f'[{current_time()}] Verification made in {(end_time - start_time):0.1f}')
            # with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
                # logger.write(f"[ {self.name} ] FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
                # logger.write(f"[ {date.today()} ] [ {current_time()} ] [{self.name}] Verification made in {(end_time - start_time):0.1f}\n")
            write(self.name,f"INFO : Verification made in {(end_time - start_time):0.1f}\n" )
        return func_output

    return wrapper


def clean_args(*args):
    list_args = []
    for args2 in args:
        if isinstance(args2, tuple) or isinstance(args2, list):
            for arg in args2:
                if isinstance(arg, Image.Image) or isinstance(arg, ndarray):
                    list_args.append("Image")
                else:
                    list_args.append(arg)
        else:
            list_args.append(args2)
    return tuple(list_args)


def get_name(func):
    @wraps(func)
    def wrapper(self: object, *args: object, **kwargs: object):
        # logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
        #                     datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.script_pause()
        # write(self.name, f"FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
        # with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
        #     logger.write(f"[ {date.today()} {current_time()} ] [ {self.name} ] FUNCTION : {func.__name__} ARGS : {clean_args(args)}\n")
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
        func_output = func(self, *args, **kwargs)
        return func_output

    return wrapper

def get_class(func):
    @wraps(func)
    def wrapper(self: object, *args: object, **kwargs: object):
        # logging.basicConfig(filename=f"{self.name}_logs.txt", level=logging.INFO, format="%(asctime)s %(message)s",
        #                     datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
        self.script_pause()
        # write(self.name, f"FUNCTION : {self.task_name()}\n")
        # with open(f"{self.name}_logs.txt", "a+", encoding="utf-8") as logger:
        #     logger.write(f"[ {date.today()} {current_time()} ] [ {self.name} ] FUNCTION : {self.task_name()}\n")
        # logging.info(f"[ {self.name} ] FUNCTION : {self.task_name()}")
        print(f"[ {date.today()} {current_time()} ] [ {self.name} ] FUNCTION : {self.task_name()}")
        func_output = func(self, *args, **kwargs)
        return func_output

    return wrapper

def filter_coordinate(couple: tuple[int, int]):
    if couple[0] < 206:
        return False
    if couple[0] < 274 and couple[1] < 108:
        return False
    if couple[0] > 516 and couple[1] < 168:
        return False
    if couple[0] < 735 and couple[1] > 587:
        return False
    if couple[0] > 1146 and couple[1] < 218:
        return False
    return True

def change_resource_type(place: str) -> str:
    if place == "First":
        return "Second"
    elif place == "Second":
        return "Third"
    elif place == "Third":
        return "Fourth"
    elif place == "Fourth":
        return "Done"

