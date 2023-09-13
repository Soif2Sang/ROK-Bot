import flet as ft
import flet_route
from views.Flet_city_layout import CityPlacement

def viewCityLayout(page: ft.Page, params: flet_route.Params, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500
    page.tile_manager.tiles[str(params.instance_index)].runner.adb.save_screen("city")

    def returnHome():
        page.window_width = 450
        page.window_height = 700
        page.go("/")

    return ft.View(
        f"/citylayout/{params.instance_index}/{params.profile_index}",
        controls=[
            ft.Container(bgcolor="#ecf0f1",
                         content=ft.Row(controls=[
                             ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: returnHome()),
                             ft.Text(value="Go back")
                         ]
                         )
                         ),
            ft.Text(value="Click on the building button you wanna set, then click in the center of the building."),
            CityPlacement(params.instance_index, params.profile_index)
        ]
    )