import flet as ft

from views.settings.page_base import BasePage
from utils.flet_utils import GenerateCard


class PageRally(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            GenerateCard(level="warning", title="*REQUIREMENT*", subtitle="Pre-configure the first red slot from the commanders presets with a rally leader!"),
            ft.Switch(
                label="Look for Marauders forts (only pre-kvk)",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "mauraudeurs_forts"] else False,
                on_change=lambda _: self.reverse_keyword("mauraudeurs_forts")
            ),
            ft.Switch(
                label="Don't wait for the rally leader to come back.",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "rally_skip_back"] else False,
                on_change=lambda _: self.reverse_keyword("rally_skip_back")
            ),
            ft.Container(
                content=ft.Row(
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
                            value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                "rally_time"],
                            on_change=lambda e: self.submit(e, "rally_time", int)
                        )
                    ],
                ), margin=ft.margin.only(left=5)
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(f"Rally Type :"),
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
                            value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                "rally_type"],
                            on_change=lambda e: self.submit(e, "rally_type", str)
                        )
                    ]
                ), margin=ft.margin.only(left=5)
            )

        )
        self.profile.initial_page.update()
