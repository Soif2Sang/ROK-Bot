# coding=UTF-8
import json
import os
import subprocess
import sys
import threading
import traceback
from time import sleep

import flet as ft
from flet_route import path, Routing

from utils.Task_utils import getchecksum
from utils.auth import selfApi
from utils.handle_files import main as HandleFiles
from views.login.login import LoginUI

try:
    from views.city_layout import viewCityLayout
    from views.profile_settings import viewProfileSettings
    from views._main import Main
    from views.config_path import find_file_in_all_drives
    from utils.Task_utils import FileSingleton, ApiSingleton
    from utils.flet_toast.toasts_flexible import ToastsFlexible
    from utils.flet_toast.core import Position
except Exception as e:

    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_str = ''.join(traceback_list)

    def handleError(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.add(ft.Text("An error occurred, a log message have been sent to the developer"))
        page.add(ft.Text(value=traceback_str, color="red"))
        page.update()


    keyauthapp = selfApi(
        name="Rokbd",
        ownerid="7oofxdj8uH",
        secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
        version="1.0",
        hash_to_check=getchecksum()
    )

    keyauthapp.log(traceback_str)

    ft.app(target=handleError)
    exit()

toasts_history = {}
fileSingleton = FileSingleton()

HandleFiles()

def main(page: ft.Page):
    # return Main(page, 500)

    page.window_width = 330
    page.window_height = 330
    page.FileSingleton = FileSingleton()
    path_file = page.FileSingleton.get_path()

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

    cmd = f"{path_file['HD-Player'].replace('Player', 'Adb')} start-server"
    subprocess.Popen(cmd)

    ready = False

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
            sleep(5)
        if ready:
            break

    if not ready:
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.add(
            ft.Card(
                content=ft.Container(
                    content=
                    ft.ListTile(
                        title=ft.Text("The Bot seems to be under maintenance, please wait a bit..")
                        , leading=ft.Icon(ft.icons.PORTABLE_WIFI_OFF_SHARP)
                    ),
                    width=400,
                    padding=10,
                ),
                color=ft.colors.SURFACE_VARIANT
            )
        )

        while 1:
            sleep(1)

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
    page.UPGRADE = False
    page.body = ft.Column()

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
        path(
            url="/login",
            clear=True,
            view=login
        ),
        path(
            url=f"/citylayout/:instance_index/:profile_index",
            clear=True,
            view=viewCityLayout
         ),
        path(
            url=f"/profile/:instance_index/:profile_index/settings",
            clear=True,
            view=viewProfileSettings
         )
    ]

    page.routing = Routing(
        page=page,
        app_routes=page.app_routes,
    )

    page.go("/login")
    page.update()


def index(page: ft.Page, params, basket):
    return ft.View(route="/", controls=page.body.controls)

def login(page: ft.Page, params, basket):
    return ft.View(route="/login", controls=[page.loginUI])


if __name__ == '__main__':
    ft.app(target=main)
