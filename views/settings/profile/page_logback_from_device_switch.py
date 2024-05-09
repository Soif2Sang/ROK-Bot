import flet as ft
from utils.schemas.emulator_schemas import LogBackFromDeviceSwitchSchema, LogBackFromErrorSchema

from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageLogbackFromDeviceSwitch(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: LogBackFromDeviceSwitchSchema = self.context.log_back_from_device_switch

        self.add_control(
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text=translate("Time to wait before the bot log back from device switch (minutes):"),
                        style=ft.TextStyle(size=15),
                    )
                ],
            ),
            ft.Container(height=10),
            ft.Row(
                controls=[
                    ft.TextField(
                        label=translate("Minimum"),
                        value=str(self.context.duration.min),
                        on_change=self.submit_with_context,
                        data={"path": "duration.min", "type": int},
                        content_padding=ft.padding.all(10),
                        width=80,
                        input_filter=ft.NumbersOnlyInputFilter(),
                    ),
                    ft.Text("~"),
                    ft.TextField(
                        label=translate("Maximum"),
                        value=str(self.context.duration.max),
                        on_change=self.submit_with_context,
                        data={"path": "duration.max", "type": int},
                        content_padding=ft.padding.all(10),
                        width=90,
                        input_filter=ft.NumbersOnlyInputFilter(),
                    ),
                ]
            ),
        )
