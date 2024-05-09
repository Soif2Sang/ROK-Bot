import flet as ft
from utils.schemas.emulator_schemas import TaskResourcesTransferSchema

from utils.flet_translations import translate
from utils.functions import FileSingleton, rsetattr
from utils.singletons import ss


class FletColumnRss(ft.Column):
    def __init__(self, context: TaskResourcesTransferSchema):
        super().__init__()
        self.context = context

        self.controls = [
            ft.TextField(
                label=translate("Million of Food to transfer :"),
                value=str(context.food_amount),
                on_change=self.submit_with_context,
                data={"path": "food_amount", "type": int},
                content_padding=ft.padding.all(10),
                input_filter=ft.NumbersOnlyInputFilter(),
            ),
            ft.TextField(
                label=translate("Million of Wood to transfer :"),
                value=str(context.wood_amount),
                on_change=self.submit_with_context,
                data={"path": "wood_amount", "type": int},
                content_padding=ft.padding.all(10),
                input_filter=ft.NumbersOnlyInputFilter(),
            ),
            ft.TextField(
                label=translate("Million of Stone to transfer :"),
                value=str(context.stone_amount),
                on_change=self.submit_with_context,
                data={"path": "stone_amount", "type": int},
                content_padding=ft.padding.all(10),
                input_filter=ft.NumbersOnlyInputFilter(),
            ),
            ft.TextField(
                label=translate("Million of Gold to transfer :"),
                value=str(context.gold_amount),
                on_change=self.submit_with_context,
                data={"path": "gold_amount", "type": int},
                content_padding=ft.padding.all(10),
                input_filter=ft.NumbersOnlyInputFilter(),
            ),
        ]

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
