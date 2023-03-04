import flet as ft
import json

from Flet_page import FletPage


def page_gems(self):
    with open('user_settings.json') as config_file:
        self.data = json.load(config_file)
    self.clean()
    self.tabs.expand = True
    self.content = ft.ListView(height=500, expand=0, padding=1, )
    self.controls.append(
        ft.Row(
            controls=[
                ft.IconButton(
                    icon=ft.icons.ARROW_BACK,
                    on_click=lambda _: self.reset()
                ),
                ft.Text("Settings", size=20),
            ],
        )
    )

    self.controls.extend([
        ft.Text(value="*REQUIREMENT*\n/!\ Pre-configure yellow-lineups with farmers !", size=15, color="red"),
        ft.TextField(label="Your kingdom :",
                     value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["kingdom"],
                     width=300,
                     border=ft.InputBorder.UNDERLINE,
                     filled=True,
                     content_padding=ft.padding.all(10),
                     on_change=lambda e: self.submit(e, "kingdom", str)),
        ft.TextField(label="Area location X coordinates :",
                     value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_x"],
                     width=300, border=ft.InputBorder.UNDERLINE,
                     filled=True,
                     content_padding=ft.padding.all(10),
                     on_change=lambda e: self.submit(e, "city_x", int)
                     ),
        ft.TextField(label="Area location Y coordinates :",
                     value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_y"],
                     width=300, border=ft.InputBorder.UNDERLINE,
                     filled=True,
                     content_padding=ft.padding.all(10),
                     on_change=lambda e: self.submit(e, "city_y", int),
                     ),
        ft.TextField(label="Scanning radius (km) :",
                     value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["radius"],
                     width=300, border=ft.InputBorder.UNDERLINE,
                     filled=True,
                     content_padding=ft.padding.all(10),
                     on_change=lambda e: self.submit(e, "radius", int)),
        ft.Row(
            controls=[
                ft.Text("Mining duration (mins)"),
                ft.TextField(label="Minimum",
                             value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                 "gather_gem_duration1"],
                             width=80, border=ft.InputBorder.UNDERLINE,
                             filled=True,
                             content_padding=ft.padding.all(10),
                             on_change=lambda e: self.submit(e, "gather_gem_duration1", int)
                             ),
                ft.Text("~"),
                ft.TextField(label="Maximum",
                             value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                 "gather_gem_duration2"],
                             width=90, border=ft.InputBorder.UNDERLINE,
                             filled=True,
                             content_padding=ft.padding.all(10),
                             on_change=lambda e: self.submit(e, "gather_gem_duration2", int)),
            ]
        ),
        ft.Row(
            controls=[
                ft.Text("Available troop scan frequency"),
                ft.TextField(label="Minimum",
                             value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                 "gem_check1"],
                             width=80, border=ft.InputBorder.UNDERLINE,
                             filled=True,
                             content_padding=ft.padding.all(10),
                             on_change=lambda e: self.submit(e, "gem_check1", int)),
                ft.Text("~"),
                ft.TextField(label="Maximum",
                             value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                 "gem_check2"],
                             width=90, border=ft.InputBorder.UNDERLINE,
                             filled=True,
                             content_padding=ft.padding.all(10),
                             on_change=lambda e: self.submit(e, "gem_check2", int)),
            ]
        ),
        ft.Switch(
            label="Restart the game randomly",
            active_track_color=self.color_choice,
            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                "restart_game"] else False,
            on_change=lambda _: self.reverse_keyword("restart_game")
        ),
        ft.Switch(
            label="Experimental feature",
            active_track_color=self.color_choice,
            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                "gem_experimental"] else False,
            on_change=lambda _: self.reverse_keyword("gem_experimental")
        )
    ]

    )
    # print(self.page)
    self.page.update()


class FletGem(FletPage):
    def __init__(self,tab, **kwargs):
        super().__init__(tab,**kwargs)

    def show(self):
        super().show()
        self.controls.extend([
            ft.Text(value="*REQUIREMENT*\n/!\ Pre-configure yellow-lineups with farmers !", size=15, color="red"),
            ft.TextField(label="Your kingdom :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["kingdom"],
                         width=300,
                         border=ft.InputBorder.UNDERLINE,
                         filled=True,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "kingdom", str)),
            ft.TextField(label="Area location X coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_x"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "city_x", int)
                         ),
            ft.TextField(label="Area location Y coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_y"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "city_y", int),
                         ),
            ft.TextField(label="Scanning radius (km) :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["radius"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,
                         content_padding=ft.padding.all(10),
                         on_change=lambda e: self.submit(e, "radius", int)),
            ft.Row(
                controls=[
                    ft.Text("Mining duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration1"],
                                 width=80, border=ft.InputBorder.UNDERLINE,
                                 filled=True,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gather_gem_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration2"],
                                 width=90, border=ft.InputBorder.UNDERLINE,
                                 filled=True,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gather_gem_duration2", int)),
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text("Available troop scan frequency"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check1"],
                                 width=80, border=ft.InputBorder.UNDERLINE,
                                 filled=True,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gem_check1", int)),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check2"],
                                 width=90, border=ft.InputBorder.UNDERLINE,
                                 filled=True,
                                 content_padding=ft.padding.all(10),
                                 on_change=lambda e: self.submit(e, "gem_check2", int)),
                ]
            ),
            ft.Switch(
                label="Restart the game randomly",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "restart_game"] else False,
                on_change=lambda _: self.reverse_keyword("restart_game")
            ),
            ft.Switch(
                label="Experimental feature",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gem_experimental"] else False,
                on_change=lambda _: self.reverse_keyword("gem_experimental")
            )
        ]
        )
