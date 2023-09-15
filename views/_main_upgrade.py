import flet as ft
from flet_route import path, Routing

from tiles.handler.logging_handler import LoggerUpgrade
from tiles.handler.tile_handler_upgrade import TileManagerUpgrade

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
    page.tile_manager = TileManagerUpgrade(page)
    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.update()
    # page.tile_manager.refresh()
    page.add(page.tile_manager.start_bar)
    page.tile_manager.start_bar.tile_manager = page.tile_manager
    # print(page.logger)
    page.logger = LoggerUpgrade(page)
    page.add(page.logger)
    page.update()

    page.app_routes = [path(
        url="/",
        clear=True,
        view=index
    )]

    page.routing = Routing(
        page=page,  # Here you have to pass the page. Which will be found as a parameter in all your views
        app_routes=page.app_routes,
        # Here a list has to be passed in which we have defined app routing like app_routes
    )


if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
