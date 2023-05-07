import flet as ft

from views import Flet_TileManager
from viewscod import Flet_TileManager_cod
color_bank ={
    1:"#3b8ed0",
    2:"#ba4543",
    3:"#dec433"
}


def Main(page: ft.Page, days=950):
    page.title = f"Rok Bot - {days} Days left"
    page.frames = {}
    page.window_width = 400
    page.tile_manager = Flet_TileManager.TileManager(page)
    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.tile_manager.refresh()
    page.update()
    page.tile_manager.update_tiles()

def Main_cod(page: ft.Page, days=950):
    page.title = f"Cod Bot - {days} Days left"
    page.frames = {}
    page.window_width = 400
    page.tile_manager = Flet_TileManager_cod.TileManager(page)
    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.tile_manager.refresh()
    page.update()
    page.tile_manager.update_tiles()

if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
