import logging
import platform

logging.basicConfig(level=logging.ERROR)
import json
import os
import subprocess
import sys
import traceback
from time import sleep

import flet as ft
from flet_route import Routing, path

try:
    from utils.Components.AnimatedCard import AnimatedCard
    from utils.Components.card import GenerateCard
    from utils.Components.filescan import generate_filescan
    from utils.Components.maintenance import generate_maintenance
    from utils.Components.PaymentMethods import payment_methods
    from utils.constants import BOT_NAME, TOAST_HISTORY, VERSION_NUMBER, VERSION_TYPE
    from utils.flet_toast.core import Position
    from utils.flet_toast.toasts_flexible import ToastAction, ToastsFlexible
    from utils.flet_translations import translate
    from utils.functions import FileSingleton, get_dic_instances, get_dic_instances_ld, getchecksum
    from utils.singletons import ApiSingleton, EmulatorSingleton, SettingsSingleton
    from utils.supabase_auth import SupabaseClient
    from views.city_layout import viewCityLayout, viewSetCenterMap
    from views.config_path import find_file_in_all_drives
    from views.login.login import LoginScreen
    from views.main import Main
    from views.profile_settings import viewProfileSettings
    from views.settings.general._settings import AllSettings
    from views.worker_slave_management import WorkerSlaveManagement
except Exception as e:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback_list = traceback.format_exception(exc_type, exc_value, exc_traceback)
    traceback_str = "".join(traceback_list)
    traceback.print_exc()

    def handleError(page: ft.Page):
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.vertical_alignment = ft.MainAxisAlignment.CENTER
        page.add(ft.Text("An error occurred, send this message to the developer", selectable=True))
        page.add(ft.Text(value=traceback_str, color="red", selectable=True))
        page.update()

    ft.app(target=handleError)
    exit()

fileSingleton = FileSingleton()
data = fileSingleton.getCachedData()

if "API_KEY" not in data:
    data["API_KEY"] = ""
    fileSingleton.write_data(data)

if "workers" not in data:
    data["workers"] = {"ld": {}, "bluestacks": {}, "pc": {}}
    fileSingleton.write_data(data)

if "pc" not in data["workers"]:
    data["workers"]["pc"] = {}
    fileSingleton.write_data(data)

if "interface" not in data:
    data["interface"] = {"auto_scroll": True, "auto_refresh": True, "limit_logs": True}
    fileSingleton.write_data(data)

if "discord" not in data:
    data["discord"] = {"user_id": 0, "enabled": False}
    fileSingleton.write_data(data)

for instances in data:
    if not "schedules" in data[instances]:
        continue
    for profiles in data[instances]["schedules"]:
        if data[instances]["schedules"][profiles]["gather_rss_method"] not in ["default", "spiral"]:
            data[instances]["schedules"][profiles]["gather_rss_method"] = "default"
            fileSingleton.write_data(data)


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window_width = 450
    page.window_height = 400
    page.FileSingleton = FileSingleton()

    page.loginUI = LoginScreen(page)
    page.UPGRADE = True
    page.body = ft.Column()
    page.padding = ft.padding.all(0)

    def generate_toast(title, description, icon=ft.icons.INFO, bgcolor_title="AMBER"):
        ToastsFlexible(
            page=page,
            icon=icon,
            title=title,
            desc=description,
            auto_close=None,
            trigger=None,
            width=360,
            set_history=TOAST_HISTORY,
            position=Position.TOP_RIGHT,
            bgcolor_title=bgcolor_title,
        )

    page.generate_toast = lambda title, description, icon=ft.icons.INFO, bgcolor_title="AMBER": generate_toast(
        title, description, icon, bgcolor_title
    )

    page.app_routes = [
        path(url="/", clear=True, view=index),
        path(url="/login", clear=True, view=login),
        path(url=f"/emulator-choice", clear=True, view=emulator_choice),
        path(url=f"/emulator-loading", clear=True, view=loading_files),
        path(
            url=f"/city-layout/:instance_index/:profile_index",
            clear=True,
            view=viewCityLayout,
        ),
        path(
            url=f"/set-center/:task/:instance_index/:profile_index",
            clear=True,
            view=viewSetCenterMap,
        ),
        path(
            url=f"/profile/:instance_index/:profile_index/settings",
            clear=True,
            view=viewProfileSettings,
        ),
        path(url="/configure-workers", clear=True, view=configure_workers),
        path(url="/settings", clear=True, view=settings),
    ]

    page.routing = Routing(
        page=page,
        app_routes=page.app_routes,
    )

    supabaseClient = SupabaseClient()
    updates = supabaseClient.getUpdates()
    force = False

    for update in updates:
        if update["force"]:
            force = True

    for update in updates:
        if update["version"] == VERSION_NUMBER:
            continue
        if force:
            page.launch_url(update["download_link"])
            sleep(1)
            page.window_destroy()
            sys.exit(0)

        ToastsFlexible(
            page=page,
            width=280,
            position=Position.BOTTOM_LEFT,
            no_live_time=True,
            set_history_title="Update available",
            set_history_desc=None,
            set_history=TOAST_HISTORY,
            desc=ft.Row(
                expand=True,
                alignment=ft.MainAxisAlignment.START,
                vertical_alignment=ft.CrossAxisAlignment.START,
                spacing=12,
                controls=[
                    ft.Icon(ft.icons.UPDATE, size=24),
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.START,
                        spacing=0,
                        controls=[
                            ft.Text(
                                "Update available",
                                style=ft.TextThemeStyle.BODY_MEDIUM,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                f"A new software version is available for download (v{update['version']}).",
                                style=ft.TextThemeStyle.LABEL_MEDIUM,
                                width=210,
                                opacity=0.8,
                            ),
                        ],
                    ),
                ],
            ),
            actions_alignment=ft.MainAxisAlignment.START,
            actions=[
                ToastAction(
                    text="Update",
                    width=100,
                    action_style="filled",
                    disabled=False,
                    on_click=lambda e: page.launch_url(update["download_link"]),
                )
            ],
        )
        break
    page.go("/login")
    page.update()


def index(page: ft.Page, params, basket):
    page.window_width = 450
    page.window_height = 750

    return ft.View(route="/", controls=page.body.controls)


def loading_files(page: ft.Page, params, basket):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    return ft.View(
        route="/emulator-loading",
        controls=[ft.ProgressRing(visible=True), generate_filescan()],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        vertical_alignment=ft.MainAxisAlignment.CENTER,
    )


def emulator_choice(page: ft.Page, params, basket):
    page.window_width = 1920 / 2
    page.window_height = 1080 / 2

    def go_main(e):
        if platform.system() == "Darwin":
            EmulatorSingleton().setEmulator("ld")

            return Main(page)

        path_file = FileSingleton().get_path()

        print(e.control.data)
        if "bluestacks" in e.control.data:
            EmulatorSingleton().setEmulator("bluestacks")

            if not os.path.exists(path_file["bluestacks"]) or not os.path.exists(path_file["HD-Player"]):
                page.go("/emulator-loading")
                page.update()

                if result := find_file_in_all_drives("bluestacks\.conf"):
                    path_file["bluestacks\.conf".split("\\")[0]] = result
                    with open("./path.json", "w", encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)

                if result := find_file_in_all_drives("HD-Player\.exe"):
                    path_file["HD-Player\.exe".split("\\")[0]] = result
                    with open("./path.json", "w", encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)

            cmd = f"{path_file['HD-Player'].replace('Player', 'Adb')} start-server"
            subprocess.Popen(cmd)

        elif "ld" in e.control.data:
            EmulatorSingleton().setEmulator("ld")

            if not path_file.get("LD-Console", False) or not os.path.exists(path_file.get("LD-Console", "fzfgrerg")):
                page.go("/emulator-loading")
                page.update()

                if result := find_file_in_all_drives(r"LDPlayer9\\ldconsole\.exe"):
                    path_file["LD-Console"] = result
                    with open("./path.json", "w", encoding="UTF-8") as f:
                        json.dump(path_file, f, indent=2)
                else:
                    page.generate_toast("LD9 Missing", "Unable to load LD Player 9 Configuration")
                    while 1:
                        sleep(1)

            cmd = f"{path_file['LD-Console'].replace('ldconsole', 'adb')} start-server"
            subprocess.Popen(cmd)
        elif "pc" in e.control.data:
            EmulatorSingleton().setEmulator("pc")

        Main(page)

    return ft.View(
        route="/emulator-choice",
        controls=[
            ft.Stack(
                controls=[
                    ft.Row(
                        controls=[
                            AnimatedCard("bluestacks_logo.png", go_main),
                            AnimatedCard("ld_logo.png", go_main),
                            # AnimatedCard("pc.ico", go_main, "tier4") ,
                        ],
                        top=100,
                        left=120,
                    ),
                ]
            )
        ],
        vertical_alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        padding=0,
    )


def login(page: ft.Page, params, basket):
    page.window_width = 1920 / 2
    page.window_height = 1080 / 2
    page.window_resizable = False
    page.title = BOT_NAME

    return ft.View(route="/login", controls=[LoginScreen(page)], padding=0)


def settings(page: ft.Page, params, basket):
    controls = [
        ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: page.go("/"),
                ),
                ft.Text(value="Back", size=20),
            ]
        ),
        ft.Divider(height=1),
        AllSettings(page, "0"),
    ]

    return ft.View(route="/settings", controls=controls)


def configure_workers(page: ft.Page, params, basket):
    page.window_width = 1920 / 2
    page.window_height = 720

    def go_back_and_refresh(e):
        page.go("/")
        page.tile_manager.refresh()

    controls = [
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=go_back_and_refresh,
                    ),
                    ft.Text(value="Back", size=20),
                ],
            ),
            padding=ft.padding.only(top=5, left=0, bottom=0),
        ),
        ft.Divider(),
    ]

    inside = []
    inside.append(
        GenerateCard(
            subtitle=translate(
                "The emulator requires a 'Worker' to execute tasks. Once you start a worker, worker will start the first assigned emulator, perform actions, close it, and then proceed to the next emulator in sequence. Decreasing the number of workers will result in fewer simultaneous windows, while increasing it will lead to a higher number of concurrent windows."
            )
        )
    )
    inside.append(ft.Divider())
    inside.append(WorkerSlaveManagement(page))

    controls.append(ft.ListView(controls=inside, expand=1))

    return ft.View(route="/configure-workers", controls=controls)


if __name__ == "__main__":
    ft.app(target=main)
