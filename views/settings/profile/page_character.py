import flet as ft
from schemas.emulator_schemas import SwitchCharacterSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageCharacter(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: SwitchCharacterSchema = self.context.switch_character
        self.add_control(
            GenerateCard(
                level="notice",
                subtitle=translate("Keep in mind that it will iterate on all of your favorite characters, it goes from top to bottom"),
            ),
            ft.Switch(
                label=translate("Restart the game after switching\nto a new character (prevent freeze)"),
                value=self.context.restart_during_game_load,
                on_change=self.submit_with_context,
                data={"path": "restart_during_game_load", "type": bool},
            ),
        )

        # self.row_whitelist = ft.ResponsiveRow()
        # [self.row_whitelist.controls.append(ft.Checkbox(label=f"Profile {i}", col=4)) for i in range(9)]
        # self.add_control(self.row_whitelist)
