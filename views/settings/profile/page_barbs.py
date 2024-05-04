import flet as ft
from utils.schemas.emulator_schemas import TaskKillBarbarianSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_presets import FletRowPresets


class PageBarbs(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskKillBarbarianSchema = self.tasks.kill_barbarian

        self.add_control(
            GenerateCard(
                level="warning",
                margin=ft.margin.only(bottom=10),
                title=translate("*WARNING*"),
                subtitle=translate(
                    "Pre-configure red-lineups with PeaceKeeper commanders!\nThe bot is unable to see the troops health.\nYou should only use this with natural AP bar."
                ),
            ),
            ft.Row(
                controls=[
                    ft.Text(value=translate("Barbarian Level")),
                    ft.Dropdown(
                        width=70,
                        height=50,
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                        options=[ft.dropdown.Option(str(i)) for i in range(1, 56)],
                        value=str(self.context.target_level),
                        on_change=self.submit_with_context,
                        data={"path": "target_level", "type": int},
                    ),
                ],
                width=300,
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
