import hashlib
import json
import os
import subprocess
import sys
import threading
import traceback
from datetime import date, datetime
from time import sleep

import flet as ft
from pyautogui import getAllWindows

import Flet_main_interface
from keyauth import api

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
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    data["user"] = {'username': username, 'password': password}
    with open('user_settings.json', 'w') as config_file:
        config_file.write(json.dumps(data, indent=2))


def find_window(window_title):
    return any(window_title in element.title for element in getAllWindows())


class LoginButton(ft.FilledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.keyauthapp:api = None

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
        print("Login schedule...")
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            main(self.page)
            sys.exit()
            return False
        try:
            if self.keyauthapp.login(username, password,page=self.page):
                date_brut = datetime.utcfromtimestamp(int(self.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
                print(date_brut)
                heures = date_brut.split('-')
                future = date(int(heures[0]), int(heures[1]), int(heures[2]))
                diff = future - date.today()
                print(diff)
                self.page.title = f"Rok Bot - {diff.days} Days left"
                self.page.update()
                sleep(24 * 3600)
                return self.login_schedule(username, password)
            else:
                self.page.clean()
                main(self.page)
                for element in self.page.tile_manager.tiles.values():
                    element.started = False
                    element.stopped = False
                self.page.update()
        except Exception as e:
            # print(e)
            # traceback.print_exc()
            self.pop_banner("Problem occurred, please try again")
            print("Problem occurred while trying to connect")
            self.page.clean()
            main(self.page)
            for element in self.page.tile_manager.tiles.values():
                element.started = False
                element.stopped = False
            self.page.update()

    def login(self, e=None, username=None, password=None):
        print("Trying to login...")
        if username is None and password is None:
            username = self.page.controls[0].value
            password = self.page.controls[1].value
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            return False
        try:
            print(f"{username =} {password =}")
            if self.keyauthapp.login(username, password,page=self.page):
                date_brut = datetime.utcfromtimestamp(int(self.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
                heures = date_brut.split('-')
                future = date(int(heures[0]), int(heures[1]), int(heures[2]))
                diff = future - date.today()
                print(diff)
                print("Login successful")
                self.page.clean()
                self.page.window_width = 400
                self.page.window_height = 700
                Flet_main_interface.Main(self.page,diff.days)
                threading.Thread(self.login_schedule(username, password))
        except Exception as e:
            print(e)
            self.pop_banner("Problem occurred, please try again")
            print("Problem occurred while trying to connect")
            self.page.window_close()
            sys.exit(1)

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
    os.environ["FLET_APP_LIFETIME_MINUTES"] = "1"
    try:
        if not os.path.exists("user_settings.json"):
            with open('user_settings.json', 'w') as f:
                json.dump({}, f, indent=2)
                print("User settings created")
    except:
        pass
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    for i in range(5):
        ready = False
        try:
            keyauthapp = api(
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
    with open('path.json') as config_file:
        path = json.load(config_file)
    cmd = f"{path['HD-Player'].replace('Player', 'Adb')} start-server"
    subprocess.Popen(cmd)
    print("Bot is starting..")
    # if not find_window("RoK Bot -"):
    if "user" in data:
        if data["user"]["username"] != "":
            # Flet_main_interface.Main(page, 100)
            login_button.login(None, data['user']["username"], data['user']["password"])


if __name__ == "__main__":
    ft.app(target=main)
