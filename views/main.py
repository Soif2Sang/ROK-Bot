import json
import sys
import time
import traceback

import flet as ft

from tiles.handler.tile_handler_worker import TileHandlerWorker
from views.tiles.handler.tile_handler_u import TileManagerUpgrade
from utils.constants import VERSION, toasts_history
from utils.flet_toast.core import Position
from utils.flet_toast.toasts_flexible import ToastAction, ToastsFlexible
from views.tiles.handler.tile_handler import TileHandler

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


def Main(page: ft.Page, days=950):
    # page.clean()
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.CUPERTINO
    page.vertical_alignment = None
    page.horizontal_alignment = None
    page.frames = {}
    page.window_resizable = True
    page.window_width = 500
    page.window_height = 800
    page.theme = theme

    if page.UPGRADE:
        page.tile_manager = TileHandlerWorker(page)
    else:
        page.tile_manager = TileHandler(page)

    page.body = ft.Column(controls=[page.tile_manager, ft.Divider(height=0)])

    # if page.UPGRADE:
    #     page.body.controls.append(page.tile_manager.start_bar)

    page.go("/")
    page.tile_manager.refresh()

    REMOTE_VERSION = page.keyauthapp.var("version")
    try:
        version_json = json.loads(REMOTE_VERSION)
    except:
        traceback.print_exc()
        version_json = {"version": "-1", "force": False, "download_link": ""}

    GLOBAL_MESSAGE = page.keyauthapp.var("message")
    PERSONAL_MESSAGE = page.keyauthapp.getvar("message").replace("None", "")
    if version_json["version"] > VERSION:
        if version_json["force"]:
            page.launch_url(version_json["download_link"])
            time.sleep(1)
            page.window_destroy()
            sys.exit(0)

        ToastsFlexible(
            page=page,
            width=280,
            position=Position.BOTTOM_LEFT,
            no_live_time=True,
            set_history_title="Update available",
            set_history_desc=None,
            set_history=toasts_history,
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
                                f"A new software version is available for download (v{version_json['version']}).",
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
                    on_click=lambda e: page.launch_url(version_json["download_link"]),
                )
            ],
        )

    try:
        message_json = json.loads(GLOBAL_MESSAGE)
        if int(message_json["end"]) > time.time() > int(message_json["start"]):
            ToastsFlexible(
                page=page,
                icon=ft.icons.NOTIFICATION_IMPORTANT_OUTLINED,
                title="Announcements",
                bgcolor_title="red",
                desc=message_json["message"],
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
            )
    except:
        pass

    try:
        message_json = json.loads(PERSONAL_MESSAGE)
        if (not message_json["read"]) and (int(message_json["end"]) > time.time() > int(message_json["start"])):

            def accept_message(e):
                message_json["read"] = True
                page.keyauthapp.setvar("message", json.dumps(message_json))

            ToastsFlexible(
                page=page,
                icon=ft.icons.ANNOUNCEMENT_OUTLINED,
                title="Private Messages",
                bgcolor_title=ft.colors.BLUE_300,
                desc=message_json["message"],
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
                actions=[
                    ToastAction(
                        text="I have read",
                        action_style="texted",
                        on_click=accept_message,
                    )
                ],
            )
    except:
        pass


if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
