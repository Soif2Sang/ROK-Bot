import flet as ft

from utils.Task_utils import VERSION, toasts_history
from utils.flet_toast.core import Position
from utils.flet_toast.toasts_flexible import ToastsFlexible, ToastAction
from views.tiles.handler.tile_handler import TileHandler
from viewscod import Flet_TileManager_cod

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}

class BodyView(ft.View):
    def __init__(self, initial_page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_page = initial_page
        self.expand = True
        self.tile_manager = TileHandler(self.initial_page)
        self.initial_page.tile_manager = self.tile_manager
        self.current_frame = ft.Container()

        self.controls = [
            self.tile_manager,
            ft.Divider(),
            self.current_frame
        ]


def Main(page: ft.Page, days=950):
    # page.clean()

    page.title = f"RokNet - {days} Days left"
    page.frames = {}
    page.window_width = 450
    page.window_height = 700

    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.CUPERTINO
    page.theme = theme
    page.update()

    page.tile_manager = TileHandler(page)

    page.body = ft.Column(controls=[page.tile_manager, ft.Divider(height=0)])

    # page.add(
    #     page.tile_manager,
    #     ft.Divider(height=0,)
    # )

    page.go('/')
    # page.update()
    page.tile_manager.refresh()

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

def Main_cod(page: ft.Page, days=950):
    page.title = f"Cod Bot - {days} Days left"
    page.frames = {}
    page.window_width = 450
    page.tile_manager = Flet_TileManager_cod.TileManager(page)

    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.FADE_UPWARDS
    page.theme = theme
    page.update()

    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.tile_manager.refresh()
    page.tile_manager.update_tiles()


if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
