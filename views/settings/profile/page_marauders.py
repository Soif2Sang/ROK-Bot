import flet as ft
from schemas.emulator_schemas import TaskMaraudersSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_presets import FletRowPresets


class PageMarauders(BasePage):
    def __init__(self, profile):
        super().__init__(profile)
        self.context: TaskMaraudersSchema = self.tasks.marauders

        self.set_area_location_button = ft.OutlinedButton(
            text=translate("Set area location"),
            on_click=lambda _: self.initial_page.go(f"/set-center/marauders/{self.instance_index}/{self.profile_index}"),
            # disabled=self.context.search_method != "map",
        )

        self.add_control(
            GenerateCard(
                level=translate("tips"),
                margin=ft.margin.only(bottom=20),
                subtitle=translate(
                    "Pre-configure your red lineups with commanders who have the same march speed.\nIf you intend to use this feature extensively, I recommend running it for 3-4 hours and enabling the option to redo tasks. This will allow your troops to return to the city for healing."
                ),
            ),
            ft.OutlinedButton(
                text=translate("Set area location"),
                on_click=lambda _: self.initial_page.go(f"/gather-gems/{self.instance_index}/{self.profile_index}"),
            ),
            ft.ResponsiveRow(
                controls=[
                    ft.Column(
                        controls=[
                            ft.TextField(
                                label=translate("Minimum Killing Duration (mins)"),
                                value=str(self.context.duration.min),
                                on_change=self.submit_with_context,
                                data={"path": "duration.min", "type": int},
                                content_padding=ft.padding.all(10),
                                input_filter=ft.NumbersOnlyInputFilter(),
                            )
                        ],
                        col=6,
                    ),
                    ft.Column(
                        controls=[
                            ft.TextField(
                                label=translate("Maximum Killing Duration (mins)"),
                                value=str(self.context.duration.max),
                                on_change=self.submit_with_context,
                                data={"path": "duration.max", "type": int},
                                content_padding=ft.padding.all(10),
                                input_filter=ft.NumbersOnlyInputFilter(),
                            )
                        ],
                        col=6,
                    ),
                ]
            ),
            ft.Divider(),
            ft.Text(value=translate("Peacekeeper presets")),
            ft.Column(
                controls=[
                    FletRowPresets(preset_index, self.context)
                    for preset_index in ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                height=150,
            ),
        )
