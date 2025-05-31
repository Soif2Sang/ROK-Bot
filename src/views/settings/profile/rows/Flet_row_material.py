import flet as ft
from src.utils.schemas.emulator_schemas import TaskProduceMaterialsSchema

from src.utils.flet_translations import translate
from src.utils.functions import rgetattr, rsetattr
from src.utils.singletons import ss, FileSingleton


class FletRowMaterial(ft.Row):
    def __init__(self, key, context: TaskProduceMaterialsSchema):
        super().__init__()
        self.context = context
        self.controls = [
            ft.Container(
                width=120,
                content=ft.Text(translate(f"{key.split('_')[0].capitalize()} choice :")),
                alignment=ft.alignment.center_right,
            ),
            ft.Dropdown(
                width=140,
                height=50,
                content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                label="Type",
                options=[
                    ft.dropdown.Option("leather"),
                    ft.dropdown.Option("stone"),
                    ft.dropdown.Option("ebony"),
                    ft.dropdown.Option("bones"),
                ],
                value=rgetattr(self.context, f"{key}.type"),
                on_change=self.submit_with_context,
                data={"path": f"{key}.type", "type": str},
            ),
        ]

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
