import flet as ft
from schemas.emulator_schemas import LogBackFromErrorSchema

from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageLogbackFromError(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: LogBackFromErrorSchema = self.context.log_back_from_error

        self.add_control(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text=translate("Time to wait before the bot log back from any error (minutes):"),
                        style=ft.TextStyle(size=15),
                    )
                ]
            ),
            ft.Container(height=10),
            ft.Row(
                controls=[
                    ft.TextField(
                        label=translate("Minimum"),
                        value=str(self.context.duration.min),
                        on_change=self.submit_with_context,
                        data={"path": "duration.min", "type": int},
                        width=80,
                        content_padding=ft.padding.all(10),
                        input_filter=ft.NumbersOnlyInputFilter(),
                    ),
                    ft.Text("~"),
                    ft.TextField(
                        label=translate("Maximum"),
                        value=str(self.context.duration.max),
                        on_change=self.submit_with_context,
                        data={"path": "duration.max", "type": int},
                        width=90,
                        content_padding=ft.padding.all(10),
                        input_filter=ft.NumbersOnlyInputFilter(),
                    ),
                ]
            ),
        )
