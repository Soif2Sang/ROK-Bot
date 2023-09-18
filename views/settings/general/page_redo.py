import flet as ft

from views.settings.page_base import BasePage


class PageRedo(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "*Randomise it as much as possible*\n",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "Time to wait before the bot re-do the tasks selected (minutes):\n",
                        style=ft.TextStyle(size=15, color="red"),
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop2", int)
                                 )
                ]
            ),
            ft.Switch(label="Close the game after all the tasks are done",
                      value=self.data[str(self.instance_index)]["leave_game_loop"],
                      on_change=lambda _: self.reverse_keyword('leave_game_loop'))
        )
        self.profile.initial_page.update()