import flet as ft

from settings.profile.rows.Flet_row_presets import FletRowPresets
from settings.page_base import BasePage


class PageBarbs(BasePage):
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
                        "Pre-configure red-lineups with PeaceKeeper commanders !\n",
                        style=ft.TextStyle(size=15, color="red"),
                    ),
                    ft.TextSpan(
                        "Avoid AOE ",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "if you're using this function on low accounts\n",
                        style=ft.TextStyle(size=15, color="red"),
                    ),
                    ft.TextSpan(
                        "The bot is",
                        style=ft.TextStyle(size=15, color="red"),
                    ),
                    ft.TextSpan(
                        " unable ",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),

                    ft.TextSpan(
                        "to see the troops health",
                        style=ft.TextStyle(size=15, color="red"),
                    ),
                ]
            ),
            ft.Text("You should only use this with natural AP bar.", color="orange", size=15),
            ft.Divider(),
            ft.Row(
                controls=[
                    ft.Text(value="Barbarian Level"),
                    ft.Dropdown(
                        width=70,
                        height=50,
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                        options=[
                            ft.dropdown.Option(str(i)) for i in range(1, 56)
                        ],
                        on_change=lambda e: self.submit(e, "barbarians_level", str),
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                            "barbarians_level"]
                    )
                ]
                , width=300
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