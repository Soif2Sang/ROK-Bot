import flet as ft

from views.settings.page_base import BasePage


class PageFog(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Row(
                controls=[
                    ft.Text("Scout duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "scout_duration1", int),content_padding=ft.padding.all(10)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "scout_duration2", int),content_padding=ft.padding.all(10)),
                ]
            ),
            ft.Divider(),
            ft.OutlinedButton(icon=ft.icons.GPS_FIXED_SHARP, text="Set Scout camp position",
                              on_click=lambda _: self.initial_page.go(
                                  f"/citylayout/{self.instance_index}/{self.profile_index}")),

        )

        self.profile.initial_page.update()