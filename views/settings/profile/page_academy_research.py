import flet as ft

from utils.singletons import ss
from utils.Components.card import GenerateCard

from utils.flet_translations import translate
from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_troops import FletRowTraining


class PageAcademyResearch(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add_control(
            GenerateCard(
                level=translate("tips"),
                subtitle=translate("It is required to place the academy where the bot can reach it."),
            ),
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set Academy Research"),
                on_click=lambda _: ss.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            ),
        )
