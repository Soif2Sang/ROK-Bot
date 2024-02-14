import copy
import re
import threading

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from utils.Components.PaymentMethods import payment_methods
from utils.constants import VERSION_TYPE
from utils.flet_translations import translate
from utils.functions import get_dic_instances, get_dic_instances_ld
from utils.singletons import EmulatorSingleton, FileSingleton
from views.tiles.tile_upgrade import TileUpgrade


class NavigationBar(ft.Row):
    def __init__(self, page, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.tileManager = tile_manager
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.button_refresh = ft.OutlinedButton(
            text=translate("Refresh"),
            icon=ft.icons.REFRESH_ROUNDED,
            on_click=lambda _: self.tileManager.refresh(),
            style=ButtonStyle(
                shape={
                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                },
                bgcolor=None if not self.tileManager.initial_page.UPGRADE else ft.colors.AMBER_100,
            ),
        )

        self.controls.append(self.button_refresh)

        bottom = ft.BottomSheet(
            content=ft.Container(
                width=300, height=300, content=payment_methods(), alignment=ft.alignment.center, padding=ft.padding.all(30)
            ),
            open=True,
            dismissible=True,
            enable_drag=True,
            on_dismiss=lambda _: self.initial_page.close_bottom_sheet(),
        )

        pattern = r"(\d+) Days left"
        match = re.search(pattern, page.title)
        days_left_str = match.group(1)

        days_left_int = int(days_left_str)

        if days_left_int > 10:
            button_style = ButtonStyle(
                shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                bgcolor=ft.colors.GREEN_100,
                color="black",
            )
        elif 10 >= days_left_int > 5:
            button_style = ButtonStyle(
                shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                bgcolor=ft.colors.ORANGE_300,
                color="black",
            )
        else:
            button_style = ButtonStyle(
                shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                bgcolor=ft.colors.RED_200,
                color="black",
            )

        if VERSION_TYPE == "global":
            self.controls.append(
                ft.Row(
                    controls=[
                        ft.OutlinedButton(
                            text="Renew",
                            icon=ft.icons.SHOPPING_CART_OUTLINED,
                            on_click=lambda e: self.initial_page.show_bottom_sheet(bottom),
                            style=button_style,
                        ),
                        ft.IconButton(
                            icon=ft.icons.MENU,
                            on_click=lambda _: self.initial_page.go("/settings"),
                        ),
                    ]
                )
            )
        else:
            self.controls.append(
                ft.IconButton(
                    icon=ft.icons.MENU,
                    on_click=lambda _: self.initial_page.go("/settings"),
                ),
            )


class TileManagerUpgrade(ft.ListView):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.height = 250
        self.expand = 0
        self.spacing = 5
        self.FileSingleton = FileSingleton()
        self.tiles: dict[str, TileUpgrade] = {}
        self.navigation_bar: NavigationBar = NavigationBar(self.initial_page, self)
        self.controls.append(self.navigation_bar)
        self.start_bar = StartBar(self.initial_page, self)
        # self.controls.append(self.start_bar)

    def add_tile(self, number: str):
        self.tiles[number] = TileUpgrade(self.initial_page, number)
        self.tiles[number].runner = self.start_bar.runner
        self.controls.append(self.tiles[number])
        self.initial_page.update()

    def delete_tile(self, number: str):
        self.controls.remove(self.tiles[number])
        self.tiles.pop(number)
        self.initial_page.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            if isinstance(tile, TileUpgrade):
                tile.bgcolor = ft.colors.SURFACE
        self.initial_page.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def refresh(self):
        data = self.FileSingleton.get_data()

        emulator = EmulatorSingleton().getEmulator()

        if emulator == "bluestacks":
            instances = get_dic_instances()
        else:
            instances = get_dic_instances_ld()

        self.fetched_instances = instances

        default_dic = {
            "instance": "",
            "name": "",
            "host": "127.0.0.1",
            "port": 0,
            "loop_task": False,
            "time_to_wait_loop1": 60,
            "time_to_wait_loop2": 110,
            "leave_game_loop": True,
            "scheduler": False,
            "schedules": {},
        }
        default_profile = {
            "timing": [],
            "enable_timing": False,
            "enabled": False,
            "kingdom": 0,
            "city_x": 0,
            "city_y": 0,
            "radius": 30,
            "First": "stone",
            "Second": "food",
            "Third": "gold",
            "Fourth": "wood",
            "Fifth": "food",
            "Sixth": "food",
            "Seventh": "food",
            "First_level": 5,
            "Second_level": 5,
            "Third_level": 5,
            "Fourth_level": 5,
            "Fifth_level": 5,
            "Sixth_level": 4,
            "Seventh_level": 4,
            "rss_custom_preset": False,
            "auto_reconnect": True,
            "auto_captcha": True,
            "check_donation": False,
            "gather_alliance_pit": False,
            "use_enhanced_buff": False,
            "gather_rss": False,
            "buy_merchant": False,
            "claim_daily_quests": False,
            "collect_ressource": False,
            "defeat_barbarians": False,
            "barbarians_level": 25,
            "barbarians_preset": {
                "1": False,
                "2": False,
                "3": False,
                "4": False,
                "5": False,
                "6": False,
                "7": False,
            },
            "gather_gem": False,
            "gem_check1": 60,
            "gem_check2": 120,
            "gem_experimental": False,
            "recenter_feature": True,
            "gather_gem_duration1": 60,
            "gather_gem_duration2": 90,
            "gather_gem_spiral_method": True,
            "gather_gem_swipe_check": True,
            "gather_gem_compare_march_duration": True,
            "gather_gem_enable_node_limit": False,
            "claim_mails": False,
            "gather_gem_note_limit": 0,
            "restart_game": False,
            "switch_character": False,
            "leave_game_switch_character": False,
            "scout_fog": False,
            "scout_duration1": 60,
            "scout_duration2": 90,
            "slow_mode": False,
            "sleep_multiplicator": 1,
            "auto_log_back": True,
            "log_back1": 5,
            "log_back2": 10,
            "claim_daily_vip": False,
            "claim_daily_chest": False,
            "claim_campaign": False,
            "start_fort": False,
            "rally_type": "cav",
            "rally_time": 10,
            "rally_radius": 20,
            "rally_count": 2,
            "mauraudeurs_forts": False,
            "heal_troop": False,
            "healing_building_x": 980,
            "healing_building_y": 267,
            "healing_count": 1500,
            "material_production": False,
            "material_choice_1": "leather",
            "material_choice_2": "leather",
            "material_choice_3": "leather",
            "material_choice_4": "leather",
            "material_choice_5": "leather",
            "alliance_help": False,
            "train_troops": False,
            "infantry_camp": [],
            "cavalry_camp": [],
            "archery_camp": [],
            "siege_camp": [],
            "hospital": [],
            "scout_camp": [],
            "infantry_enable": True,
            "cavalry_enable": True,
            "archery_enable": True,
            "siege_enable": True,
            "infantry_tier": "t1",
            "cavalry_tier": "t1",
            "archery_tier": "t1",
            "siege_tier": "t1",
            "city_transfer": [],
            "transfer_enable": False,
            "transfer_food": 0,
            "transfer_wood": 0,
            "transfer_stone": 0,
            "transfer_gold": 0,
            "upgrade_city": False,
            "kill_marauders": False,
            "kill_marauders_duration": [30, 90],
            "rally_skip_back": False,
            "gather_rss_method": False,
            "fast_rss_transfer": False,
            "city_hall_position": [],
            "upgrade_city_method": "normal",
            "academic_research": False,
            "academy_position": [],
            "buy_merchant_skip": False,
            "expedition_shop_ethel": False,
            "expedition_shop_items": False,
        }

        for i in range(1, 4):
            default_dic["schedules"][i] = copy.deepcopy(default_profile)
        default_dic["schedules"][1]["enabled"] = True

        for instance in instances:
            if str(instance) not in data:
                data[str(instance)] = copy.deepcopy(default_dic)
            else:
                for key in default_dic:
                    if key not in data[str(instance)]:
                        data[str(instance)][key] = copy.deepcopy(default_dic[key])

                for key in default_profile:
                    for i in range(1, 4):
                        if key not in data[str(instance)]["schedules"][str(i)]:
                            data[str(instance)]["schedules"][str(i)][key] = copy.deepcopy(default_profile[key])

            data[str(instance)]["instance"] = instances[str(instance)]["instance"]
            data[str(instance)]["name"] = instances[str(instance)]["name"]
            data[str(instance)]["port"] = int(instances[str(instance)]["port"])

        self.FileSingleton.write_data(data)

        instances = [(instance, instance) for instance in instances]

        for i in range(len(self.controls) - 1):
            self.controls.pop()
        # print(instances)
        if instances:
            for instance in instances:
                if str(instance[0]) in self.tiles:
                    self.controls.append(self.tiles[str(instance[0])])
                    # self.tiles[str(instance[0])].main_task.adb.update_port()
                    self.tiles[str(instance[0])].runner.adb.update_port()
                else:
                    self.add_tile(str(instance[0]))
        else:
            if emulator == "bluestacks":
                text_explanation = "No emulator found, have you started one?\nIf so, check the correct bluestacks version (Nougat64)"
            else:
                text_explanation = "No emulator found, have you started one?\nIf so, check the correct LdPlayer version (LD9)"

            self.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Icon(ft.icons.INFO_OUTLINED, size=60),
                            ft.Text(
                                translate(text_explanation),
                                text_align=ft.TextAlign.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    margin=ft.margin.only(top=40),
                )
            )
        if instances:
            for instance in instances:
                self.tiles[str(instance[0])].config_overrider.items = []
                self.tiles[str(instance[0])].config_overrider.refresh()
        self.initial_page.update()

        # self.padding = ft.padding.only(top=15, left=0, bottom=0)

    def get_enabled_sel(self):
        tiles = []
        for tile in self.controls[1:]:
            if tile.selected:
                tiles.append(tile.instance)
        return tiles

    def get_enabled_sel_object(self):
        tiles = []
        for tile in self.controls[1:]:
            if tile.selected:
                tiles.append(tile)
        return tiles

    def disable_all_unselected_tiles(self):
        for tile in self.controls[1:]:
            if not tile.selected:
                tile.enable_switch.disabled = True
        self.initial_page.update()

    def enable_all_unselected_tiles(self):
        for tile in self.controls[1:]:
            if not tile.selected:
                tile.enable_switch.disabled = False
        self.initial_page.update()


class StartBar(ft.Row):
    def __init__(self, page, tile_manager: TileManagerUpgrade, **kwargs):
        super().__init__(**kwargs)
        self.text_status = ft.Text()
        self.number = "0"
        self.FileSingleton = FileSingleton()
        self.FileSingleton.get_data()
        self.initial_page = page
        self.tasks_process = None
        self.paused = False
        self.stopped = False

        self.main_task = Task(self)
        self.runner = TaskRunner(self.main_task, self)
        self.tasks_process = threading.Thread(target=self.runner.run_groups)

        self.tile_manager = tile_manager

        self.button_start = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED, on_click=self.start)
        self.button_stop = ft.IconButton(icon=ft.icons.HIGHLIGHT_REMOVE_ROUNDED, disabled=True, on_click=self.stop)

        self.controls.extend([self.button_start, self.button_stop, self.text_status])

    def get_enabled_sel(self):
        return self.tile_manager.get_enabled_sel()

    def get_enabled_sel_object(self):
        return self.tile_manager.get_enabled_sel_object()

    def start_tasks(self):
        # if not self.tasks_process.is_alive():
        #     self.tasks_process = threading.Thread(target=self.runner.run_groups)
        #     for tile in self.tile_manager.controls[1:]:
        #         tile.tasks_process = self.tasks_process
        #         tile.tasks_process = self.tasks_process
        #
        #     self.tasks_process.start()
        # else:
        #     self.add_text("Task is frozen, you may need to restart the bot.")
        #     self.initial_page.generate_toast("Warning", "Task is frozen, you may need to restart the bot.")
        #     print("Task is frozen, you may need to restart the bot.")

        tiles = self.get_enabled_sel_object()
        if not tiles:
            self.page.generate_toast("Warning", "No emulator selected!", ft.colors.AMBER)
            return

        self.data = self.FileSingleton.get_data()
        groups = {}

        for tile in tiles:
            for instance in self.data:
                if isinstance(self.data[instance], dict):
                    if self.data[instance].get("group", None) is not None:
                        if self.data[instance]["instance"] == str(tile.instance):
                            if self.data[instance]["group"] not in groups:
                                groups[self.data[instance]["group"]] = []
                            groups[self.data[instance]["group"]].append(tile)

        threads = []

        for group, tiles in groups.items():
            main_task = Task(self)
            runner = TaskRunner(main_task, self)

            thread = threading.Thread(target=runner.run3, args=(tiles,))
            threads.append((thread, tiles))

        return threads
        # for thread in threads:
        #     thread.join()

    def start(self, e):
        self.button_start.icon = ft.icons.PAUSE
        self.button_stop.disabled = False

        self.paused = False
        self.stopped = False

        for tile in self.tile_manager.controls[1:]:
            tile.paused = False
            tile.stopped = False

        worker_threads = self.start_tasks()

        self.button_start.on_click = self.pause

        threads = []
        for thread, tiles in worker_threads:
            t = threading.Thread(target=self.run_with_callback, args=(thread, tiles))
            t.start()
            threads.append(t)

        for thread in threads:
            thread.join()

        self.button_start.on_click = self.start

        for tile in self.tile_manager.controls[1:]:
            tile.paused = False
            tile.stopped = False
            tile.set_text("")

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True
        self.set_text("")

    def run_with_callback(self, task, tiles):
        task.start()
        task.join()

        for tile in tiles:
            tile.paused = False
            tile.stopped = False

    def resume(self, e):
        self.paused = False

        for tile in self.tile_manager.controls[1:]:
            tile.paused = False

        self.button_start.icon = ft.icons.PAUSE
        self.initial_page.update()
        self.button_start.on_click = self.pause

    def pause(self, e):
        self.paused = True

        for tile in self.tile_manager.controls[1:]:
            tile.paused = True

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_start.on_click = self.resume
        self.initial_page.update()

    def stop(self, e):
        self.paused = False
        self.stopped = True

        for tile in self.tile_manager.controls[1:]:
            tile.paused = False
            tile.stopped = True

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True
        self.initial_page.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        self.text_status.update()

    def get_text(self):
        return self.text_status.value

    def add_text(self, phrase: str, color=None):
        self.tile_manager.add_text(phrase, color)

    def add_divider(self):
        self.controls.append(ft.Divider())
        self.initial_page.update()
