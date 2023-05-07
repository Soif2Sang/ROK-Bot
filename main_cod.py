import hashlib
import json
import os
import subprocess
import sys
import threading
from datetime import date, datetime
from time import sleep

import flet as ft
from pyautogui import getAllWindows

import views.Flet_main_interface
from views import Flet_main_interface
from views.Flet_Path import find_file_in_all_drives
from utils.Task_utils import get_data, get_path, write_data
from utils.auth import selfApi


def getchecksum():
    md5_hash = hashlib.md5()
    try:
        file = open(''.join(sys.argv), "rb")
    except:
        file = open(''.join(sys.argv[0]), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

def update_user_info(password, username):
    data = get_data()
    data["user"] = {'username': username, 'password': password}
    write_data(data)

def find_window(window_title):
    return any(window_title in element.title for element in getAllWindows())


class LoginButton(ft.FilledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyauthapp:selfApi | None= None

    def is_str_valid(self, username, password):
        for element in ['#', "$", "&", "|", "\0",
                        "\n",
                        "\r",
                        '\'',
                        "'",
                        '"',
                        "\Z"]:
            if element in username or element in password:
                return False
        return True

    def login_schedule(self, username, password):
        self.keyauthapp = selfApi(
            name="Rokbd",
            ownerid="7oofxdj8uH",
            secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
            version="1.0",
            hash_to_check=getchecksum()
        )
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            main(self.page)
            try:
                os._exit(1)
            except:
                sys.exit(1)
        try:
            if self.keyauthapp.login(user=username, password=password,page=self.page):
                date_brut = datetime.utcfromtimestamp(int(self.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
                heures = date_brut.split('-')
                future = date(int(heures[0]), int(heures[1]), int(heures[2]))
                diff = future - date.today()
                self.page.title = f"Cod Bot - {diff.days} Days left"
                self.page.update()
                sleep(24 * 3600)
                return self.login_schedule(username, password)
            else:
                self.page.clean()
                main(self.page)
                for element in self.page.tile_manager.tiles.values():
                    element.started = False
                    element.stopped = True
                self.page.update()
        except:
            try:
                os._exit(1)
            except:
                sys.exit(1)

        #     traceback.print_exc()
        #     self.pop_banner("Problem occurred, please try again")
        #     print("Problem occurred during the connection")
        #     self.page.clean()
        #     main(self.page)
        #     for element in self.page.tile_manager.tiles.values():
        #         element.started = False
        #         element.stopped = False
        #     self.page.update()

    def login(self, e=None, username=None, password=None):
        self.keyauthapp = selfApi(
            name="Rokbd",
            ownerid="7oofxdj8uH",
            secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
            version="1.0",
            hash_to_check=getchecksum()
        )
        print("Trying to login...")
        if username is None and password is None:
            username = self.page.controls[0].value
            password = self.page.controls[1].value
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            return False
        # try:
        if self.keyauthapp.login(username, password,page=self.page):
            print("Login successful")
            data = get_data()
            if 'user' not in data:
                data['user'] = {'username':username,'password':password}
                write_data(data)
            date_brut = datetime.utcfromtimestamp(int(self.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
            heures = date_brut.split('-')
            future = date(int(heures[0]), int(heures[1]), int(heures[2]))
            diff = future - date.today()
            self.page.clean()
            self.page.window_width = 400
            self.page.window_height = 700
            Flet_main_interface.Main_cod(self.page, diff.days)
            threading.Thread(self.login_schedule(username, password))
        # except Exception as e:
        #     print(e)
        #     self.pop_banner("Problem occurred, please try again")
        #     print("Problem occurred during the connection")
        #     self.page.window_close()
        #     sys.exit(1)

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def pop_banner(self, text):
        self.page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=self.close_banner),
            ],
            open=True
        )
        self.page.update()

def main(page: ft.Page):
    try:
        if not os.path.exists("./user_settings.json"):
            write_data({})
            print("User settings created")
    except:
        pass
    path = get_path()
    if not os.path.exists(path['bluestacks']) or not os.path.exists(path['HD-Player']):
        if result:=find_file_in_all_drives('bluestacks\.conf'):
            path['bluestacks\.conf'.split("\\")[0]] = result
            with open('../path.json', 'w', encoding="UTF-8") as f:
                json.dump(path, f, indent=2)
        if result := find_file_in_all_drives('HD-Player\.exe'):
            path['HD-Player\.exe'.split("\\")[0]] = result
            with open('../path.json', 'w', encoding="UTF-8") as f:
                json.dump(path, f, indent=2)

    data = get_data()
    if "discord" not in data:
        data["discord"] = {"user_id":0, "enabled":False}
        write_data(data)
    for i in range(5):
        ready = False
        try:
            keyauthapp = selfApi(
                name="Rokbd",
                ownerid="7oofxdj8uH",
                secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
                version="1.0",
                hash_to_check=getchecksum()
            )
            ready = True
        except :
            keyauthapp = None
            print("Problem in the database loading..Wait a bit please..")
            sleep(5)
        if ready:break

    page.window_width = 330
    page.window_height = 330
    page.add(ft.TextField(label="Username", width=300, value=data.get("user",{}).get("username","")))
    page.add(ft.TextField(label="Password", password=True, can_reveal_password=True, width=300,value=data.get("user",{}).get("password","")))
    login_button = LoginButton(text="Login", width=100)
    login_button.on_click = login_button.login
    login_button.keyauthapp = keyauthapp
    page.close_banner = login_button.close_banner
    page.add(login_button)
    page.update()
    path = get_path()
    cmd = f"{path['HD-Player'].replace('Player', 'Adb')} start-server"
    subprocess.Popen(cmd)
    print("Bot is starting..")
    # if not find_window("RoK Bot -"):
    if "user" in data:
        if data["user"]["username"] != "":
            # Flet_main_interface.Main(page, 100)
            login_button.login(None, data['user']["username"], data['user']["password"])

from pathlib import Path
from threading import Thread

from pyprotector import PythonProtector

# -- Define Constants
LOGGING_PATH = (
    Path.home() / "AppData/Roaming/PythonProtector/logs/[Security].log"
)  # -- This can be any path

# -- Construct Class
security = PythonProtector(
    debug=True,
    modules=[
        "AntiProcess",
        "AntiVM",
        "Miscellaneous",
        "AntiDLL",
        "AntiAnalysis",
        "AntiDump"],
    logs_path=LOGGING_PATH,
    webhook_url="",
    on_detect=[
        "Report",
        "Exit",
        "Screenshot"],
)

# -- Main Code


if __name__ == "__main__":
    SecurityThread = Thread(
        name="Python Protector", target=security.start
    )  # -- Start Before Any Other Code Is Run
    # SecurityThread.start()
    ft.app(target=main)
