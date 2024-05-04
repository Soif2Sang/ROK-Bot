import flet as ft
from utils.schemas.emulator_schemas import TaskExploreFogSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageFog(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskExploreFogSchema = self.tasks.explore_fog

        self.add_control(
            GenerateCard(
                level=translate("tips"),
                subtitle=translate(
                    "If you plan on having the safest configuration, do not use this functionality extensively throughout the day."
                ),
            ),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        text=translate("Scout duration (mins)"),
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
                        width=80,
                        content_padding=ft.padding.all(10),
                    ),
                    ft.Text("~"),
                    ft.TextField(
                        label=translate("Maximum"),
                        value=str(self.context.duration.max),
                        on_change=self.submit_with_context,
                        data={"path": "duration.min", "type": int},
                        width=90,
                        content_padding=ft.padding.all(10),
                    ),
                ]
            ),
            ft.Divider(),
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set Scout camp position"),
                on_click=lambda _: self.initial_page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            ),
        )
