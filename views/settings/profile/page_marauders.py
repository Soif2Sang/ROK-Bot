import flet as ft

from views.settings.profile.rows.Flet_row_presets import FletRowPresets
from views.settings.page_base import BasePage


class PageMarauders(BasePage):
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
                        "Pre-configure red-lineups with commanders with the same march speed!\n",
                        style=ft.TextStyle(size=15, color="red"),
                    )
                ]
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "I also recommend having it running up to maximum",
                        style=ft.TextStyle(size=15),
                    ),
                    ft.TextSpan(
                        " 3-4 hours ",
                        style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "with re-do tasks enabled so the marches can come back to the city and heal.",
                        style=ft.TextStyle(size=15)
                    )
                ]
            ),
            ft.Divider(),

            ft.Container(content=ft.ResponsiveRow(controls=[
                ft.Column(controls=[ft.TextField(label="Your kingdom :",
                                                 value=
                                                 self.data[str(self.instance_index)]['schedules'][
                                                     str(self.profile_index)][
                                                     "kingdom"],
                                                 content_padding=ft.padding.all(10),
                                                 on_change=lambda e: self.submit(e, "kingdom", str),
                                                 )], col=4),
                ft.Column(controls=[ft.TextField(label="Area location X coordinates :",
                                                 value=
                                                 self.data[str(self.instance_index)]['schedules'][
                                                     str(self.profile_index)][
                                                     "city_x"],
                                                 content_padding=ft.padding.all(10),
                                                 on_change=lambda e: self.submit(e, "city_x", int),

                                                 )], col=4),
                ft.Column(controls=[ft.TextField(label="Area location Y coordinates :",
                                                 value=
                                                 self.data[str(self.instance_index)]['schedules'][
                                                     str(self.profile_index)][
                                                     "city_y"],
                                                 content_padding=ft.padding.all(10),
                                                 on_change=lambda e: self.submit(e, "city_y", int),
                                                 )], col=4)
            ], vertical_alignment=ft.CrossAxisAlignment.CENTER
            ), margin=ft.margin.only(bottom=10))
            ,
            ft.ResponsiveRow(
                controls=[
                    ft.Column(controls=[ft.TextField(label="Minimum Killing Duration (mins)",
                                                     value=self.data[str(self.instance_index)]['schedules'][
                                                         str(self.profile_index)][
                                                         "kill_marauders_duration"][0],
                                                     content_padding=ft.padding.all(10),
                                                     on_change=lambda e: self.submit_marauders(e, 0)
                                                     )], col=6),
                    ft.Column(controls=[ft.TextField(label="Maximum Killing Duration (mins)",
                                                     value=self.data[str(self.instance_index)]['schedules'][
                                                         str(self.profile_index)][
                                                         "kill_marauders_duration"][1],
                                                     content_padding=ft.padding.all(10),
                                                     on_change=lambda e: self.submit_marauders(e, 1)
                                                     )], col=6),
                ]
            ),

            ft.Divider(),
            ft.Text(value="Peacekeeper presets"),
            ft.Column(
                controls=[FletRowPresets(self.instance_index, self.profile_index, str(preset_index)) for preset_index in
                          range(1, 8)],
                wrap=True,
                spacing=10,
                run_spacing=10,
                height=150
            )
        )
        self.profile.initial_page.update()

    def submit_marauders(self, e, index):
        self.data = self.FileSingleton.get_data()
        self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["kill_marauders_duration"][
            index] = e.control.value if e.control.value is not None or e.control.value != "" else 0
        self.FileSingleton.write_data(self.data)