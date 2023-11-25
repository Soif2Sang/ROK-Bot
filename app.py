# coding=UTF-8
import json
import os
import subprocess
import sys
import traceback
from time import sleep

import flet as ft
from flet_route import Routing, path

from utils.auth import selfApi
from utils.Components.AnimatedCard import AnimatedCard
from utils.Components.filescan import generate_filescan
from utils.Components.maintenance import generate_maintenance
from utils.constants import BREZILIAN, toasts_history
from utils.functions import FileSingleton, getchecksum
from views.login.login import LoginUI

from utils.flet_toast.core import Position
from utils.flet_toast.toasts_flexible import ToastsFlexible
from utils.singletons import ApiSingleton, EmulatorSingleton, LinkSingleton
from views.city_layout import viewCityLayout
from views.config_path import find_file_in_all_drives
from views.main import Main
from views.profile_settings import viewProfileSettings

try:
    1
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
        name="Rokbd" if not BREZILIAN else "RokbdBR",
        ownerid="7oofxdj8uH",
        secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0" if not BREZILIAN else "6d15b7ee5e7312238105efd4b648535835dc1ce5f4250fe2dc82910db43147b6",
        version="2.0",
        hash_to_check=getchecksum()
    )

    keyauthapp.log(traceback_str)

    ft.app(target=handleError)
    exit()

fileSingleton = FileSingleton()

def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 400
    page.FileSingleton = FileSingleton()

    ready = False

    for i in range(3):
        ready = False
        try:
            page.keyauthapp = selfApi(
                name="Rokbd" if not BREZILIAN else "RokbdBR",
                ownerid="7oofxdj8uH",
                secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0" if not BREZILIAN else "6d15b7ee5e7312238105efd4b648535835dc1ce5f4250fe2dc82910db43147b6",
                version="2.0",
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
            generate_maintenance()
        )

        while 1:
            sleep(1)

    def create_banner(text):
        return ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=lambda _ :page.close_banner()),
            ],
            open=True
        )

    page.open_banner = lambda text: page.show_banner(create_banner(text))
    page.loginUI = LoginUI(page)
    page.UPGRADE = False
    page.body = ft.Column()

    def generate_toast(title, description, icon=ft.icons.INFO, bgcolor_title="AMBER"):
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
            bgcolor_title=bgcolor_title
        )

    page.generate_toast = lambda title, description, icon=ft.icons.INFO, bgcolor_title="AMBER": generate_toast(title,
                                                                                                               description,
                                                                                                               icon,
                                                                                                            bgcolor_title)

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
            url=f"/emulator-choice",
            clear=True,
            view=emulator_choice
        ),
        path(
            url=f"/emulator-loading",
            clear=True,
            view=loading_files
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

    if not BREZILIAN:
        LinkSingleton().setStripeLink(page.keyauthapp.var('stripe'))
        LinkSingleton().setSellixLink(page.keyauthapp.var('sellix'))


def index(page: ft.Page, params, basket):
    return ft.View(route="/", controls=page.body.controls)

def loading_files(page: ft.Page, params, basket):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    return ft.View(route="/emulator-loading", controls=[ft.ProgressRing(visible=True), generate_filescan()], horizontal_alignment = ft.CrossAxisAlignment.CENTER, vertical_alignment = ft.MainAxisAlignment.CENTER)

def emulator_choice(page: ft.Page, params, basket):
    page.window_width = 1920 / 2
    page.window_height = 1080 / 2

    def go_main(e):
        path_file = FileSingleton().get_path()

        if "bluestacks" in e.control.data:
            EmulatorSingleton().setEmulator("bluestacks")

            if not os.path.exists(path_file['bluestacks']) or not os.path.exists(path_file['HD-Player']):
                page.go('/emulator-loading')
                page.update()

                if result := find_file_in_all_drives('bluestacks\.conf'):
                    path_file['bluestacks\.conf'.split("\\")[0]] = result
                    with open('./path.json', 'w', encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)

                if result := find_file_in_all_drives('HD-Player\.exe'):
                    path_file['HD-Player\.exe'.split("\\")[0]] = result
                    with open('./path.json', 'w', encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)

            cmd = f"{path_file['HD-Player'].replace('Player', 'Adb')} start-server"
            subprocess.Popen(cmd)

        elif "ld" in e.control.data :
            EmulatorSingleton().setEmulator("ld")

            if not path_file.get('LD-Console', False) or not os.path.exists(path_file['LD-Console']):
                page.go('/emulator-loading')
                page.update()

                if result := find_file_in_all_drives(r'LDPlayer9\\ldconsole\.exe'):
                    path_file['LD-Console'] = result
                    with open('./path.json', 'w', encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)

            cmd = f"{path_file['LD-Console'].replace('ldconsole', 'adb')} start-server"
            subprocess.Popen(cmd)

        Main(page)

    return ft.View(route="/emulator-choice", controls=[ft.Stack(controls=[
        ft.Container(image_src=f"rok_wallpaper.webp", width=1920 / 2, height=1080 / 2, image_fit=ft.ImageFit.COVER),

        ft.Row(
            controls=[AnimatedCard("bluestacks_logo.png", go_main), AnimatedCard("ld_logo.png", go_main)],
            top=100,
            left=240
        ),

    ])], vertical_alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER, padding=0)



def login(page: ft.Page, params, basket):
    page.window_width = 1920 / 2
    page.window_height = 1080 / 2
    page.window_resizable = False
    page.title = "RokNet"

    return ft.View(route="/login",
                   controls=[
                       ft.Stack(
                           controls=[
                               ft.Container(
                                   image_src=f"./rok_wallpaper.webp",
                                   width=1920 / 2,
                                   height=1080 / 2,
                                   image_fit=ft.ImageFit.COVER
                               ),

                               ft.Container(
                                   blur=100,
                                   width=400,
                                   height=250,
                                   right=1920 / 4 - 400 / 2,
                                   top=1080 / 4 - 250 / 2 - 15,
                                   content=ft.Container(content=page.loginUI, height=160, width=300,
                                                        ),
                                   alignment=ft.Alignment(0, 0),
                                   border_radius=5,
                                   border=ft.border.all(3, ft.colors.GREY_900)
                               ),

                           ]
                       )
                   ],
                   vertical_alignment=ft.MainAxisAlignment.CENTER,
                   horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                   padding=0
       )


if __name__ == '__main__':
    ft.app(target=main)
