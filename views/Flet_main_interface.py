import flet as ft
from flet_route import path, Routing

from views import Flet_TileManager
from viewscod import Flet_TileManager_cod
color_bank ={
    1:"#3b8ed0",
    2:"#ba4543",
    3:"#dec433"
}

def index(page: ft.Page, params, basket):
    return  ft.View("/", controls=page.controls,)

def Main(page: ft.Page, days=950):
    page.title = f"Rok Bot - {days} Days left"
    page.frames = {}
    page.window_width = 400
    page.tile_manager = Flet_TileManager.TileManager(page)

    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.FADE_UPWARDS
    page.theme = theme
    page.update()

    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.tile_manager.refresh()
    page.tile_manager.update_tiles()


def Main_cod(page: ft.Page, days=950):
    page.title = f"Cod Bot - {days} Days left"
    page.frames = {}
    page.window_width = 400
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
