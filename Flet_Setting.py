import json

import flet as ft

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}


class SettingContainer(ft.Container):
    def __init__(self, page, tab, instance_index: int, profile_index: int):
        super().__init__()
        with open('user_settings.json') as config_file: self.data = json.load(config_file)
        self.tabs = tab
        self.page = page
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.color_choice = color_bank[self.profile_index]
        self.content = ft.ListView(height=500, expand=0, padding=1, )

        self.create_advanced_switch("gather_gem", "Gather gems", self.page_gems)
        self.create_advanced_switch("gather_rss", "Gather rss", self.page_rss)
        self.create_normal_switch("collect_ressource", "Collect city rss")
        self.create_normal_switch("use_enhanced_buff", "Use enhanced buff")
        self.create_normal_switch("buy_merchant", "Buy merchant")
        self.create_normal_switch("check_donation", "Alliance donation")
        self.create_advanced_switch("material_production", "Material Production", self.page_materials)
        self.create_normal_switch("claim_daily_vip", "Claim VIP Chests")
        self.create_normal_switch("claim_daily_chest", "Claim Daily Chests")
        self.create_normal_switch("claim_daily_quests", "Claim Daily Quests")
        self.create_normal_switch("claim_campaign", "Claim Campaign Rewards")
        self.create_normal_switch("alliance_help", "Alliance Help")
        self.create_advanced_switch("start_fort", "Launch Barbarian Rally", self.page_rally)
        self.create_advanced_switch("scout_fog", "Clear fog", self.page_fog)
        self.create_advanced_switch("heal_troop", "Troops healing", self.page_heal)

        self.content.controls.append(ft.Divider())

        self.create_normal_switch("auto_reconnect", "Auto reconnection")
        self.create_normal_switch("auto_captcha", "Resolve captchas")
        self.create_slow_mode()
        self.create_advanced_switch("switch_character", "Characters switching", self.page_character)
        self.create_advanced_switch("auto_log_back", "Log back from other device", self.page_logback)

        self.create_advanced_switch("loop_task", "Re-do Tasks", self.page_redo)
        self.create_advanced_switch("scheduler", "Profiles", self.page_profile)

    def reset(self):
        self.clean()
        self.content = ft.ListView(height=500, expand=0, padding=1, )
        self.create_advanced_switch("gather_gem", "Gather gems", self.page_gems)
        self.create_advanced_switch("gather_rss", "Gather rss", self.page_rss)
        self.create_normal_switch("collect_ressource", "Collect city rss")
        self.create_normal_switch("use_enhanced_buff", "Use enhanced buff")
        self.create_normal_switch("buy_merchant", "Buy merchant")
        self.create_normal_switch("check_donation", "Alliance donation")
        self.create_advanced_switch("material_production", "Material Production", self.page_materials)
        self.create_normal_switch("claim_daily_vip", "Claim VIP Chests")
        self.create_normal_switch("claim_daily_chest", "Claim Daily Chests")
        self.create_normal_switch("claim_daily_quests", "Claim Daily Quests")
        self.create_normal_switch("claim_campaign", "Claim Campaign Rewards")
        self.create_normal_switch("alliance_help", "Alliance Help")
        self.create_advanced_switch("start_fort", "Launch Barbarian Rally", self.page_rally)
        self.create_advanced_switch("scout_fog", "Clear fog", self.page_fog)
        self.create_advanced_switch("heal_troop", "Troops healing", self.page_heal)

        self.content.controls.append(ft.Divider())

        self.create_normal_switch("auto_reconnect", "Auto reconnection")
        self.create_normal_switch("auto_captcha", "Resolve captchas")
        self.create_slow_mode()
        self.create_advanced_switch("switch_character", "Characters switching", self.page_character)
        self.create_advanced_switch("auto_log_back", "Log back from other device", self.page_logback)

        self.create_advanced_switch("loop_task", "Re-do Tasks", self.page_redo)
        self.create_advanced_switch("scheduler", "Profiles", self.page_profile)
        self.page.update()

    def submit(self, e, keyword, method):
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1"]:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(self.data, indent=2))
            return
        if keyword not in ["sleep_multiplicator","defeat_barbarians"]:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(e.control.value.replace("x", "").replace("level ",""))
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))

    def page_gems(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=1, )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )

        self.content.controls.extend([
            ft.TextField(label="Your kingdom :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["kingdom"],
                         width=300,
                         border=ft.InputBorder.UNDERLINE,
                         filled=True,
                         bgcolor="#ebebeb",
                         content_padding=ft.padding.all(10),
                         on_submit=lambda e: self.submit(e, "kingdom", str)),
            ft.TextField(label="Area location X coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_x"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,bgcolor="#ebebeb",
                         content_padding=ft.padding.all(10),
                         on_submit=lambda e: self.submit(e, "city_x", int)
                         ),
            ft.TextField(label="Area location Y coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_y"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,bgcolor="#ebebeb",
                         content_padding=ft.padding.all(10),
                         on_submit=lambda e: self.submit(e, "city_y", int),
                         ),
            ft.TextField(label="Scanning radius (km) :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["radius"],
                         width=300, border=ft.InputBorder.UNDERLINE,
                         filled=True,bgcolor="#ebebeb",
                         content_padding=ft.padding.all(10),
                         on_submit=lambda e: self.submit(e, "radius", int)),
            ft.Row(
                controls=[
                    ft.Text("Mining duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration1"],
                                 width=80, border=ft.InputBorder.UNDERLINE,
                                 filled=True,bgcolor="#ebebeb",
                                 content_padding=ft.padding.all(10),
                                 on_submit=lambda e: self.submit(e, "gather_gem_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration2"],
                                 width=90, border=ft.InputBorder.UNDERLINE,
                                 filled=True,bgcolor="#ebebeb",
                                 content_padding=ft.padding.all(10),
                                 on_submit=lambda e: self.submit(e, "gather_gem_duration2", int)),
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text("Available troop scan frequency"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check1"],
                                 width=80, border=ft.InputBorder.UNDERLINE,
                                 filled=True,bgcolor="#ebebeb",
                                 content_padding=ft.padding.all(10),
                                 on_submit=lambda e: self.submit(e, "gem_check1", int)),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check2"],
                                 width=90, border=ft.InputBorder.UNDERLINE,
                                 filled=True,bgcolor="#ebebeb",
                                 content_padding=ft.padding.all(10),
                                 on_submit=lambda e: self.submit(e, "gem_check2", int)),
                ]
            ),
            ft.Switch(
                label="Restart the game randomly",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "restart_game"] else False,
                on_change=lambda _: self.reverse_keyword("restart_game")
            ),
            ft.Switch(
                label="Experimental feature",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "gem_experimental"] else False,
                on_change=lambda _: self.reverse_keyword("gem_experimental")
            )
        ]

        )
        # print(self.page)
        self.page.update()

    def page_rss(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        keys = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
            "Sixth",
            "Seventh"
        ]
        for key in keys:
            self.content.controls.extend([
                ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(f"{key} choice :"),
                            alignment=ft.alignment.center_right
                        ),

                        ft.Dropdown(
                            width=140,
                            height=70,
                            label="Node Type",
                            options=[
                                ft.dropdown.Option("food"),
                                ft.dropdown.Option("wood"),
                                ft.dropdown.Option("stone"),
                                ft.dropdown.Option("gold"),
                            ],
                            value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][key],
                            on_change=lambda e: self.submit(e, key, str)
                        ),

                        ft.Dropdown(
                            width=140,
                            height=70,
                            label="Node Level",
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
                            value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                key + "_level"],
                            on_change=lambda e: self.submit(e, key + "_level", int)
                        ),
                    ]
                )
            ]
            )
        self.update()

    def page_fog(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.content = ft.Column()
        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ),
            ft.TextField(label="Scout building placement X :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "scout_building_x"],
                         width=300,
                         on_submit=lambda e: self.submit(e, "scout_building_x", int),
                         ),
            ft.TextField(label="Scout building placement Y :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "scout_building_y"],
                         width=300,
                         on_submit=lambda e: self.submit(e, "scout_building_y", int)),
            ft.Row(
                controls=[
                    ft.Text("Scout duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration1"],
                                 width=80,
                                 on_submit=lambda e: self.submit(e, "scout_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration2"],
                                 width=90,
                                 on_submit=lambda e: self.submit(e, "scout_duration2", int)),
                ]
            )]
        )
        self.update()

    def page_heal(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.content = ft.Column()
        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ),
            ft.TextField(label="Healing building placement X :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_building_y"],
                         width=300,
                         on_submit=lambda e: self.submit(e, "healing_building_x", int)),
            ft.TextField(label="Healing building placement Y :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_building_y"],
                         width=300,
                         on_submit=lambda e: self.submit(e, "healing_building_y", int)
                         ),
            ft.TextField(label="Heal batch :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_count"],
                         width=300,
                         on_submit=lambda e: self.submit(e, "healing_count", int),
                         )
        ]
        )
        self.update()

    def page_materials(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        keys = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
        ]
        for i in range(1, 6):
            self.content.controls.extend([
                ft.Row(
                    controls=[
                        ft.Container(
                            width=100,
                            content=ft.Text(f"{keys[i - 1]} choice :"),
                            alignment=ft.alignment.center_right
                        ),

                        ft.Dropdown(
                            width=140,
                            height=70,
                            label="Type",
                            options=[
                                ft.dropdown.Option("leather"),
                                ft.dropdown.Option("stone"),
                                ft.dropdown.Option("ebony"),
                                ft.dropdown.Option("bones"),
                            ],
                            value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                f"material_choice_{i}"],
                            on_change=lambda e: self.submit(e, f"material_choice_{i}", str)
                        )
                    ]
                )
            ]
            )
        self.update()

    def page_rally(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.content = ft.Column()
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        keys = [
            "First",
            "Second",
            "Third",
            "Fourth",
            "Fifth",
            "Sixth",
            "Seventh"
        ]
        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.Container(
                        width=100,
                        content=ft.Text(f"Mobilisation time (minutes):"),
                        alignment=ft.alignment.center_right
                    ),

                    ft.Dropdown(
                        width=140,
                        height=70,
                        label="Minutes",
                        options=[
                            ft.dropdown.Option("5"),
                            ft.dropdown.Option("10"),
                            ft.dropdown.Option("30"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["rally_time"],
                        on_change=lambda e: self.submit(e, "rally_time", int)
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.Container(
                        width=100,
                        content=ft.Text(f"Rally type :"),
                        alignment=ft.alignment.center_right
                    ),

                    ft.Dropdown(
                        width=140,
                        height=70,
                        label="Type",
                        options=[
                            ft.dropdown.Option("cav"),
                            ft.dropdown.Option("inf"),
                            ft.dropdown.Option("archers"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["rally_type"],
                        on_change=lambda e: self.submit(e, "rally_type", str)
                    )
                ]
            )
        ]
        )
        self.update()

    def page_character(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ))

        self.content.controls.append(
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "leave_game_switch_character"] else False,
                on_change=lambda _: self.reverse_keyword("leave_game_switch_character")
            )
        )
        self.page.update()

    def page_logback(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ),
            ft.Row(
                controls=[
                    ft.Text(
                        "Time to wait before the bot log\nback from your connection(mins): "
                    ),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back1"],
                                 width=80,
                                 on_submit=lambda e: self.submit(e, "log_back1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back2"],
                                 width=90,
                                 on_submit=lambda e: self.submit(e, "log_back2", int)
                                 )
                ]
            )
        ]
        )

        self.update()

    def page_profile(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )

        self.content.controls.extend([

            ft.Switch(
                label="Profile n°1",
                active_track_color="#3b8ed0",
                value=True if self.data[str(self.instance_index)]['schedules'][str(1)][
                    "enabled"] else False,
                on_change=lambda _: self.reverse_keyword("enabled", 1)
            ),
            ft.Switch(
                label="Profile n°2",
                active_track_color="#ba4543",
                value=True if self.data[str(self.instance_index)]['schedules'][str(2)][
                    "enabled"] else False,
                on_change=lambda _: self.reverse_keyword("enabled", 2)
            ),
            ft.Switch(
                label="Profile n°3",
                active_track_color="#dec433",
                value=True if self.data[str(self.instance_index)]['schedules'][str(3)][
                    "enabled"] else False,
                on_change=lambda _: self.reverse_keyword("enabled", 3)
            )
        ]
        )
        self.update()

    def page_redo(self):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        # self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )

        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.Text(
                        "*Randomise it as much as possible*",
                        size=20,
                        font_family="RobotoSlab",
                        weight=ft.FontWeight.W_400,
                        color="red"
                    )
                ]
            ),

            ft.Text(
                "Time to wait before\nthe bot re-do the tasks selected  (mins):"
            ),
            ft.Row(
                controls=[
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop1"],
                                 width=80,
                                 on_submit=lambda e: self.submit(e, "time_to_wait_loop1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop2"],
                                 width=90,
                                 on_submit=lambda e: self.submit(e, "time_to_wait_loop2", int)
                                 )
                ]
            )
        ]
        )
        self.update()

    def reverse_keyword(self, keyword: str, index=None):
        if index is None:
            index = self.profile_index
        print(f"{keyword = }, {index = }, {self.instance_index =}")
        if keyword not in ["loop_task", "scheduler"]:
            self.data[str(self.instance_index)]['schedules'][str(index)][keyword] = not \
                self.data[str(self.instance_index)]['schedules'][str(index)][keyword]
        else:
            self.data[str(self.instance_index)][keyword] = not \
                self.data[str(self.instance_index)][keyword]
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))

    def create_normal_switch(self, keyword: str, text: str):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        print(keyword)
        self.content.controls.append(
            ft.Switch(
                label=text,
                active_track_color=self.color_choice,
                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    keyword] else False,
                on_change=lambda _: self.reverse_keyword(keyword)
            )
        )

    def create_advanced_switch(self, keyword: str, text: str, function):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        if keyword not in ["loop_task", "scheduler"]:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,
                            active_track_color=self.color_choice,
                            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                keyword] else False,
                            on_change=lambda _: self.reverse_keyword(keyword),

                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon_color=self.color_choice,
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        else:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,
                            active_track_color=self.color_choice,
                            value=True if self.data[str(self.instance_index)][keyword] else False,
                            on_change=lambda _: self.reverse_keyword(keyword)
                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon_color=self.color_choice,
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function()
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )

    def create_barbs_row(self):
        self.content.controls.append(ft.Row
            (
            controls=[
                ft.Switch(
                    label="Kill barbs with AP",
                    active_track_color=self.color_choice,
                    value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                        "defeat_barbarians"] else False,
                    on_change=lambda _: self.reverse_keyword("defeat_barbarians")
                ),
                ft.Dropdown(
                    width=140,
                    height=70,
                    label="Multiplicator",
                    options=[
                        ft.dropdown.Option(f"level {i}") for i in range(1,51)],
                    value="level " +str(self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                  "barbarians_level"]),
                    on_change=lambda e: self.submit(e, "barbarians_level", str)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        )
    def create_slow_mode(self):
        self.content.controls.append(ft.Row
            (
            controls=[
                ft.Switch(
                    label="Slow mode",
                    active_track_color=self.color_choice,
                    value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                        "slow_mode"] else False,
                    on_change=lambda _: self.reverse_keyword("slow_mode")
                ),
                ft.Dropdown(
                    width=140,
                    height=70,
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
                    value=str(self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                  "sleep_multiplicator"]) + "x",
                    on_change=lambda e: self.submit(e, "sleep_multiplicator", str)
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        )
