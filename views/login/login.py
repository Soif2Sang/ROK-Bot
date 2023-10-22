import os
import sys
import threading
from datetime import datetime
from time import sleep

import flet as ft

from views._main import Main
from utils.auth import selfApi, update_user_info
from utils.Task_utils import FileSingleton, ApiSingleton, getchecksum


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
                              on_click=lambda _: self.initial_page.launch_url(
                                  "https://buy.stripe.com/dR66oX4ov0qldkQaEF"),
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
                ApiSingleton().setApiKey(self.initial_page.keyauthapp.var('2captcha'))
                Main(self.initial_page, days_remaining)

                self.initial_page.subscription_checker = threading.Thread(target=self.verify_subscription,
                                                                          args=(username, password))
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

            if self.initial_page.keyauthapp.login(user=username, password=password, page=self.initial_page):
                target_date = datetime.utcfromtimestamp(int(self.initial_page.keyauthapp.user_data.expires))

                current_date = datetime.utcnow()
                days_remaining = (target_date - current_date).days

                self.initial_page.title = f"RokNet - {days_remaining} Days left"
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
        self.textfield_username = ft.TextField(
            label="Username",
            width=300,
            value=self.data.get("user", {}).get("username", "")
        )
        self.textfield_password = ft.TextField(
            label="Password",
            password=True,
            can_reveal_password=True,
            width=300,
            value=self.data.get("user", {}).get("password", "")
        )
        self.button_login = ft.OutlinedButton(
            text="Login",
            on_click=self.login
        )
        self.subscribe_button = ft.FilledTonalButton(
            text="Subscribe",
            on_click=self.show_banner
        )

        return self.controls.extend([
            self.textfield_username,
            self.textfield_password,
            ft.Row(
                controls=[
                    ft.Column(controls=[self.button_login], col=4),
                    ft.Column(controls=[self.subscribe_button], col=6),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        ])
