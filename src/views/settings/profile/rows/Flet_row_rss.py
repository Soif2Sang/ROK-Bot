import flet as ft
from src.utils.schemas.emulator_schemas import TaskGatherRssSchema

from src.utils.flet_translations import translate
from src.utils.functions import rsetattr
from src.utils.singletons import ss


class FletRowRss(ft.ResponsiveRow):
    def __init__(self, key, instance_index, profile_index, context):
        super().__init__()
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.context: TaskGatherRssSchema = context

        self.node_level_dropdown = ft.Dropdown(
            content_padding=ft.padding.all(1),  # modify to your likings
            label=translate("Node Level"),
            options=[
                ft.dropdown.Option("1"),
                ft.dropdown.Option("2"),
                ft.dropdown.Option("3"),
                ft.dropdown.Option("4"),
                ft.dropdown.Option("5"),
                ft.dropdown.Option("6"),
                ft.dropdown.Option("7"),
                ft.dropdown.Option("8"),
                ft.dropdown.Option("9"),
            ],
            # value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][f"{key}_level"],
            value=getattr(self.context, f"{key.lower()}_node").level,
            on_change=self.submit_with_context,
            disabled=self.context.search_method == "zoom",
            data={"path": f"{key.lower()}_node.level", "type": int},
            width=100
        )

        self.controls = [
            ft.Column(
                controls=[
                    ft.Container(
                        ft.Text(translate(f"{key} choice :")),
                        alignment=ft.alignment.center_right,
                    )
                ],
                col=4,
                height=50,
            ),
            ft.Column(
                controls=[
                    ft.Dropdown(
                        content_padding=ft.padding.all(1),  # modify to your likings
                        label=translate("Node Type"),
                        options=[
                            ft.dropdown.Option("food"),
                            ft.dropdown.Option("wood"),
                            ft.dropdown.Option("stone"),
                            ft.dropdown.Option("gold"),
                            ft.dropdown.Option("random"),
                            ft.dropdown.Option("nothing"),
                        ],
                        value=getattr(self.context, f"{key.lower()}_node").type,
                        on_change=self.submit_with_context,
                        data={"path": f"{key.lower()}_node.type", "type": str},
                    )
                ],
                col=4,
                height=50,
            ),
            ft.Column(
                controls=[self.node_level_dropdown],
                col=3,
                height=50,
            ),
        ]

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
