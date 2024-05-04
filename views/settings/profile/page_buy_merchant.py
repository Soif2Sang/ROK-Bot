import flet as ft
from utils.schemas.emulator_schemas import TaskBuyMysteriousMerchantSchema

from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageBuyMerchant(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskBuyMysteriousMerchantSchema = self.tasks.buy_mysterious_merchant

        self.add_control(
            ft.Switch(
                label=translate("Skip second and fourth row"),
                value=self.context.skip_second_row,
                on_change=self.submit_with_context,
                data={"path": "skip_second_row", "type": bool},
                width=300,
            )
        )
