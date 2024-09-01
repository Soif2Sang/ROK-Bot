import flet as ft

from utils.Components.card import GenerateCard, SimpleCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_troops import FletRowTraining
from utils.singletons import ss


class PageTraining(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        keys = [
            "infantry",
            "cavalry",
            "archery",
            "siege",
        ]

        self.context = self.tasks.troop_training

        self.add_control(
            SimpleCard(translate("Enable/Disable and choose the tier of the troops you want to train.")),
        )

        for key in keys:
            self.add_control(
                FletRowTraining(
                    key=key,
                    context=self.context,
                    # instance_index=self.instance_index,
                    # profile_index=self.profile_index,
                )
            )

        self.add_control(
            ft.Divider()
        )

        self.add_control(
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set Training camps position"),
                on_click=lambda _: ss.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            )
        )
