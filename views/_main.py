import threading
from time import sleep

import flet as ft

from views.tiles.handler.tile_handler import TileHandler
from views._body import Body
from viewscod import Flet_TileManager_cod
color_bank ={
    1:"#3b8ed0",
    2:"#ba4543",
    3:"#dec433"
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
    page.title = f"Rok Bot - {days} Days left"
    page.frames = {}

    page.window_width = 450
    page.window_height = 700
    page.clean()

    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.FADE_UPWARDS
    page.theme = theme
    page.update()

    page.tile_manager = TileHandler(page)

    page.add(
        page.tile_manager,
        ft.Divider(height=0,)
    )

    page.tile_manager.refresh()

    # def process_is_alive():
    #     while 1:
    #         changed = False
    #         for tile in body.tile_manager.tiles.values():
    #             if (not tile.tasks_process.is_alive() and tile.button_start.icon == ft.icons.PAUSE) and (page.route == '/'):
    #                 tile.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
    #                 tile.button_stop.disabled = True
    #                 tile.set_text("")
    #                 changed = True
    #         sleep(0.1)
    #         if changed:
    #             page.update()

    # is_alive = threading.Thread(target=process_is_alive)
    # is_alive.deamon = True
    # is_alive.start()

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
