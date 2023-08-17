import flet as ft

from Flet_page import FletPage
from utils.Task_utils import FileSingleton

fileSingleton = FileSingleton()

class FletGem(FletPage):
    def __init__(self,tab,instance_index, profile_index, color_choice, **kwargs):
        super().__init__(tab,instance_index, profile_index, color_choice,**kwargs)

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
                label="Spiral path method, should decrease march speed.",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "recenter_feature"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_spiral_method")
            ),
            ft.Switch(
                label="Recenter the view based on city location\n(turn off if the cords are NOT your city's cords)",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "recenter_feature"] else False,
                on_change=lambda _: self.reverse_keyword("recenter_feature")
            ),
            ft.Switch(
                label="Compare march speed (Increase gem gathering but increase number of actions",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "recenter_feature"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_compare_march_duration")
            ),
            ft.Switch(
                label="Detect free marches without clicking on the node",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "recenter_feature"] else False,
                on_change=lambda _: self.reverse_keyword("gather_gem_swipe_check")
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
            ),
        ]
        )
