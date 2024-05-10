import flet as ft

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from utils.singletons import ss
from views.settings.page_base import BasePage
from views.settings.profile.rows.Flet_row_rss import FletRowRss


class PageRss(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.context = self.tasks.gather_rss

        keys = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
        self.values = {}

        for key in keys:
            self.values[key] = FletRowRss(
                key=key, instance_index=self.instance_index, profile_index=self.profile_index, context=self.context
            )

        self.search_methods_radio_group = ft.RadioGroup(
            content=ft.Column(
                [
                    ft.Radio(value="default", label=translate("Search with default loop method")),
                    ft.Radio(value="zoom", label=translate("Search with zooming method")),
                ]
            ),
            on_change=self.toggle_search_method,
            value=self.context.search_method,
        )

        self.availability_dropdown = ft.Dropdown(
            width=100,
            options=[
                ft.dropdown.Option(text="On all characters", key="all"),
                ft.dropdown.Option(text="Only first character", key="only_first"),
                ft.dropdown.Option(text="On all characters except the first", key="all_except_first"),
            ],
            value=self.context.availability,
            on_change=self.submit_with_context,
            data={"path": "availability", "type": str},
        )

        self.add_control(
            GenerateCard(
                level=translate("tips"),
                subtitle=translate(
                    "If you plan on having the safest configuration, take a look at 'Zoom out method' and 'random' node choice!"
                ),
            ),
            ft.Divider(),
            ft.Text("Availability", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ResponsiveRow(
                controls=[ft.Text("Condition to run task"), self.availability_dropdown],
            ),
            ft.Divider(),
            ft.Text("Search Methods", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            self.search_methods_radio_group,
            ft.Divider(),
            ft.Text("Settings", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.Switch(
                label=translate("Use Yellow presets as gatherers"),
                value=self.context.use_custom_preset,
                on_change=self.submit_with_context,
                data={"path": "use_custom_preset", "type": bool},
            ),
            ft.Container(height=10),
            *self.values.values()
        )

    def toggle_node_levels(self, value):
        for rows in self.values.values():
            rows.node_level_dropdown.disabled = value

    def update_availability(self, e):
        self.data = self.FileSingleton.get_data()

        data = e.control.value

        self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_rss_availability"] = data

        self.FileSingleton.write_data(self.data)

    def toggle_search_method(self, e):
        data = e.control.value

        self.toggle_node_levels(data != "default")

        self.context.search_method = data

        ss.write_emulator_settings(ss.emulator_settings)
        ss.page.update()
