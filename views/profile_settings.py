import flet as ft
import flet_route
from views.frametime import ManagerTimezone

def viewProfileSettings(page: ft.Page, params: flet_route.Params, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500

    def returnHome():
        page.window_width = 450
        page.window_height = 700
        page.go("/")

    return ft.View(
        f"/profile/{params.instance_index}/{params.profile_index}/settings",
        controls=[
            ft.Container(bgcolor="#ecf0f1",
                         content=ft.Row(controls=[
                             ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: returnHome()),
                             ft.Text(value="Go back")
                         ]
                         )
                         ),
            ManagerTimezone(params.instance_index, params.profile_index)
        ]
    )