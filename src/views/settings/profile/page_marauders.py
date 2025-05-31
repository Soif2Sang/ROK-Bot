import flet as ft
from src.utils.schemas.emulator_schemas import TaskKillBarbarianSchema, TaskMaraudersSchema

from src.utils.Components.card import GenerateCard
from src.utils.flet_translations import translate
from src.views.settings.page_base import BasePage
from src.views.settings.profile.rows.Flet_row_presets import FletRowPresets
from src.utils.singletons import ss


class PageMarauders(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context: TaskMaraudersSchema = self.tasks.marauders

        self.add_control(
            GenerateCard(
                level="warning",
                margin=ft.margin.only(bottom=10),
                title=translate("*WARNING*"),
                subtitle=translate(
                    "Pre-configure red-lineups with PeaceKeeper commanders!\nThe bot is unable to see the troops health.\nYou should only use this with natural AP bar."
                ),
            ),
            ft.Text("Search Methods", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.OutlinedButton(
                text=translate("Set area location"),
                on_click=lambda _: ss.page.go(f"/set-center/marauders/{self.instance_index}/{self.profile_index}"),
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
            ft.Text("Other Settings", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Text(value=translate("Peacekeeper presets")),
            ft.Column(
                controls=[
                    FletRowPresets(preset_index, self.context)
                    for preset_index in ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
                ],
                wrap=True,
                spacing=10,
                run_spacing=10,
                height=150,
            ),
        )
