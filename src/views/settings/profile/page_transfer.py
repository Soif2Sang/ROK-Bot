import flet as ft

from src.utils.Components.card import GenerateCard
from src.utils.flet_translations import translate
from src.views.settings.page_base import BasePage
from src.views.settings.profile.cols.Flet_col_transfer import FletColumnRss
from src.utils.singletons import ss


class PageTransfer(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context = self.tasks.resources_transfer

        self.add_control(
            GenerateCard(
                level=translate("warning"),
                subtitle=translate("In order to use this feature, you have to purchase a API key on 2captcha.com (this is very cheap!)"),
            ),
            self.create_normal_switch(
                "fast_transfer", "Enable faster rss transfer may be riskier", data={"path": "fast_transfer", "type": bool}
            ),
            ft.Container(height=10),
            FletColumnRss(self.context),
            ft.Divider(),
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set City Position"),
                on_click=lambda _: ss.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            ),
        )
