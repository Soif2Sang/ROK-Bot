import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from src.utils.flet_translations import translate
from src.utils.singletons import ss
from src.views.settings.page_base import BasePage


class PageProfiles(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add_control(
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate("Profile n°1"),
                        active_track_color="#3b8ed0",
                        value=ss.emulator_settings.emulators[self.instance_index].schedules["1"].enabled,
                        on_change=self.submit_with_context,
                        data="1",
                    ),
                    ft.OutlinedButton(
                        text=translate("Settings"),
                        icon_color="#3b8ed0",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: ss.page.go(f"/profile/{self.instance_index}/1/settings"),
                        style=ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            }
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate("Profile n°2"),
                        active_track_color="#ba4543",
                        value=ss.emulator_settings.emulators[self.instance_index].schedules["2"].enabled,
                        on_change=self.submit_with_context,
                        data="2",
                    ),
                    ft.OutlinedButton(
                        text=translate("Settings"),
                        icon_color="#ba4543",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: ss.page.go(f"/profile/{self.instance_index}/2/settings"),
                        style=ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            }
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate("Profile n°3"),
                        active_track_color="#dec433",
                        value=ss.emulator_settings.emulators[self.instance_index].schedules["3"].enabled,
                        on_change=self.submit_with_context,
                        data="3",
                    ),
                    ft.OutlinedButton(
                        text=translate("Settings"),
                        icon_color="#dec433",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: ss.page.go(f"/profile/{self.instance_index}/3/settings"),
                        style=ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            }
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
        )
        ss.page.update()

    def submit_with_context(self, e):
        ss.emulator_settings.emulators[self.instance_index].schedules[e.control.data].enabled = e.control.value
        ss.write_emulator_settings(ss.emulator_settings)
