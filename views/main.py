import flet as ft
from utils.constants import VERSION, toasts_history
from utils.flet_toast.core import Position
from utils.flet_toast.toasts_flexible import ToastsFlexible, ToastAction
from views.tiles.handler.tile_handler import TileHandler

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}

def Main(page: ft.Page, days=950):
    # page.clean()
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.CUPERTINO
    page.vertical_alignment = None
    page.horizontal_alignment = None
    page.frames = {}
    page.window_resizable = True
    page.window_width = 450
    page.window_height = 700
    page.theme = theme
    page.tile_manager = TileHandler(page)
    page.body = ft.Column(controls=[page.tile_manager, ft.Divider(height=0)])
    page.go('/')
    page.tile_manager.refresh()

    def fetchNews():
        if VERSION != page.keyauthapp.var('version'):
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
                                ft.Text("Update available",
                                        style=ft.TextThemeStyle.BODY_MEDIUM,
                                        weight=ft.FontWeight.BOLD
                                        ),
                                ft.Text("A new software version is available for download.",
                                        style=ft.TextThemeStyle.LABEL_MEDIUM,
                                        width=210,
                                        opacity=0.8
                                        ),
                            ]
                        ),
                    ]
                ),
                actions_alignment=ft.MainAxisAlignment.START,
                actions=[
                    ToastAction(
                        text="Update",
                        width=100,
                        action_style="filled",
                        disabled=False,
                        on_click=lambda e: page.launch_url(page.keyauthapp.var('download_link')),
                    )
                ]
            )
        if message:=page.keyauthapp.var('message').replace('None',''):
            ToastsFlexible(
                page=page,
                icon=ft.icons.NOTIFICATION_IMPORTANT_OUTLINED,
                title="Announcements",
                bgcolor_title="red",
                desc=message,
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
            )

        if message:=page.keyauthapp.getvar('message').replace('None',''):
            ToastsFlexible(
                page=page,
                icon=ft.icons.ANNOUNCEMENT_OUTLINED,
                title="Private Messages",
                bgcolor_title=ft.colors.BLUE_300,
                desc=message,
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
                actions=[
                    ToastAction(
                        text="I have read",
                        action_style="texted",
                        on_click=lambda e: page.keyauthapp.setvar('message', 'None'),
                    )
                ]
            )

    fetchNews()
    # threading.Thread(target=threadFetchNews, name="FetchNews").start()


if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
