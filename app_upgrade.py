# coding=UTF-8
import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, date
import threading
from time import sleep
from flet_route import path, Routing
import flet as ft

from views.city_layout import viewCityLayout
from views.profile_settings import viewProfileSettings
from views._main import Main
from views.config_path import find_file_in_all_drives
from utils.Task_utils import FileSingleton
from utils.auth import selfApi
from utils.flet_toast.toasts_flexible import ToastsFlexible
from utils.flet_toast.core import Position

toasts_history = {}
fileSingleton = FileSingleton()

try:
    if not os.path.exists("./user_settings.json"):
        fileSingleton.write_data({})
        print("User settings created")
except:
    pass
try:
    if not os.path.exists("./path.json"):
        fileSingleton.write_data(
            {
                "bluestacks": "C:\\ProgramData\\BlueStacks_nxt\\bluestacks.conf",
                "HD-Player": "C:\\Program Files\\BlueStacks_nxt\\HD-Player.exe"
            }
        )
        print("User settings created")
except:
    pass

data = fileSingleton.get_data()

if "discord" not in data:
    data["discord"] = {"user_id":0, "enabled":False}
    fileSingleton.write_data(data)

def update_user_info(password, username):
    data = fileSingleton.get_data()
    data["user"] = {'username': username, 'password': password}
    fileSingleton.write_data(data)

def getchecksum():
    md5_hash = hashlib.md5()
    try:
        file = open(''.join(sys.argv), "rb")
    except:
        file = open(''.join(sys.argv[0]), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

def is_str_valid(username, password):
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

class LoginUI(ft.Column):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_page = page
        self.fileSingleton = FileSingleton()
        self.data = self.fileSingleton.get_data()
        self.init()

    def show_banner(self, e):
        def close_banner(e):
            self.initial_page.banner.open = False
            self.initial_page.update()

        self.initial_page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            content=ft.Column(controls=[
                ft.TextButton(icon=ft.icons.LINK_OUTLINED, text="Pay with Stripe",
                              on_click=lambda _: self.initial_page.launch_url("https://buy.stripe.com/dR66oX4ov0qldkQaEF"),
                              ),
                ft.TextButton(icon=ft.icons.LINK_OUTLINED, text="Pay with Crypto",
                              on_click=lambda _: self.initial_page.launch_url(
                                  "https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099"))

            ]),
            actions=[
                ft.TextButton("Close", on_click=close_banner),
            ],
            content_padding=ft.padding.all(5)
        )

        self.initial_page.banner.open = True
        self.initial_page.update()

    def login(self, e):
        return                 Main(self.initial_page, "9999")
        try:
            self.initial_page.splash = ft.ProgressBar()
            self.button_login.disabled = True
            self.initial_page.update()

            username = self.textfield_username.value
            password = self.textfield_password.value

            if username == '' or password == '':
                return
            if not is_str_valid(username, password):
                self.initial_page.open_banner("Illegal characters..")
            if self.initial_page.keyauthapp.login(user=username, password=password, page=self.initial_page):
                update_user_info(password, username)

                target_date = datetime.utcfromtimestamp(int(self.initial_page.keyauthapp.user_data.expires))

                current_date = datetime.utcnow()
                days_remaining = (target_date - current_date).days

                self.initial_page.splash = None
                self.button_login.disabled = False

                Main(self.initial_page, days_remaining)

                self.initial_page.subscription_checker = threading.Thread(target=self.verify_subscription, args=(username, password))
                self.initial_page.subscription_checker.start()
            else:
                sleep(5)
                self.initial_page.splash = None
                self.initial_page.loginUI.button_login.disabled = False
                self.initial_page.update()
        except Exception as e:
            print(e)
            self.initial_page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()

    def verify_subscription(self, username, password):
        try:
            self.initial_page.keyauthapp = selfApi(
                name="Rokbd",
                ownerid="7oofxdj8uH",
                secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
                version="1.0",
                hash_to_check=getchecksum()
            )

            if self.initial_page.keyauthapp.login(user=username, password=password,page=self.initial_page):
                target_date = datetime.utcfromtimestamp(int(self.initial_page.keyauthapp.user_data.expires))

                current_date = datetime.utcnow()
                days_remaining = (target_date - current_date).days

                self.initial_page.title = f"Rok Bot - {days_remaining} Days left"
                self.initial_page.update()
                sleep(6 * 3600)
                return self.verify_subscription(username, password)
            else:
                for element in self.initial_page.tile_manager.tiles.values():
                    element.paused = False
                    element.stopped = True
                self.initial_page.window_width = 330
                self.initial_page.window_height = 330
                self.initial_page.clean()
                self.initial_page.add(self.initial_page.loginUI)
                self.initial_page.update()
        except Exception as e:
            print(e)
            self.initial_page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()

    def init(self):
        self.textfield_username = ft.TextField(label="Username", width=300, value=self.data.get("user",{}).get("username",""))
        self.textfield_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300, value=self.data.get("user",{}).get("password",""))
        self.button_login = ft.OutlinedButton(text="Login", on_click=self.login)
        self.subscribe_button = ft.FilledTonalButton(text="Subscribe", on_click=self.show_banner)



        return self.controls.extend([self.textfield_username, self.textfield_password,
                                     ft.Row(
                                         controls=[ft.Column(controls=[self.button_login], col=4),ft.Column(controls=[self.subscribe_button], col=6),], alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                                     )
                                     ])


def main(page: ft.Page):


    # return Main(page, 500)

    page.window_width = 330
    page.window_height = 330
    page.FileSingleton = FileSingleton()
    path_file = page.FileSingleton.get_path()

    cmd = f"{path_file['HD-Player'].replace('Player', 'Adb')} start-server"
    subprocess.Popen(cmd)

    if not os.path.exists(path_file['bluestacks']) or not os.path.exists(path_file['HD-Player']):
        progress_bar = ft.ProgressBar(visible=True)
        page.add(progress_bar)
        page.update()
        if result := find_file_in_all_drives('bluestacks\.conf'):
            path_file['bluestacks\.conf'.split("\\")[0]] = result
            with open('./path.json', 'w', encoding="UTF-8") as f:
                json.dump(path_file, f, indent=2)
        if result := find_file_in_all_drives('HD-Player\.exe'):
            path_file['HD-Player\.exe'.split("\\")[0]] = result
            with open('./path.json', 'w', encoding="UTF-8") as f:
                json.dump(path_file, f, indent=2)
        progress_bar.visible = False
        page.update()

    for i in range(5):
        ready = False
        try:
            page.keyauthapp = selfApi(
                name="Rokbd",
                ownerid="7oofxdj8uH",
                secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
                version="1.0",
                hash_to_check=getchecksum()
            )
            ready = True
        except Exception as e:
            print(e)
            page.keyauthapp = None
            print("Problem in the database loading..Wait a bit please..")
            sleep(5)
        if ready:break
    if not ready:
        page.window_close()

    def close_banner(e):
        page.banner.open = False
        page.update()

    def open_banner(text):
        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=page.close_banner),
            ],
            open=True
        )
        page.update()

    page.close_banner = close_banner
    page.open_banner = lambda text: open_banner(text)
    page.subscription_checker = threading.Thread()
    page.loginUI = LoginUI(page)
    page.UPGRADE = True
    page.body = ft.Container()

    def generate_toast(title, description, icon=ft.icons.INFO):
        ToastsFlexible(
            page=page,
            icon=icon,
            title=title,
            desc=description,
            auto_close=None,
            trigger=None,
            width=360,
            set_history=toasts_history,
            position=Position.TOP_RIGHT,
            bgcolor_title="AMBER"
        )

    page.generate_toast = lambda title, description, icon=ft.icons.INFO: generate_toast(title, description, icon)

    page.app_routes = [
        path(
            url="/",
            clear=True,
            view=index
        ),
        path(url=f"/citylayout/:instance_index/:profile_index",
             clear=False,
             view=viewCityLayout
        ),
        path(url=f"/profile/:instance_index/:profile_index/settings",
             clear=False,
             view=viewProfileSettings
        )
    ]

    page.routing = Routing(
        page=page,
        app_routes=page.app_routes,
    )

    page.add(page.loginUI)

    page.update()



def index(page: ft.Page, params, basket):
    return ft.View(route="/", controls=page.controls)

if __name__ == '__main__':
    ft.app(target=main)
