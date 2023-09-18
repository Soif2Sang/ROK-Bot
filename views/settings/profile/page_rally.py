import flet as ft

from views.settings.page_base import BasePage


class PageRally(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "*REQUIREMENT*\n",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "Pre-configure first slot of red line-up with rally Leader !",
                        style=ft.TextStyle(size=15, color="red"),
                    )
                ]
            ),

            ft.Switch(
                label="Look for Marauders forts",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "mauraudeurs_forts"] else False,
                on_change=lambda _: self.reverse_keyword("mauraudeurs_forts")
            ),
            ft.Switch(
                label="Skip commander back",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "rally_skip_back"] else False,
                on_change=lambda _: self.reverse_keyword("rally_skip_back")
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        width=100,
                        content=ft.Text(f"Mobilisation time (minutes):"),
                        alignment=ft.alignment.center_right
                    ),

                    ft.Dropdown(
                        width=140, height=50,
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                        label="Minutes",
                        options=[
                            ft.dropdown.Option("5"),
                            ft.dropdown.Option("10"),
                            ft.dropdown.Option("30"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["rally_time"],
                        on_change=lambda e: self.submit(e, "rally_time", int)
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        width=100,
                        content=ft.Text(f"Rally type :"),
                        alignment=ft.alignment.center_right
                    ),

                    ft.Dropdown(
                        width=140, height=50,
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                        label="Type",
                        options=[
                            ft.dropdown.Option("cav"),
                            ft.dropdown.Option("inf"),
                            ft.dropdown.Option("archers"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["rally_type"],
                        on_change=lambda e: self.submit(e, "rally_type", str)
                    )
                ]
            ),
        )
        self.profile.initial_page.update()