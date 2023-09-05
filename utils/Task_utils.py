import hashlib
import json
import logging
import os
import shutil
import sys
from datetime import datetime
from functools import wraps
from os.path import exists
from threading import Lock
from time import perf_counter, sleep
from datetime import date

import pyautogui
import win32gui
import win32process
from PIL import Image
from numpy import ndarray, array
import re
dir = "./"

def custom_key(item):
    parts = item['instance'].split('_')
    if len(parts) == 1:
        return -1
    return int(parts[1])

class FileSingleton:
    __instance = None
    FileLock = Lock()
    def __new__(cls):
       if cls.__instance is None:
           cls.__instance = super().__new__(cls)
       return cls.__instance

    def write(self,name,text:str):
        self.FileLock.acquire()
        with open(f"{dir}logs/{name}_logs.txt", "a+", encoding="utf-8") as logger:
            logger.write(f"[ {date.today()} {current_time()} ] [ {name} ] {text}\n")
        self.FileLock.release()

    def get_data(self):
        self.FileLock.acquire()
        with open(f"{dir}user_settings.json", encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.FileLock.release()
        return data

    def get_path(self):
        self.FileLock.acquire()
        with open(f"{dir}path.json", encoding='utf-8') as config_file:
            path = json.load(config_file)
        self.FileLock.release()
        return  path

    def write_data(self,data):
        self.FileLock.acquire()
        with open(f"{dir}user_settings.json",'w', encoding='utf-8') as config_file:
            config_file.write(json.dumps(data,indent=2))
        self.FileLock.release()

    def get_default_config(self):
        self.FileLock.acquire()
        with open(f"{dir}default_profile.json", encoding='utf-8') as config_file:
            data = json.load(config_file)
        self.FileLock.release()
        return data

def current_time():
    return datetime.now().strftime("%H:%M:%S")

def string_to_co(string):
    pattern_x = r'x=(\d+)'
    pattern_y = r'y=(\d+)'

    matches_x = re.findall(pattern_x, string)
    matches_y = re.findall(pattern_y, string)

    return [(int(pair[0]) + 441, int(pair[1]) + 101) for pair in list(zip(matches_x, matches_y))]

def string_to_co_slide(string):
    pattern_x = r'x=(\d+)'
    pattern_y = r'y=(\d+)'

    matches_x = re.search(pattern_x, string)
    matches_y = re.search(pattern_y, string)
    # print(matches_y.group())
    return (int(matches_x.group(1)), int(matches_y.group(1)))

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
            self.FileSingleton.write(self.name,f"INFO : Verification made in {(end_time - start_time):0.1f}\n" )
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
        # self.logger.info(f"FUNCTION : {func.__name__} ARGS : {clean_args(args)}")
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
        # print(f"[ {date.today()} {current_time()} ] [ {self.name} ] FUNCTION : {self.task_name()}")
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

def getchecksum():
    md5_hash = hashlib.md5()
    try:
        file = open(''.join(sys.argv), "rb")
    except:
        file = open(''.join(sys.argv[0]), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

def get_dic_instances():
    try:
        fileSingleton = FileSingleton()
        path = fileSingleton.get_path()
        string = path["bluestacks"][:-5] + ".txt"
        if exists(rf'{path["bluestacks"]}'):
            string = path["bluestacks"][:-5] + ".txt"
            shutil.copy(rf'{path["bluestacks"]}', rf'{string}')
        with open(rf'{string}', 'r', encoding='utf-8') as file:
            data_instance = file.read().split('\n')
    except:
        raise OSError(
            "The path you provided is wrong ! We are looking for something like : \n r'C:\ProgramData\BlueStacks_nxt\\bluestacks.conf'")

    pattern_status_adb = re.compile(r'bst\.instance\.Nougat64_?(\d*)\.status\.adb_port')
    pattern_display_name = re.compile(r'bst\.instance\.Nougat64_?(\d*)\.display_name')

    pattern_for_nougat = re.compile(r'Nougat64_?(\d*)')
    pattern_for_value = re.compile(r'="([^"]*)"')

    matched_lines = []

    for line in data_instance:
        line = line.strip()
        # Check for display_name pattern and nougat version
        if pattern_display_name.search(line):
            matched_lines.append(pattern_for_nougat.search(line).group())
            matched_lines.append(pattern_for_value.search(line).group(1))
        # Check for status and adb_port pattern
        elif pattern_status_adb.search(line):
            matched_lines.append(pattern_for_value.search(line).group(1))

    bluestacks_instances = []
    for i in range(0, len(matched_lines), 3):
        bluestacks_instances.append(
            {
                'instance': str(matched_lines[i]),
                'name': matched_lines[i + 1],
                'port': int(matched_lines[i + 2]),
            }
        )

    bluestacks_instances.sort(key=custom_key)
    transformed_dict = dict(map(lambda idx_item: (str(idx_item[0]), idx_item[1]), enumerate(bluestacks_instances)))
    return transformed_dict

def get_index_and_names(data):
    names = []
    for index, value in enumerate(data.values()):
        names.append((index, value['name']))
    return names

def get_current_instances(data):
    names = get_index_and_names(data)
    instances_available = []
    for win in pyautogui.getAllWindows():
        for name in names:
            if win.title == name[1]:
                instances_available.append(name)
    instances_available.sort(key=lambda x: x[0])
    return instances_available

def get_all_vms_running():
    return get_current_instances(get_dic_instances())

def string_to_co_slide(string):
    pattern_x = r'x=(\d+)'
    pattern_y = r'y=(\d+)'

    matches_x = re.search(pattern_x, string)
    matches_y = re.search(pattern_y, string)
    # print(matches_y.group())
    return (int(matches_x.group(1)), int(matches_y.group(1)))