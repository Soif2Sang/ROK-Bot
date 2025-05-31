import flet as ft

from src.utils.Components.card import GenerateCard
from src.utils.flet_translations import translate
from src.utils.singletons import ss
from src.views.settings.page_base import BasePage


class PageUpgradeCity(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context = self.tasks.upgrade_city

        self.add_control(
            GenerateCard(
                level=translate("warning"),
                title=translate("*REQUIREMENT*"),
                subtitle=translate(
                    "If you use the normal way to upgrade the city, you have to configure the city hall position!",
                ),
            ),
            ft.Switch(
                label=translate(
                    "Use normal way to upgrade the city \n(if unchecked the bot is unable to upgrade the wall but \nit is a safer way to upgrade the city)"
                ),
                width=300,
                on_change=self.submit_upgrade_mode,
                value=self.context.method == "normal",
            ),
        )

        self.add_control(
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set City Hall Position"),
                on_click=lambda _: ss.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            )
        )

    def submit_upgrade_mode(self, e):
        data = e.control.value

        self.context.method = data

        ss.write_emulator_settings(ss.emulator_settings)
