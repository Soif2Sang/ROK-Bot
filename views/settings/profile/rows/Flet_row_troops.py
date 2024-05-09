import flet as ft
from utils.schemas.emulator_schemas import TaskTroopTraining

from utils.flet_translations import translate
from utils.functions import FileSingleton, rgetattr, rsetattr
from utils.singletons import ss


class FletRowTraining(ft.ResponsiveRow):
    def __init__(self, key, context: TaskTroopTraining):
        super().__init__()
        self.content_padding = ft.padding.all(10)
        self.context = context
        # self.instance_index = instance_index
        # self.profile_index = profile_index
        #
        # self.emulator_settings = ss.open_emulator_settings()
        # self.context = self.emulator_settings.emulators[str(self.instance_index)].schedules[str(self.profile_index)].tasks.troop_training

        self.controls = [
            ft.Switch(
                label=translate(f"Train {key}"),
                value=rgetattr(self.context, f"{key}.enabled"),
                on_change=self.submit_with_context,
                data={"path": f"{key}.enabled", "type": bool},
                col=6,
            ),
            ft.Dropdown(
                width=140,
                label="Tier",
                options=[
                    ft.dropdown.Option("t1"),
                    ft.dropdown.Option("t2"),
                    ft.dropdown.Option("t3"),
                    ft.dropdown.Option("t4"),
                    ft.dropdown.Option("t5"),
                    ft.dropdown.Option("highest"),
                ],
                value=rgetattr(self.context, f"{key}.tier"),
                on_change=self.submit_with_context,
                data={"path": f"{key}.tier", "type": str},
                height=40,
                content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                col=6,
            ),
        ]

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
