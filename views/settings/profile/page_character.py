import flet as ft

from settings.page_base import BasePage


class PageCharacter(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "leave_game_switch_character"] else False,
                on_change=lambda _: self.reverse_keyword("leave_game_switch_character")
            ))

        self.profile.initial_page.update()

    def reverse_keyword(self, keyword: str):
        print(self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "leave_game_switch_character"])
        super().reverse_keyword(keyword)