import flet as ft

from schemas.emulator_schemas import TaskGatherRssSchema
from utils.flet_translations import translate
from utils.functions import FileSingleton, rsetattr
from utils.singletons import ss


class FletRowRss(ft.ResponsiveRow):
    def __init__(self, key, instance_index, profile_index, context):
        super().__init__()
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.context: TaskGatherRssSchema = context

        self.node_level_dropdown = ft.Dropdown(
            content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
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
            disabled=self.context.search_method == "spiral",
            data={"path": f"{key.lower()}_node.level", "type": int},
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
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
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

    def submit(self, e, keyword, method):
        self.data = self.FileSingleton.get_data()
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1", "API_KEY"]:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            self.FileSingleton.write_data(self.data)
            return
        if keyword not in ["sleep_multiplicator", "defeat_barbarians"]:
            self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][keyword] = float(
                e.control.value.replace("x", "").replace("level ", "")
            )
        self.FileSingleton.write_data(self.data)

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
