import flet as ft
from schemas.emulator_schemas import TaskKillBarbarianSchema, TaskMaraudersSchema

from utils.functions import FileSingleton, rgetattr, rsetattr
from utils.singletons import ss


class FletRowPresets(ft.Row):
    def __init__(self, key, context: TaskMaraudersSchema | TaskKillBarbarianSchema):
        super().__init__()
        self.content_padding = ft.padding.all(10)
        self.context = context

        self.controls = [
            ft.Checkbox(
                label=f"{key.capitalize()} preset",
                value=rgetattr(self.context, f"presets_selection.{key}"),
                on_change=self.submit_with_context,
                data={"path": f"presets_selection.{key}", "type": bool},
            )
        ]

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
