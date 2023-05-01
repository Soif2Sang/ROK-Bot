import json
import shutil
from os.path import exists

import flet as ft
import pyautogui

from Task_utils import get_data, write_data


class Tile(ft.Row):
    def __init__(self, page, number, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.number = number
        self.started = False
        self.button_select = ft.IconButton(
            icon=ft.icons.PAGEVIEW,
            selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED,
            on_click=lambda _: self.select()
        )
        self.button_start = ft.IconButton(
            icon=ft.icons.NOT_STARTED_OUTLINED,
            on_click=lambda _: self.start()
        )
        self.button_stop = ft.IconButton(
            icon=ft.icons.STOP_OUTLINED,
            disabled=True,
            on_click=lambda _: self.stop()
        )
        self.text_name = ft.Text(value="main")
        self.text_status = ft.Text(value="Inactive")

        self.controls.extend([
            self.button_select,
            self.button_start,
            self.button_stop,
            self.text_name,
            self.text_status
        ]
        )

    def select(self):
        self.page.tile_manager.unselect_all()
        self.button_select.selected = True
        self.button_select.update()

        if self.page.frames == {}:
            self.page.frames[self.number] = Frame(self.page, self.number)
            self.page.add(self.page.frames[self.number])
            self.page.update()
        else:
            self.page.controls.pop()
            if self.number not in self.page.frames:
                self.page.frames[self.number] = Frame(self.page, self.number)
            self.page.add(self.page.frames[self.number])
            self.page.update()

    def start(self):
        print(self.number)
        self.started = not self.started
        if self.started:
            self.button_start.icon = ft.icons.PAUSE
            self.button_stop.disabled = False
        else:
            self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
            self.button_stop.disabled = True
        self.update()

    def stop(self):
        self.started = False
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        self.update()


class NavigationBar(ft.Row):
    def __init__(self, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.tileManager = tile_manager
        self.button_refresh = ft.TextButton(text="Refresh", on_click=lambda _: self.tileManager.refresh())
        self.controls.append(self.button_refresh)


class TileManager(ft.Column):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.tiles = {}
        self.navigation_bar = NavigationBar(self)
        self.controls.append(self.navigation_bar)

    def add_tile(self, number: str):
        self.tiles[number] = Tile(self.page, number)
        self.controls.append(self.tiles[number])
        self.update()

    def delete_tile(self, number: str):
        self.controls.remove(self.tiles[number])
        del self.tiles[number]
        self.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            tile.button_select.selected = False
            tile.button_select.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def get_dic_instances(self):
        with open(rf'bluestacks.txt', 'r', encoding='utf-8') as file:
            data_instance = file.read().split('\n')

        def sort_by_instance(tab):
            for i in range(len(tab)):
                for y in range(len(tab) - 1):
                    if len(tab[y]['instance']) == len(tab[y + 1]['instance']):
                        if tab[y]['instance'] > tab[y + 1]['instance']:
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
                    else:
                        if len(tab[y]['instance']) > len(tab[y + 1]['instance']):
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
            dic = {}
            for i in range(len(tab)):
                dic[str(i)] = tab[i]
            return dic

        liste_info = []
        for element in data_instance:
            if ((('bst.instance.Nougat64' in element) and ('adb_port' in element))
                and 'status' in element) or \
                    (('bst.instance.Nougat64' in element) and ('display_name' in element)
                    ):
                liste_info.append(element)
        tab_instance = []
        for i in range(0, len(liste_info), 2):
            string = liste_info[i + 1].split('.status.adb_port=')

            instance = string[0].split(".")[-1]
            port = string[1].replace('"', "")
            display_name = liste_info[i].split('.display_name=')[1].replace('"', "")

            dico_instance = {
                'instance': str(instance),
                'port': port,
                'name': display_name
            }
            tab_instance.append(dico_instance)
        return sort_by_instance(tab_instance)

    def get_names(self, data):
        names = []
        for key in data.keys():
            for element in data[key]:
                if element == 'name':
                    names.append((len(names), data[key][element]))
        return names

    def get_current_instances(self, data):
        names = self.get_names(data)
        # print(f"{names = }")
        # print(names)
        instances_available = []
        for win in pyautogui.getAllWindows():
            for name in names:
                if win.title == name[1]:
                    instances_available.append(name)
        # print(instances_available)
        instances_available.sort(key=lambda x: x[0])
        # print(instances_available)
        return instances_available

    def get_all_vms_running(self):
        return self.get_current_instances(self.get_dic_instances())

    def refresh(self):
        instances = self.get_all_vms_running()
        for i in range(len(self.controls) - 1):
            self.controls.pop()
        print(f"{self.controls = }")
        for instance in instances:
            if instance[0] in self.tiles:
                self.controls.append(self.tiles[instance[0]])
            else:
                self.controls.append(Tile(self.page, instance[0]))
        self.update()


class Logger(ft.ListView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)

    def add_text(self, texte:str):
        self.controls.append(ft.Text(value=texte))

color_bank ={
    1:"#3b8ed0",
    2:"#ba4543",
    3:"#dec433"
}

class SettingContainer(ft.Container):
    def __init__(self, page,tab, instance_index: int, profile_index: int):
        super().__init__()
        self.data = get_data()
        self.tabs = tab
        self.page = page
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.color_choice = color_bank[self.profile_index]
        self.content = ft.ListView(height=500, expand=0, padding=1, )

        self.create_advanced_switch("gather_rss", "Gather rss", self.page_rss)

        self.content.controls.append(ft.Divider())

        self.create_normal_switch("auto_reconnect", "Auto reconnection")
        self.create_normal_switch("auto_captcha", "Resolve captchas")
        self.create_slow_mode()
        self.create_advanced_switch("auto_log_back", "Characters switching", self.page_character)
        self.create_advanced_switch("switch_character", "Log back from other device", self.page_logback)

        self.create_advanced_switch("loop_task", "Re-do Tasks", self.page_redo)
        self.create_advanced_switch("scheduler", "Profiles", self.page_profile)

    def reset(self):
        self.clean()
        self.content = ft.ListView(height=500, expand=0, padding=1, )
        self.create_advanced_switch("gather_rss", "Gather rss", self.page_rss)

        self.content.controls.append(ft.Divider())

        self.create_normal_switch("auto_reconnect", "Auto reconnection")
        self.create_normal_switch("auto_captcha", "Resolve captchas")
        self.create_slow_mode()
        self.create_advanced_switch("auto_log_back", "Characters switching", self.page_character)
        self.create_advanced_switch("switch_character", "Log back from other device", self.page_logback)

        self.create_advanced_switch("loop_task", "Re-do Tasks", self.page_redo)
        self.create_advanced_switch("scheduler", "Profiles", self.page_profile)
        self.page.update()

    def submit(self, e, keyword, method):
        if keyword in ["time_to_wait_loop2","time_to_wait_loop1"]:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            write_data(self.data)
            return
        if keyword != "sleep_multiplicator":
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(e.control.value.replace("x",""))
        write_data(self.data)


    def page_gems(self):
        self.data = get_data()
        print("ici")
        self.clean()
        print("ici")
        self.tabs.expand=True
        self.content = ft.ListView(height=500, expand=0, padding=1, )
        print("ici")
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
                         on_change=lambda e: self.submit(e, "kingdom", str)),
            ft.TextField(label="Area location X coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_x"],
                         width=300,
                         on_change=lambda e: self.submit(e, "city_x", int)
                         ),
            ft.TextField(label="Area location Y coordinates :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["city_y"],
                         width=300,
                         on_change=lambda e: self.submit(e, "city_y", int),
                         ),
            ft.TextField(label="Scanning radius (km) :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["radius"],
                         width=300,
                         on_change=lambda e: self.submit(e, "radius", int)),
            ft.Row(
                controls=[
                    ft.Text("Mining duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "gather_gem_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gather_gem_duration2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "gather_gem_duration2", int)),
                ]
            ),
            ft.Row(
                controls=[
                    ft.Text("Available troop scan frequency"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "gem_check1", int)),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "gem_check2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "gem_check2", int)),
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
        self.data = get_data()
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
                                ft.dropdown.Option("gold"),
                                ft.dropdown.Option("wood"),
                                ft.dropdown.Option("stone"),
                                ft.dropdown.Option("mana"),
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
        self.data = get_data()
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
                         on_change=lambda e: self.submit(e, "scout_building_x", int),
                         ),
            ft.TextField(label="Scout building placement Y :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "scout_building_y"],
                         width=300,
                         on_change=lambda e: self.submit(e, "scout_building_y", int)),
            ft.Row(
                controls=[
                    ft.Text("Scout duration (mins)"),
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "scout_duration1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "scout_duration2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "scout_duration2", int)),
                ]
            )]
        )
        self.update()

    def page_heal(self):
        self.data = get_data()
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
                         on_change=lambda e: self.submit(e, "healing_building_x", int)),
            ft.TextField(label="Healing building placement Y :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_building_y"],
                         width=300,
                         on_change=lambda e: self.submit(e, "healing_building_y", int)
                         ),
            ft.TextField(label="Heal batch :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                             "healing_count"],
                         width=300,
                         on_change=lambda e: self.submit(e, "healing_count", int),
                         )
            ]
        )
        self.update()

    def page_materials(self):
        self.data = get_data()
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
        self.data = get_data()
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
        self.data = get_data()
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
        self.data = get_data()
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
                                 on_change=lambda e: self.submit(e, "log_back1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "log_back2", int)
                                 )
                ]
            )
            ]
        )

        self.update()


    def page_profile(self):
        self.data = get_data()
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
                on_change=lambda _: self.reverse_keyword("enabled",1)
            ),
            ft.Switch(
                label="Profile n°2",
                active_track_color="#ba4543",
                value=True if self.data[str(self.instance_index)]['schedules'][str(2)][
                    "enabled"] else False,
                on_change=lambda _: self.reverse_keyword("enabled",2)
            ),
            ft.Switch(
                label="Profile n°3",
                active_track_color="#dec433",
                value=True if self.data[str(self.instance_index)]['schedules'][str(3)][
                    "enabled"] else False,
                on_change=lambda _: self.reverse_keyword("enabled",3)
            )
            ]
        )
        self.update()

    def page_redo(self):
        self.data = get_data()
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

        self.page.extend([
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
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop2", int)
                                 )
                ]
            )
            ]
        )
        self.update()

    def reverse_keyword(self, keyword: str, index = None):
        self.data = get_data()
        if index is None:
            index = self.instance_index
        if keyword not in ["loop_task", "scheduler"]:
            self.data[str(self.instance_index)]['schedules'][str(index)][keyword] = not \
                self.data[str(self.instance_index)]['schedules'][str(index)][keyword]
        else:
            self.data[str(self.instance_index)][keyword] = not \
                self.data[str(self.instance_index)][keyword]
        write_data(self.data)

    def create_normal_switch(self, keyword: str, text: str):
        self.data = get_data()
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
        self.data = get_data()
        if keyword not in ["loop_task", "scheduler"]:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,
                            active_track_color=self.color_choice,
                            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                keyword] else False,
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
                                "sleep_multiplicator"]) +"x",
                            on_change=lambda e: self.submit(e, "sleep_multiplicator", str)
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
        )


class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = SettingContainer(page,self, int(number),1)
        self.expand = True
        self.width = 400
        self.logger = Logger()
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logger"))

    def add_text(self, texte:str):
        self.logger.add_text(texte)


def Main(page: ft.Page):
    page.title = "Rok Bot - 850 Days left"
    page.frames = {}
    page.tile_manager = TileManager(page)
    page.add(page.tile_manager)
    page.tile_manager.add_tile("1")
    page.tile_manager.add_tile("2")
    page.update()

ft.app(target=Main, view=ft.FLET_APP)
