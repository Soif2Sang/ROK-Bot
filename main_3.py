import hashlib
import os
import sys
import threading
from datetime import datetime, date
import threading
from time import sleep
from flet_route import path, Routing
import flet as ft

import Flet_main_interface
from Task_utils import FileSingleton
from auth import selfApi


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

class LoginUI(ft.View):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fileSingleton = FileSingleton()
        self.data = self.fileSingleton.get_data()
        self.route = '/login'
        self.page = page
        self.init()

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
            # actions=[
            #     ft.TextButton("Ok", on_click=self.close_banner),
            # ],
            open=True
        )
        self.page.update()

    def init(self):
        self.textfield_username = ft.TextField(label="Username", width=300, value=self.data.get("user",{}).get("username",""))
        self.textfield_password = ft.TextField(label="Password", password=True, can_reveal_password=True, width=300,value=self.data.get("user",{}).get("password",""))
        self.button_login = ft.FilledButton(text="Login", on_click=self.page.button_clicked, width=100)

        return self.controls.extend([self.textfield_username, self.textfield_password, self.button_login])


def main(page: ft.Page):
    page.window_width = 330
    page.window_height = 330


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
        except :
            page.keyauthapp = None
            print("Problem in the database loading..Wait a bit please..")
            sleep(5)
        if ready:break
    if not ready:
        page.window_close()

    def close_banner():
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

    def login():
        page.splash = ft.ProgressBar()
        page.loginUI.button_login.text="test"
        page.loginUI.button_login.disabled = True
        page.update()

        username = page.loginUI.textfield_username.value
        password = page.loginUI.textfield_password.value

        if username == '' or password == '':
            return
        if not is_str_valid(username, password):
            page.pop_banner("Illegal characters..")
        # sleep(3)
        print('You pressed login button')
        return
        if page.keyauthapp.login(user=username, password=password, page=page):
            date_brut = \
            datetime.utcfromtimestamp(int(page.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[
                0]
            heures = date_brut.split('-')
            future = date(int(heures[0]), int(heures[1]), int(heures[2]))
            diff = future - date.today()
            page.splash = None
            page.update()
            page.go('/')
            page.window_width = 400
            page.window_height = 700
            Flet_main_interface.Main(page, diff.days)
            threading.Thread(target=page.verify_subscription, args=(username, password))

    def verify_subscription(username, password):
        try:
            page.keyauthapp = selfApi(
                name="Rokbd",
                ownerid="7oofxdj8uH",
                secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
                version="1.0",
                hash_to_check=getchecksum()
            )

            if page.keyauthapp.login(user=username, password=password,page=page):
                date_brut = datetime.utcfromtimestamp(int(page.keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
                heures = date_brut.split('-')
                future = date(int(heures[0]), int(heures[1]), int(heures[2]))
                diff = future - date.today()
                page.title = f"Rok Bot - {diff.days} Days left"
                page.update()
                sleep(24 * 3600)
                return page.verify_subscription(username, password)
            else:
                page.clean()
                for element in page.page.tile_manager.tiles.values():
                    element.paused = False
                    element.stopped = True
                page.go('/login')
                page.update()
        except Exception as e:
            print(e)
            page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()

    def button_clicked(e):
        page.loginUI.button_login.text = "Clicked"
        page.loginUI.button_login.disabled = True
        page.update()
        print("button clicked !")

    page.button_clicked = button_clicked

    page.close_banner = lambda _: close_banner()
    page.open_banner = lambda text: open_banner(text)
    page.login = login
    page.verify_subscription = lambda username, password : verify_subscription(username, password)
    page.loginUI = LoginUI(page)



    page.app_routes = [
        path(
            url="/login",
            clear=True,
            view=lambda page, params, basket : LoginUI(page)
        ),
        path(
                url="/",
                clear=True,
                view=index
            )
    ]

    page.routing = Routing(
        page=page,  # Here you have to pass the page. Which will be found as a parameter in all your views
        app_routes=page.app_routes,
        # Here a list has to be passed in which we have defined app routing like app_routes
    )

    page.go('/login')
    page.update()

def index(page: ft.Page, params, basket):
    return  ft.View("/", controls=page.controls,)

def loginView(page: ft.Page, params, basket):
    return page.loginUI

if __name__ == '__main__':
    ft.app(target=main)
