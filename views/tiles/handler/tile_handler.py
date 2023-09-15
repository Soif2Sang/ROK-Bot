import threading
from time import sleep

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from tiles.tile import Tile
from utils.Task_utils import FileSingleton, get_all_vms_running, get_dic_instances
import re
class NavigationBar(ft.Row):
    def __init__(self, page, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.tileManager = tile_manager
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.button_refresh = ft.OutlinedButton(text="Refresh", icon=ft.icons.REFRESH_ROUNDED,
                                                on_click=lambda _: self.tileManager.refresh(), style=ButtonStyle(shape={
                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
            }, bgcolor=None if not self.tileManager.initial_page.UPGRADE else ft.colors.AMBER_100)
                                                )

        self.controls.append(self.button_refresh)

        # self.controls.append(
        #     ft.PopupMenuButton(
        #         tooltip="Extend my account",
        #         icon=ft.icons.ADD_SHOPPING_CART_ROUNDED,
        #         items=[
        #             ft.PopupMenuItem(
        #                 content=ft.Row(
        #                     [
        #                         ft.Icon(ft.icons.LINK),
        #                         ft.Text("Pay with Stripe"),
        #                     ]
        #                 ),
        #                 on_click=lambda _: self.initial_page.launch_url("https://buy.stripe.com/dR66oX4ov0qldkQaEF"),
        #             ),
        #             ft.PopupMenuItem(
        #                 content=ft.Row(
        #                     [
        #                         ft.Icon(ft.icons.LINK),
        #                         ft.Text("Pay with Cryptos"),
        #                     ]
        #                 ),
        #                 on_click=lambda _: self.initial_page.launch_url(
        #                     "https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099"),
        #             ),
        #         ]
        #     )
        # )

        def close_banner(e):
            page.banner.open = False
            page.update()

        page.banner = ft.Banner(
            bgcolor=ft.colors.WHITE30,
            content=ft.Column(controls=[
                ft.TextButton(icon=ft.icons.LINK_OUTLINED, text="Pay with Stripe",
                              on_click=lambda _: page.launch_url("https://buy.stripe.com/dR66oX4ov0qldkQaEF"),
                              ),
                ft.TextButton(icon=ft.icons.LINK_OUTLINED, text="Pay with Crypto",
                              on_click=lambda _: page.launch_url("https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099"))

            ]),
            actions=[
                ft.TextButton("Close", on_click=close_banner),
            ],
            content_padding=ft.padding.all(5)
        )

        def show_banner_click(e):
            page.banner.open = True
            page.update()

        pattern = r'(\d+) Days left'
        match = re.search(pattern, page.title)
        days_left_str = match.group(1)

        days_left_int = int(days_left_str)

        if days_left_int > 10:
            button_style = ButtonStyle(shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                                       bgcolor=ft.colors.GREEN_100, color="black")
        elif 10 >= days_left_int > 5:
            button_style = ButtonStyle(shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                                       bgcolor=ft.colors.ORANGE_300, color="black")
        else:
            button_style = ButtonStyle(shape={ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5)},
                                       bgcolor=ft.colors.RED_200, color="black")

        self.controls.append(ft.OutlinedButton(text="Renew", icon=ft.icons.SHOPPING_CART_OUTLINED,
                                               on_click=show_banner_click, style=button_style))

class TileHandler(ft.ListView):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.height = 250
        self.expand = 0
        self.FileSingleton = FileSingleton()
        self.tiles: dict[str, Tile] = {}
        self.navigation_bar: NavigationBar = NavigationBar(self.initial_page, self)
        self.controls.append(self.navigation_bar)

    def update(self):
        self.initial_page.update()

    def add_tile(self, number: str):
        self.tiles[number] = Tile(self.initial_page, number)
        self.controls.append(self.tiles[number])
        self.update()

    def delete_tile(self, number: str):
        # index = self.controls.index(self.tiles[number])
        self.controls.remove(self.tiles[number])
        self.tiles.pop(number)
        self.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            tile.button_select.selected = False
        self.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def process_is_alive(self):
        while 1:
            changed = False
            for tile in self.tiles.values():
                if (not tile.tasks_process.is_alive() and tile.button_start.icon == ft.icons.PAUSE) and (self.initial_page is not None) and (self.initial_page.route == '/'):
                    tile.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
                    tile.button_stop.disabled = True
                    tile.set_text("")
                    changed = True
            sleep(0.1)
            if changed and self.initial_page is not None:
                self.initial_page.update()

    def update_tiles(self):
        is_alive = threading.Thread(target=self.process_is_alive)
        is_alive.deamon = True
        is_alive.start()

    def refresh(self):
        data = self.FileSingleton.get_data()
        # try:
        #     default_config = self.FileSingleton.get_default_config()
        #     default_config_here = True
        # except:
        #     print("There is no default profile")
        #     default_config_here = False
        instances = get_dic_instances()

        default_dic = {
            'instance': "",
            'name': "",
            'host': '127.0.0.1',
            'port': 0,
            'API_KEY': "",
            'loop_task': False,
            'time_to_wait_loop1': 60,
            'time_to_wait_loop2': 110,
            'leave_game_loop': True,
            'scheduler': False,
            'schedules': {}
        }
        default_profile = {
            'timing': [],
            'enable_timing': False,
            'enabled': False,
            'kingdom': 0,
            'city_x': 0,
            'city_y': 0,
            'radius': 30,
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
            'auto_reconnect': True,
            'auto_captcha': True,
            'check_donation': False,
            'gather_alliance_pit': False,
            'use_enhanced_buff': False,
            'gather_rss': False,
            'buy_merchant': False,
            'claim_daily_quests': False,
            'collect_ressource': False,
            'defeat_barbarians': False,
            'barbarians_level': 25,
            'barbarians_preset': {"1":False,
                                  "2":False,
                                  "3":False,
                                  "4":False,
                                  "5":False,
                                  "6":False,
                                  "7":False,
                                  },
            'gather_gem': False,
            'gem_check1': 60,
            'gem_check2': 120,
            'gem_experimental': False,
            'recenter_feature': True,
            'gather_gem_duration1': 60,
            'gather_gem_duration2': 90,
            'gather_gem_spiral_method': True,
            'gather_gem_swipe_check': True,
            'gather_gem_compare_march_duration': True,
            'restart_game': False,
            'switch_character': False,
            'leave_game_switch_character': False,
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
            "rally_type": 'cav',
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
            "upgrade_city":False,
            "kill_marauders" : False,
            "kill_marauders_duration" : [30,90],
            "rally_skip_back" :  False,
            "gather_rss_method": False,
            "fast_rss_transfer": False
        }

        for i in range(1, 4):
            default_dic['schedules'][i] = default_profile
        default_dic['schedules'][1]['enabled'] = True

        for instance in instances:
            if str(instance) not in data:
                print("Default config set !")
                data[str(instance)] = default_dic
            else:
                for key in default_dic:
                    if key not in data[str(instance)]:
                        data[str(instance)][key] = default_dic[key]
                for key in default_profile:
                    for i in range(1, 4):
                        if key not in data[str(instance)]['schedules'][str(i)]:
                            data[str(instance)]['schedules'][str(i)][key] = default_profile[key]

            data[str(instance)]['instance'] = instances[str(instance)]['instance']
            data[str(instance)]['name'] = instances[str(instance)]['name']
            data[str(instance)]['port'] = int(instances[str(instance)]['port'])

        self.FileSingleton.write_data(data)
        instances = get_all_vms_running()
        for i in range(len(self.controls) - 1):
            self.controls.pop()
        for instance in instances:
            if str(instance[0]) in self.tiles:
                self.controls.append(self.tiles[str(instance[0])])
                self.tiles[str(instance[0])].main_task.adb.update_port()
                self.tiles[str(instance[0])].runner.adb.update_port()
            else:
                self.add_tile(str(instance[0]))
            self.tiles[str(instance[0])].config_overrider.items = []
            self.tiles[str(instance[0])].config_overrider.refresh()
        self.update()
