import flet as ft
from settings.page_base import BasePage


class PageGem(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "*REQUIREMENT* ",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "Pre-configure yellow-lineups with gathering gem commanders !\n",
                        style=ft.TextStyle(size=15, color="red"),
                    )
                ]
            ),
            ft.Divider(),
            ft.TextField(label="Your kingdom :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["kingdom"],
                         width=300,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "kingdom", str)),
            ft.Divider(),
            ft.TextField(label="Area location X coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_x"],
                         width=300,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "city_x", int)
                         ),
            ft.Divider(),
            ft.TextField(label="Area location Y coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_y"],
                         width=300,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "city_y", int),
                         ),
            ft.Divider(),
            ft.TextField(label="Scanning radius (km) :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["radius"],
                         width=300,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "radius", int)),

            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text("Mining duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration1"],
                                 width=80,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gather_gem_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration2"],
                                 width=90,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gather_gem_duration2", int)),
                ]
            ),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text("Available troop scan\nfrequency (seconds)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check1"],
                                 width=80,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gem_check1", int)),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check2"],
                                 width=90,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gem_check2", int)),
                ]
            ),
            ft.Switch(
                label="Spiral path method, \nonly if you gather near your city.",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gather_gem_spiral_method"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_spiral_method")
            ),
            ft.Switch(
                label="Recenter the view based on city location\n(turn off if the cords are NOT your city's cords)",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "recenter_feature"] else False,
                on_change=lambda _: self.reverse_keyword("recenter_feature")
            ),
            ft.Switch(
                label="Compare march speed (Increase gem gathering\nbut increase number of actions",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gather_gem_compare_march_duration"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_compare_march_duration")
            ),
            ft.Switch(
                label="Detect free marches without clicking on the node",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gather_gem_swipe_check"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_swipe_check")
            ),
            ft.Switch(
                label="Restart the game randomly",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "restart_game"] else False,
                on_change=lambda _: self.reverse_keyword("restart_game")
            ),
            ft.Switch(
                label="Experimental feature",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gem_experimental"] else False,
                on_change=lambda _: self.reverse_keyword("gem_experimental")
            ),

        )

        self.profile.initial_page.update()