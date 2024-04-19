import flet as ft

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from views.settings.page_base import BasePage


class PageGem(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        # Troop Scan Controls
        self.troop_scan_min_text_field = ft.TextField(
            label=translate("Minimum"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gem_check1"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "gem_check1", int),
            disabled=not self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_swipe_check"],
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.troop_scan_max_text_field = ft.TextField(
            label=translate("Maximum"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gem_check2"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "gem_check2", int),
            disabled=not self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_swipe_check"],
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        # Area Location Controls
        self.kingdom_text_field = ft.TextField(
            label=translate("Your kingdom :"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["kingdom"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "kingdom", str),
            disabled=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] != 'default',
        )

        self.city_x_text_field = ft.TextField(
            label=translate("Area location X coordinates :"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["city_x"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "city_x", int),
            disabled=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] != 'default',
        )

        self.city_y_text_field = ft.TextField(
            label=translate("Area location Y coordinates :"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["city_y"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "city_y", int),
            disabled=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] != 'default',
        )

        # Number of Nodes Controls
        self.node_limit_text_field = ft.TextField(
            label=translate("Fixed number of nodes to gather :"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_note_limit"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "gather_gem_note_limit", int),
            disabled=not self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_enable_node_limit"],
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        # Button Controls
        self.set_area_location_button = ft.OutlinedButton(
            text=translate("Set area location"),
            on_click=lambda _: self.initial_page.go(f"/gather-gems/{self.instance_index}/{self.profile_index}"),
            disabled=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] != "map",
        )

        # Other Controls
        min_duration_text_field = ft.TextField(
            label=translate("Minimum running duration (mins)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_duration1"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "gather_gem_duration1", int),
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        max_duration_text_field = ft.TextField(
            label=translate("Maximum running duration (mins)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_duration2"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "gather_gem_duration2", int),
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        scanning_radius_text_field = ft.TextField(
            label=translate("Scanning radius (km) :"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["radius"],
            content_padding=ft.padding.all(10),
            on_change=lambda e: self.submit(e, "radius", int),
            input_filter=ft.NumbersOnlyInputFilter(),
        )

        self.normal_switch = ft.Switch(
            label=translate("Normal path method (will use cords)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] == "default",
            on_change=self.toggle_search_method,
            data="default",
        )

        spiral_switch = ft.Switch(
            label=translate("Spiral path method (only around your city)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] == "spiral",
            on_change=self.toggle_search_method,
            data="spiral",
        )

        map_switch = ft.Switch(
            label=translate("Map method (Will use your selected area) /!SAFEST!/"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] == "map",
            on_change=self.toggle_search_method,
            data="map"
            ,
        )

        self.detect_free_marches_switch = ft.Switch(
            label=translate("Detect free marches without clicking on the node"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_swipe_check"],
            on_change=lambda _: self.reverse_keyword("gather_gem_swipe_check"),
        )

        self.max_nodes_switch = ft.Switch(
            label=translate("Set the maximum of nodes to gather"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_enable_node_limit"],
            on_change=lambda _: self.reverse_keyword("gather_gem_enable_node_limit"),
        )

        recenter_view_switch = ft.Switch(
            label=translate("Recenter the view based on city location\n(turn off if the cords are NOT your city's cords)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["recenter_feature"],
            on_change=lambda _: self.reverse_keyword("recenter_feature"),
        )

        compare_march_speed_switch = ft.Switch(
            label=translate("Compare march speed (Increase gem gathering\nbut increase number of actions)"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_compare_march_duration"],
            on_change=lambda _: self.reverse_keyword("gather_gem_compare_march_duration"),
        )

        restart_game_switch = ft.Switch(
            label=translate("Restart the game randomly"),
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["restart_game"],
            on_change=lambda _: self.reverse_keyword("restart_game"),
        )
        self.search_methods_radio_group = ft.RadioGroup(
            content=ft.Column([
                ft.Radio(value="default", label=translate("Normal path method (will use cords)")),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            self.kingdom_text_field,
                            self.city_x_text_field,
                            self.city_y_text_field,
                        ],
                    ),
                    margin=ft.margin.only(left=50),
                ),
                ft.Radio(value="map", label=translate("Map method (Will use your selected area)")),
                ft.Container(content=self.set_area_location_button, margin=ft.margin.only(left=50)),
                ft.Radio(value="spiral", label=translate("Spiral path method (only around your city)")),
            ]),
            on_change=self.toggle_search_method,
            value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"]
        )

        self.availability_dropdown = ft.Dropdown(
                        width=100,
                        options=[
                            ft.dropdown.Option(text="On all characters", key="all"),
                            ft.dropdown.Option(text="Only first character", key="only_first"),
                            ft.dropdown.Option(text="On all characters except the first", key="all_except_first"),
                        ],
                        on_change=self.update_availability,
                        value=self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_availability"]
                    )


        # Adding controls
        self.add_control(
            GenerateCard(
                level=translate("warning"),
                title=translate("*REQUIREMENT*"),
                subtitle=translate("Pre-configure yellow-lineups with gathering gem commanders!"),
            ),
            ft.Divider(),
            ft.Text("Availability", weight=ft.FontWeight.BOLD),
            ft.Divider(),
            ft.ResponsiveRow(
                controls=[
                    ft.Text("When to activate"),
                    self.availability_dropdown
                ],
            ),
            ft.Divider(),
            ft.Text("General Settings", weight=ft.FontWeight.BOLD),
            ft.Divider(),

            ft.ResponsiveRow(
                controls=[
                    ft.Column(controls=[min_duration_text_field], col={"sm": 4, "xs": 12}),
                    ft.Column(controls=[max_duration_text_field], col={"sm": 4, "xs": 12}),
                    ft.Column(controls=[scanning_radius_text_field], col={"sm": 4, "xs": 12}),
                ]
            ),
            ft.Divider(),
            ft.Text("Search Methods", weight=ft.FontWeight.BOLD),
            ft.Divider(),

            # self.normal_switch,
            # ft.Container(
            #     content=ft.Column(
            #         controls=[
            #             self.kingdom_text_field,
            #             self.city_x_text_field,
            #             self.city_y_text_field,
            #         ],
            #     ),
            #     margin=ft.margin.only(left=50),
            # ),

            # map_switch,
            # ft.Container(content=self.set_area_location_button, margin=ft.margin.only(left=50)),

            # spiral_switch,
            self.search_methods_radio_group,

            ft.Divider(),
            ft.Text("Other Settings", weight=ft.FontWeight.BOLD),
            ft.Divider(),

            self.detect_free_marches_switch,

            ft.Container(
                content=ft.Column(
                    controls=[
                        self.troop_scan_min_text_field,
                        self.troop_scan_max_text_field,
                    ],
                ),
                margin=ft.margin.only(left=50),
            ),

            self.max_nodes_switch,

            ft.Container(
                content=ft.Column(
                    controls=[
                        self.node_limit_text_field,
                    ],
                ),
                margin=ft.margin.only(left=50),
            ),

            recenter_view_switch,
            compare_march_speed_switch,
            restart_game_switch,
        )

        # Assigning switches for later reference
        self.spiral_switch = spiral_switch
        self.map_switch = map_switch


    def toggle_default(self, value):
        self.kingdom_text_field.disabled = value
        self.city_x_text_field.disabled = value
        self.city_y_text_field.disabled = value

        
    def toggle_spiral(self, value):
        pass

    def toggle_map(self, value):
        self.set_area_location_button.disabled = value

    def update_availability(self, e):
        self.data = self.FileSingleton.get_data()

        data = e.control.value

        self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_availability"] = data

        self.FileSingleton.write_data(self.data)

    def toggle_search_method(self, e):
        self.data = self.FileSingleton.get_data()
        data = e.control.value

        self.toggle_default(data != "default")
        self.toggle_spiral(data != "spiral")
        self.toggle_map(data != "map")

        self.data[str(self.instance_index)]["schedules"][str(self.profile_index)]["gather_gem_method"] = data

        self.FileSingleton.write_data(self.data)
        self.profile.initial_page.update()

    def reverse_keyword(self, keyword: str):
        super().reverse_keyword(keyword)
        self.data = self.FileSingleton.get_data()

        if keyword == "gather_gem_swipe_check":
            is_enabled = self.detect_free_marches_switch.value
            self.troop_scan_min_text_field.disabled = not is_enabled
            self.troop_scan_max_text_field.disabled = not is_enabled
        if keyword == "gather_gem_enable_node_limit":
            is_enabled = self.max_nodes_switch.value
            self.node_limit_text_field.disabled = not is_enabled

        self.profile.initial_page.update()
