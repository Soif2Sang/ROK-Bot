import flet as ft

from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageExpedition(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add_control(
            ft.Switch(
                label=translate("Buy ethel heads"),
                on_change=lambda e: self.reverse_keyword("expedition_shop_ethel"),
                value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["expedition_shop_ethel"],
                width=300,
            ),
            ft.Switch(
                label=translate("Buy items shop"),
                on_change=lambda e: self.reverse_keyword("expedition_shop_items"),
                value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["expedition_shop_items"],
                width=300,
            ),
        )

    def submit_upgrade_mode(self, e):
        self.data = self.FileSingleton.get_data()
        self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["upgrade_city_method"] = (
            "normal" if e.control.value else "safest"
        )
        self.FileSingleton.write_data(self.data)
