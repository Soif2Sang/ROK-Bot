import flet as ft

from settings.page_base import BasePage


class PageHeal(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.TextField(label="Heal batch :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_count"],
                         width=300,
                         on_change=lambda e: self.submit(e, "healing_count", int),
                         ),
            ft.Divider(),
            ft.OutlinedButton(icon=ft.icons.GPS_FIXED_SHARP, text="Set Hospital position",
                              on_click=lambda _: self.initial_page.go(
                                  f"/citylayout/{self.instance_index}/{self.profile_index}")),

        )

        self.profile.initial_page.update()