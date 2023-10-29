import flet as ft

from views.settings.page_base import BasePage
from utils.flet_utils import GenerateCard


class PageCharacter(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            GenerateCard("notice", subtitle="Keep in mind that it well iterate on all of your favorite characters, it goes from top to bottom"),
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "leave_game_switch_character"] else False,
                on_change=lambda _: self.reverse_keyword("leave_game_switch_character")
            ),
            # ft.Divider(),
            # ft.Text("Character Whitelist"),
        )

        # self.row_whitelist = ft.ResponsiveRow()
        # [self.row_whitelist.controls.append(ft.Checkbox(label=f"Profile {i}", col=4)) for i in range(9)]
        # self.add(self.row_whitelist)
        self.profile.initial_page.update()

    def reverse_keyword(self, keyword: str):
        super().reverse_keyword(keyword)