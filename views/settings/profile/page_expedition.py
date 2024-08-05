import flet as ft

from Components.card import SimpleCard
from utils.schemas.emulator_schemas import TaskClaimDailyExpeditionRewardsSchema

from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageExpedition(BasePage):
    def __init__(self, profile):
        super().__init__(profile)
        self.context: TaskClaimDailyExpeditionRewardsSchema = self.tasks.claim_daily_expedition_rewards

        self.add_control(
            SimpleCard(translate("Enable/Disable items you want to buy.")),
        )
        self.add_control(
            ft.Switch(
                label=translate("Buy ethel heads"),
                value=self.context.enable_buy_heads,
                on_change=self.submit_with_context,
                data={"path": f"enable_buy_heads", "type": bool},
                width=300,
            ),
            ft.Switch(
                label=translate("Buy items shop"),
                value=self.context.enable_buy_items,
                on_change=self.submit_with_context,
                data={"path": f"enable_buy_items", "type": bool},
                width=300,
            ),
        )
