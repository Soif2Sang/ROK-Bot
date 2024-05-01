import flet as ft
from schemas.emulator_schemas import TaskAllianceFortSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageRally(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskAllianceFortSchema = self.tasks.alliance_fort

        self.add_control(
            GenerateCard(
                level=translate("warning"),
                title=translate("*REQUIREMENT*"),
                subtitle=translate("Pre-configure the first red slot from the commanders presets with a rally leader!"),
            ),
            ft.Text("Search Methods", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.OutlinedButton(
                text=translate("Set area location"),
                on_click=lambda _: self.initial_page.go(f"/set-center/alliance_fort/{self.instance_index}/{self.profile_index}"),
                # disabled=self.context.search_method != "map",
            ),
            ft.TextField(
                label=translate("Scanning radius (km) :"),
                value=str(self.context.searching_radius),
                content_padding=ft.padding.all(10),
                on_change=self.submit_with_context,
                input_filter=ft.NumbersOnlyInputFilter(),
                data={"path": "searching_radius", "type": int},
            ),
            ft.Divider(),
            ft.Switch(
                label=translate("Look for Marauders forts (only pre-kvk)"),
                value=self.context.marauders_mode,
                on_change=self.submit_with_context,
                data={"path": "marauders_mode", "type": bool},
            ),
            ft.Switch(
                label=translate("Don't wait for the rally leader to come back."),
                value=self.context.skip_leader_back,
                on_change=self.submit_with_context,
                data={"path": "skip_leader_back", "type": bool},
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(value=translate(f"Mobilisation time (minutes):")),
                            alignment=ft.alignment.center_right,
                        ),
                        ft.Dropdown(
                            width=140,
                            height=50,
                            content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                            label=translate("Minutes"),
                            options=[
                                ft.dropdown.Option("5"),
                                ft.dropdown.Option("10"),
                                ft.dropdown.Option("30"),
                            ],
                            value=str(self.context.mobilisation_time),
                            on_change=self.submit_with_context,
                            data={"path": "mobilisation_time", "type": int},
                        ),
                    ],
                ),
                margin=ft.margin.only(left=5),
            ),
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(value=translate("Rally Type :")),
                            alignment=ft.alignment.center_right,
                        ),
                        ft.Dropdown(
                            width=140,
                            height=50,
                            content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                            label=translate("Type"),
                            options=[
                                ft.dropdown.Option("cav"),
                                ft.dropdown.Option("inf"),
                                ft.dropdown.Option("archers"),
                            ],
                            value=self.context.rally_type,
                            on_change=self.submit_with_context,
                            data={"path": "rally_type", "type": str},
                        ),
                    ]
                ),
                margin=ft.margin.only(left=5),
            ),
        )
