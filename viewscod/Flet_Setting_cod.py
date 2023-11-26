import multiprocessing

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from utils.functions import FileSingleton
from views import frametime
from views.settings.profile.cols.Flet_col_transfer import FletColumnRss
from views.settings.profile.rows.Flet_row_material import FletRowMaterial
from views.settings.profile.rows.Flet_row_presets import FletRowPresets
from views.settings.profile.rows.Flet_row_troops import FletRowTraining
from viewscod.Flet_city_layout_cod import CityPlacement
from viewscod.Flet_row_rss_cod import FletRowRss

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


class SettingContainer(ft.Container):
    def __init__(self, page, instance_index: str, profile_index: int):
        super().__init__()
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
        self.page = page
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.color_choice = color_bank[self.profile_index]
        self.content: ft.ListView = ft.ListView(
            height=500, expand=0, padding=1, width=300, spacing=2
        )
        self.init()

    def nextView(self, page, params, basket):
        self.page.window_width = 900
        self.page.window_height = 500
        return ft.View(
            f"/city-layout/{self.instance_index}/{self.profile_index}",
            controls=[
                ft.Container(
                    bgcolor="#ecf0f1",
                    content=ft.Row(
                        controls=[
                            ft.IconButton(
                                icon=ft.icons.ARROW_BACK,
                                on_click=lambda _: self.returnHome(),
                            ),
                            ft.Text(value="Go back"),
                        ]
                    ),
                ),
                ft.Text(
                    value="Click on the building button you wanna set, then click in the center of the building."
                ),
                CityPlacement(self.instance_index, self.profile_index),
            ],
        )

    def returnHome(self):
        self.page.window_width = 450
        self.page.window_height = 700
        self.page.go("/")

    def init(self):
        # self.create_advanced_switch("gather_gem", "Gather gems", self.page_gems)
        self.create_advanced_switch("gather_rss", "Gather rss", self.page_rss)
        # self.create_normal_switch("collect_ressource", "Collect city rss")
        # self.create_normal_switch("use_enhanced_buff", "Use enhanced buff")
        # self.create_normal_switch("buy_merchant", "Buy merchant")
        self.create_normal_switch("check_donation", "Alliance donation")
        # self.create_advanced_switch("material_production", "Material Production", self.page_materials)
        self.create_advanced_switch("train_troops", "Train troops", self.page_troops)
        self.create_advanced_switch(
            "academy_research", "Academy Research", self.show_cords_page
        )
        self.create_normal_switch("claim_daily_vip", "Claim VIP Chests")
        self.create_normal_switch("claim_daily_chest", "Claim Daily Chests")
        # self.create_normal_switch("claim_daily_quests", "Claim Daily Quests")
        # self.create_normal_switch("claim_campaign", "Claim Campaign Rewards")
        # self.create_normal_switch("alliance_help", "Alliance Help")
        # self.create_advanced_switch("defeat_barbarians", "Hunt Barbarians", self.page_barbs)
        # self.create_advanced_switch("start_fort", "Launch Barbarian Rally", self.page_rally)
        self.create_advanced_switch("scout_fog", "Clear fog", self.page_fog)
        # self.create_advanced_switch("heal_troop", "Troops healing", self.page_heal)
        # self.create_advanced_switch("transfer_enable", "Rss Transfer", self.page_transfer)

        self.content.controls.append(ft.Divider())

        # self.create_normal_switch("auto_reconnect", "Auto reconnection")
        # self.create_normal_switch("auto_captcha", "Resolve captchas")
        self.create_slow_mode()
        # self.create_advanced_switch("switch_character", "Characters switching", self.page_character)
        # self.create_advanced_switch("auto_log_back", "Log back from other device", self.page_logback)

        self.create_advanced_switch("loop_task", "Re-do Tasks", self.page_redo)
        self.create_advanced_switch("scheduler", "Profiles", self.page_profile)

        self.content.controls.append(
            ft.TextField(
                label="Custom API key:",
                value=self.data[str(self.instance_index)]["API_KEY"],
                on_change=lambda e: self.submit(e, "API_KEY", str),
            )
        )

    def reset(self):
        self.content.clean()
        self.init()
        self.page.update()

    def submit(self, e, keyword, method):
        self.data = self.FileSingleton.get_data()
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1", "API_KEY"]:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            print(self.data[str(self.instance_index)][keyword])
            return self.FileSingleton.write_data(self.data)

        if keyword not in ["sleep_multiplicator", "defeat_barbarians"]:
            self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][
                keyword
            ] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][
                keyword
            ] = float(e.control.value.replace("x", "").replace("level ", ""))
        self.FileSingleton.write_data(self.data)

    def page_gems(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=1,
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )

        self.content.controls.extend(
            [
                ft.Divider(),
                ft.Text(
                    value="*REQUIREMENT*\n/!\ Pre-configure yellow-lineups with farmers !",
                    size=15,
                    color="red",
                ),
                ft.Divider(),
                ft.TextField(
                    label="Your kingdom :",
                    value=self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["kingdom"],
                    width=300,
                    content_padding=ft.padding.all(10),
                    on_change=lambda e: self.submit(e, "kingdom", str),
                ),
                ft.Divider(),
                ft.TextField(
                    label="Area location X coordinates :",
                    value=self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["city_x"],
                    width=300,
                    content_padding=ft.padding.all(10),
                    on_change=lambda e: self.submit(e, "city_x", int),
                ),
                ft.Divider(),
                ft.TextField(
                    label="Area location Y coordinates :",
                    value=self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["city_y"],
                    width=300,
                    content_padding=ft.padding.all(10),
                    on_change=lambda e: self.submit(e, "city_y", int),
                ),
                ft.Divider(),
                ft.TextField(
                    label="Scanning radius (km) :",
                    value=self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["radius"],
                    width=300,
                    content_padding=ft.padding.all(10),
                    on_change=lambda e: self.submit(e, "radius", int),
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text("Mining duration (mins)"),
                        ft.TextField(
                            label="Minimum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["gather_gem_duration1"],
                            width=80,
                            content_padding=ft.padding.all(10),
                            on_change=lambda e: self.submit(
                                e, "gather_gem_duration1", int
                            ),
                        ),
                        ft.Text("~"),
                        ft.TextField(
                            label="Maximum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["gather_gem_duration2"],
                            width=90,
                            content_padding=ft.padding.all(10),
                            on_change=lambda e: self.submit(
                                e, "gather_gem_duration2", int
                            ),
                        ),
                    ]
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text("Available troop scan frequency"),
                        ft.TextField(
                            label="Minimum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["gem_check1"],
                            width=80,
                            content_padding=ft.padding.all(10),
                            on_change=lambda e: self.submit(e, "gem_check1", int),
                        ),
                        ft.Text("~"),
                        ft.TextField(
                            label="Maximum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["gem_check2"],
                            width=90,
                            content_padding=ft.padding.all(10),
                            on_change=lambda e: self.submit(e, "gem_check2", int),
                        ),
                    ]
                ),
                ft.Switch(
                    label="Restart the game randomly",
                    active_track_color=self.color_choice,
                    value=True
                    if self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["restart_game"]
                    else False,
                    on_change=lambda _: self.reverse_keyword("restart_game"),
                ),
                ft.Switch(
                    label="Experimental feature",
                    active_track_color=self.color_choice,
                    value=True
                    if self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["gem_experimental"]
                    else False,
                    on_change=lambda _: self.reverse_keyword("gem_experimental"),
                ),
            ]
        )
        # print(self.page)
        self.page.update()

    def page_troops(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content: ft.ListView = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )

        self.content.controls.append(
            ft.Divider(),
        )
        # self.show_cords_page()
        keys = [
            "infantry",
            "cavalry",
            "archery",
            "siege",
        ]
        for key in keys:
            self.content.controls.append(
                FletRowTraining(
                    key=key,
                    instance_index=self.instance_index,
                    profile_index=self.profile_index,
                )
            )
        self.content.controls.append(ft.Divider())
        self.content.controls.append(
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text="Set training camps position",
                on_click=lambda _: self.show_cords_page(),
            )
        )
        self.update()

    def page_rss(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content: ft.ListView = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        keys = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
        self.data = self.FileSingleton.get_data()
        for key in keys:
            self.content.controls.append(
                FletRowRss(
                    key=key,
                    instance_index=self.instance_index,
                    profile_index=self.profile_index,
                )
            )

        self.update()

    def page_fog(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                        ),
                        ft.Text("Settings", size=20),
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text("Scout duration (mins)"),
                        ft.TextField(
                            label="Minimum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["scout_duration1"],
                            width=80,
                            on_change=lambda e: self.submit(e, "scout_duration1", int),
                        ),
                        ft.Text("~"),
                        ft.TextField(
                            label="Maximum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["scout_duration2"],
                            width=90,
                            on_change=lambda e: self.submit(e, "scout_duration2", int),
                        ),
                    ]
                ),
                ft.Divider(),
                ft.OutlinedButton(
                    icon=ft.icons.GPS_FIXED_SHARP,
                    text="Set Scout camp position",
                    on_click=lambda _: self.show_cords_page(),
                ),
            ]
        )
        self.update()

    def show_cords_page(self):
        self.page.tile_manager.tiles[str(self.instance_index)].runner.adb.save_screen(
            "city"
        )
        self.page.go(f"/city-layout/{self.instance_index}/{self.profile_index}")

    def page_heal(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                        ),
                        ft.Text("Settings", size=20),
                    ],
                ),
                ft.Divider(),
                ft.TextField(
                    label="Heal batch :",
                    value=self.data[str(self.instance_index)]["schedules"][
                        str(self.profile_index)
                    ]["healing_count"],
                    width=300,
                    on_change=lambda e: self.submit(e, "healing_count", int),
                ),
                ft.Divider(),
                ft.OutlinedButton(
                    icon=ft.icons.GPS_FIXED_SHARP,
                    text="Set Hospital position",
                    on_click=lambda _: self.show_cords_page(),
                ),
            ]
        )
        self.update()

    def page_materials(self):
        self.data = self.FileSingleton.get_data()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        keys = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
        ]
        for i in range(1, 6):
            self.content.controls.append(
                FletRowMaterial(
                    keys=keys,
                    i=i,
                    instance_index=self.instance_index,
                    profile_index=self.profile_index,
                )
            )
        self.update()

    def page_transfer(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.content: ft.ListView = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Text(
                value="/!\ This feature require a custom ApiKey /!\ \n"
                "/!\ This feature is on beta and may crash /!\ \n",
                size=15,
                color="red",
            )
        )
        self.content.controls.append(ft.Divider())
        self.content.controls.append(
            FletColumnRss(self.instance_index, self.profile_index)
        )
        self.content.controls.append(ft.Divider())
        self.content.controls.append(
            ft.OutlinedButton(
                icon=ft.icons.GPS_FIXED_SHARP,
                text="Set City Position",
                on_click=lambda _: self.show_cords_page(),
            )
        )
        self.update()

    def page_barbs(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.content: ft.ListView = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        self.content.controls.extend(
            [
                ft.Text(
                    value="*REQUIREMENT*\n\n/!\ Pre-configure all red slot with PeaceKeeper/!\ \n\n/!\Avoid AOE to not hit higher barb level/!\ \n\n/!\The bot is unenable see to the troops health/!\ \n\nNote this function is not designed for New accounts !",
                    size=15,
                    color="red",
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text(value="Barbarian Level"),
                        ft.Dropdown(
                            width=50,
                            options=[ft.dropdown.Option(str(i)) for i in range(1, 56)],
                            on_change=lambda e: self.submit(e, "barbarians_level", str),
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["barbarians_level"],
                        ),
                    ],
                    width=300,
                ),
                ft.Divider(),
                ft.Text(value="Peacekeeper presets"),
                ft.Column(
                    controls=[
                        FletRowPresets(
                            self.instance_index, self.profile_index, str(preset_index)
                        )
                        for preset_index in range(1, 8)
                    ],
                    wrap=True,
                    spacing=10,
                    run_spacing=10,
                    height=150,
                ),
            ]
        )
        self.update()

    def page_rally(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.content: ft.ListView = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        keys = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth", "Seventh"]
        self.content.controls.extend(
            [
                ft.Text(
                    value="*REQUIREMENT*\n/!\ Pre-configure first slot of red line-up with rally Leader !",
                    size=15,
                    color="red",
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(f"Mobilisation time (minutes):"),
                            alignment=ft.alignment.center_right,
                        ),
                        ft.Dropdown(
                            width=140,
                            height=50,
                            content_padding=ft.Padding(
                                left=5, top=3, right=5, bottom=3
                            ),  # modify to your likings
                            label="Minutes",
                            options=[
                                ft.dropdown.Option("5"),
                                ft.dropdown.Option("10"),
                                ft.dropdown.Option("30"),
                            ],
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["rally_time"],
                            on_change=lambda e: self.submit(e, "rally_time", int),
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(f"Rally type :"),
                            alignment=ft.alignment.center_right,
                        ),
                        ft.Dropdown(
                            width=140,
                            height=50,
                            content_padding=ft.Padding(
                                left=5, top=3, right=5, bottom=3
                            ),  # modify to your likings
                            label="Type",
                            options=[
                                ft.dropdown.Option("cav"),
                                ft.dropdown.Option("inf"),
                                ft.dropdown.Option("archers"),
                            ],
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["rally_type"],
                            on_change=lambda e: self.submit(e, "rally_type", str),
                        ),
                    ]
                ),
            ]
        )
        self.update()

    def page_character(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        self.content.controls.append(
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",
                active_track_color=self.color_choice,
                value=True
                if self.data[str(self.instance_index)]["schedules"][
                    str(self.profile_index)
                ]["leave_game_switch_character"]
                else False,
                on_change=lambda _: self.reverse_keyword("leave_game_switch_character"),
            )
        )
        self.page.update()

    def page_logback(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                        ),
                        ft.Text("Settings", size=20),
                    ],
                ),
                ft.Divider(),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Time to wait before the bot log\nback from your connection(mins): \n\n",
                            size=17,
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Minimum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["log_back1"],
                            width=80,
                            on_change=lambda e: self.submit(e, "log_back1", int),
                        ),
                        ft.Text("~"),
                        ft.TextField(
                            label="Maximum",
                            value=self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["log_back2"],
                            width=90,
                            on_change=lambda e: self.submit(e, "log_back2", int),
                            input_filter=ft.NumbersOnlyInputFilter(),
                        ),
                    ]
                ),
            ]
        )

        self.update()

    def page_profile(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        self.content.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.Switch(
                            label="Profile n°1",
                            active_track_color="#3b8ed0",
                            value=True
                            if self.data[str(self.instance_index)]["schedules"][str(1)][
                                "enabled"
                            ]
                            else False,
                            on_change=lambda _: self.reverse_keyword("enabled", 1),
                        ),
                        ft.ElevatedButton(
                            text="Settings",
                            on_click=lambda _: multiprocessing.Process(
                                target=Flet_time_allower.start,
                                args=(self.instance_index, "1"),
                            ).start(),
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Switch(
                            label="Profile n°2",
                            active_track_color="#ba4543",
                            value=True
                            if self.data[str(self.instance_index)]["schedules"][str(2)][
                                "enabled"
                            ]
                            else False,
                            on_change=lambda _: self.reverse_keyword("enabled", 2),
                        ),
                        ft.ElevatedButton(
                            text="Settings",
                            on_click=lambda _: multiprocessing.Process(
                                target=Flet_time_allower.start,
                                args=(self.instance_index, "2"),
                            ).start(),
                        ),
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Switch(
                            label="Profile n°3",
                            active_track_color="#dec433",
                            value=True
                            if self.data[str(self.instance_index)]["schedules"][str(3)][
                                "enabled"
                            ]
                            else False,
                            on_change=lambda _: self.reverse_keyword("enabled", 3),
                        ),
                        ft.ElevatedButton(
                            text="Settings",
                            on_click=lambda _: multiprocessing.Process(
                                target=Flet_time_allower.start,
                                args=(self.instance_index, "3"),
                            ).start(),
                        ),
                    ]
                ),
            ]
        )
        self.update()

    def page_redo(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        # self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        self.content.controls.extend(
            [
                ft.Row(
                    controls=[
                        ft.Text(
                            "*Randomise it as much as possible*",
                            size=20,
                            font_family="RobotoSlab",
                            weight=ft.FontWeight.W_400,
                            color="red",
                        )
                    ]
                ),
                ft.Text(
                    "Time to wait before\nthe bot re-do the tasks selected  (mins):"
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Minimum",
                            value=self.data[str(self.instance_index)][
                                "time_to_wait_loop1"
                            ],
                            width=80,
                            on_change=lambda e: self.submit(
                                e, "time_to_wait_loop1", int
                            ),
                            input_filter=ft.NumbersOnlyInputFilter(),
                        ),
                        ft.Text("~"),
                        ft.TextField(
                            label="Maximum",
                            value=self.data[str(self.instance_index)][
                                "time_to_wait_loop2"
                            ],
                            width=90,
                            on_change=lambda e: self.submit(
                                e, "time_to_wait_loop2", int
                            ),
                            input_filter=ft.NumbersOnlyInputFilter(),
                        ),
                    ]
                ),
                ft.Switch(
                    label="Close the game after all the tasks are done",
                    value=self.data[str(self.instance_index)]["leave_game_loop"],
                    on_change=lambda _: self.reverse_keyword("leave_game_loop"),
                ),
            ]
        )
        self.update()

    def reverse_keyword(self, keyword: str, index=None):
        if index is None:
            index = self.profile_index
        if keyword not in ["loop_task", "scheduler", "leave_game_loop"]:
            self.data[str(self.instance_index)]["schedules"][str(index)][
                keyword
            ] = not self.data[str(self.instance_index)]["schedules"][str(index)][
                keyword
            ]
        else:
            # print(keyword,self.data[str(self.instance_index)][keyword])

            self.data[str(self.instance_index)][keyword] = not self.data[
                str(self.instance_index)
            ][keyword]
        self.FileSingleton.write_data(self.data)

    def create_normal_switch(self, keyword: str, text: str):
        self.data = self.FileSingleton.get_data()
        self.content.controls.append(
            ft.Switch(
                label=text,
                active_track_color=self.color_choice,
                value=True
                if self.data[str(self.instance_index)]["schedules"][
                    str(self.profile_index)
                ][keyword]
                else False,
                on_change=lambda _: self.reverse_keyword(keyword),
            )
        )

    def create_advanced_switch(self, keyword: str, text: str, function):
        self.data = self.FileSingleton.get_data()
        if keyword not in ["loop_task", "scheduler"]:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,
                            active_track_color=self.color_choice,
                            value=True
                            if self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ][keyword]
                            else False,
                            on_change=lambda _: self.reverse_keyword(keyword),
                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon_color=self.color_choice,
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function(),
                            style=ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(
                                        radius=5
                                    ),
                                }
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        else:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,
                            active_track_color=self.color_choice,
                            value=True
                            if self.data[str(self.instance_index)][keyword]
                            else False,
                            on_change=lambda _: self.reverse_keyword(keyword),
                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon_color=self.color_choice,
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function(),
                            style=ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(
                                        radius=5
                                    ),
                                },
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            )

    def create_barbs_row(self):
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label="Kill barbs with AP",
                        active_track_color=self.color_choice,
                        value=True
                        if self.data[str(self.instance_index)]["schedules"][
                            str(self.profile_index)
                        ]["defeat_barbarians"]
                        else False,
                        on_change=lambda _: self.reverse_keyword("defeat_barbarians"),
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

    def create_slow_mode(self):
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label="Slow mode",
                        active_track_color=self.color_choice,
                        value=True
                        if self.data[str(self.instance_index)]["schedules"][
                            str(self.profile_index)
                        ]["slow_mode"]
                        else False,
                        on_change=lambda _: self.reverse_keyword("slow_mode"),
                    ),
                    ft.Dropdown(
                        width=140,
                        height=50,
                        content_padding=ft.Padding(
                            left=5, top=3, right=5, bottom=3
                        ),  # modify to your likings
                        label="Multiplicator",
                        options=[
                            ft.dropdown.Option("1.0x"),
                            ft.dropdown.Option("1.25x"),
                            ft.dropdown.Option("1.5x"),
                            ft.dropdown.Option("1.75x"),
                            ft.dropdown.Option("2.0x"),
                            ft.dropdown.Option("2.25x"),
                            ft.dropdown.Option("2.5x"),
                            ft.dropdown.Option("2.75x"),
                            ft.dropdown.Option("3.0x"),
                        ],
                        value=str(
                            self.data[str(self.instance_index)]["schedules"][
                                str(self.profile_index)
                            ]["sleep_multiplicator"]
                        )
                        + "x",
                        on_change=lambda e: self.submit(e, "sleep_multiplicator", str),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
