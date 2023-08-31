import flet as ft
import flet_route
from views.Flet_time_allower import ManagerTimezone

def viewProfileSettings(page: ft.Page, params: flet_route.Params, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500

    def returnHome():
        page.window_width = 400
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
            # ft.Column(
            #     controls=[
            #         ft.Row(controls=[
            #             ft.Text("Time to wait after this profile is done (minutes)")
            #         ]),
            #         ft.Row(controls=[
            #         ft.TextField(label="Minimum",
            #                      value=
            #                      self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
            #                          "gather_gem_duration1"],
            #                      width=80,
            #                      content_padding=ft.padding.all(10),
            #                      on_change=lambda e: self.submit(e, "gather_gem_duration1", int)
            #                      ),
            #         ft.Text("~"),
            #         ft.TextField(label="Maximum",
            #                      value=
            #                      self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
            #                          "gather_gem_duration2"],
            #                      width=90,
            #                      content_padding=ft.padding.all(10),
            #                      on_change=lambda e: self.submit(e, "gather_gem_duration2", int)),
            #         ]
            #         )
            #     ]
            # ),
            # ft.Divider(),
            ManagerTimezone(params.instance_index, params.profile_index)
        ]
    )