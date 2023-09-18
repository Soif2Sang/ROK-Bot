import flet as ft

from views.settings.page_base import BasePage


class PageLogback(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "Time to wait before the bot log  back from your connection(minutes):\n",
                        style=ft.TextStyle(size=15, color="black"),
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "log_back1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "log_back2", int)
                                 )
                ]
            ))

        self.profile.initial_page.update()
