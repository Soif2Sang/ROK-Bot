import flet as ft
from utils.schemas.emulator_schemas import TaskTroopHealingSchema

from utils.flet_translations import translate
from views.settings.page_base import BasePage
from utils.singletons import ss


class PageHeal(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskTroopHealingSchema = self.tasks.troop_healing
        self.add_control(
            ft.TextField(
                label=translate("Heal batch :"),
                value=str(self.context.healing_batch_size),
                on_change=self.submit_with_context,
                data={"path": f"healing_batch_size", "type": int},
                content_padding=ft.padding.all(10),
                width=300,
            ),
            ft.Divider(),
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text=translate("Set Hospital position"),
                on_click=lambda _: ss.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}"),
            ),
        )
