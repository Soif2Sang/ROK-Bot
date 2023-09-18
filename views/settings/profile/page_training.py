import flet as ft

from views.settings.profile.rows.Flet_row_troops import FletRowTraining
from views.settings.page_base import BasePage


class PageTraining(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        keys = [
            "infantry",
            "cavalry",
            "archery",
            "siege",
        ]

        for key in keys:
            self.add(
                FletRowTraining(key=key, instance_index=self.instance_index, profile_index=self.profile_index))

        self.add(
            ft.OutlinedButton(icon=ft.icons.GPS_FIXED_SHARP, text="Set Training camps position",
                              on_click=lambda _: self.initial_page.go(
                                  f"/citylayout/{self.instance_index}/{self.profile_index}")))

        self.profile.initial_page.update()