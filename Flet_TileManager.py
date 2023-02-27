import json
import shutil
import threading
from os.path import exists
from time import sleep

import flet as ft
import pyautogui

from Flet_Tile import Tile


class NavigationBar(ft.Row):
    def __init__(self, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.tileManager = tile_manager
        self.button_refresh = ft.TextButton(text="Refresh", on_click=lambda _: self.tileManager.refresh())
        self.controls.append(self.button_refresh)

class TileManager(ft.ListView):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.height = 250
        self.expand = 0
        self.tiles:dict[str,Tile] = {}
        self.navigation_bar:NavigationBar = NavigationBar(self)
        self.controls.append(self.navigation_bar)

    def add_tile(self, number: str):
        self.tiles[number] = Tile(self.page, number)
        self.controls.append(self.tiles[number])
        # self.update()

    def delete_tile(self, number: str):
        index = self.controls.index(self.tiles[number])
        self.controls.pop(index)
        del self.tiles[number]
        self.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            try:
                tile.button_select.selected = False
            finally:
                tile.button_select.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def process_is_alive(self):
        while 1:
            for tile in self.tiles.values():
                if not tile.tasks_process.is_alive():
                    tile.started = False
                    tile.stopped = False
                    tile.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
                    tile.button_stop.disabled = True
                    tile.button_start.update()
                    tile.button_stop.update()
                    tile.set_text("")
            sleep(1)

    def update_tiles(self):
        is_alive = threading.Thread(target=self.process_is_alive)
        is_alive.deamon = True
        is_alive.start()

    def get_dic_instances(self):
        try:
            with open('path.json', encoding='utf-8') as config_file:
                path = json.load(config_file)
            string = path["bluestacks"][:-5] + ".txt"
            if exists(rf'{path["bluestacks"]}'):
                string = path["bluestacks"][:-5] + ".txt"
                shutil.copy(rf'{path["bluestacks"]}', rf'{string}')
            with open(rf'{string}', 'r', encoding='utf-8') as file:
                data_instance = file.read().split('\n')
        except:
            raise OSError(
                "The path you provided is wrong ! We are looking for something like : \n r'C:\ProgramData\BlueStacks_nxt\\bluestacks.conf'")

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
        with open("user_settings.json","r") as f:
            data = json.load(f)


        instances = self.get_dic_instances()


        for key in instances:

            if str(key) not in data:
                default_dic = {
                    'instance': instances[str(key)]['instance'],
                    'name': instances[str(key)]['name'],
                    'host': '127.0.0.1',
                    'port': int(instances[str(key)]['port']),
                    'API_KEY': "",
                    'loop_task': False,
                    'time_to_wait_loop1': 60,
                    'time_to_wait_loop2': 110,
                    'leave_game_loop': True,
                    'scheduler': False,
                    'schedules': {}
                }
                for i in range(1, 4):
                    default_dic['schedules'][i] = {
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
                        "First_level": 6,
                        "Second_level": 6,
                        "Third_level": 6,
                        "Fourth_level": 6,
                        "Fifth_level": 6,
                        "Sixth_level": 6,
                        "Seventh_level": 6,
                        "rss_custom_preset": False,
                        'auto_reconnect': True,
                        'auto_captcha': True,
                        'check_donation': False,
                        'use_enhanced_buff': False,
                        'gather_rss': False,
                        'buy_merchant': False,
                        'claim_daily_quests': False,
                        'collect_ressource': False,
                        'defeat_barbarians': False,
                        'barbarians_level': 25,
                        'gather_gem': False,
                        'gem_check1': 60,
                        'gem_check2': 120,
                        'gem_experimental': False,
                        'gather_gem_duration1': 60,
                        'gather_gem_duration2': 90,
                        'restart_game': False,
                        'switch_character': False,
                        'leave_game_switch_character': False,
                        "scout_fog": False,
                        "scout_duration1": 60,
                        "scout_duration2": 90,
                        "scout_building_x": 730,
                        "scout_building_y": 410,
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
                        "alliance_help": False
                    }
                default_dic['schedules'][1]['enabled'] = True
                if str(key) not in data:
                    data[str(key)] = default_dic
                else:
                    for key2 in default_dic:
                        if key2 not in data[str(key)]:
                            data[str(key)][key2] = default_dic[key2]

                    for key2 in default_dic['schedules'][1]:
                        for i in range(1, 4):
                            if key2 not in data[str(key)]['schedules'][str(i)]:
                                data[str(key)]['schedules'][str(i)][key2] = default_dic['schedules'][1][key2]
            else:
                data[str(key)]['instance'] = instances[str(key)]['instance']
                data[str(key)]['name'] = instances[str(key)]['name']
                data[str(key)]['port'] = int(instances[str(key)]['port'])

        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))
        instances = self.get_all_vms_running()
        for i in range(len(self.controls) - 1):
            self.controls.pop()
        for instance in instances:
            if str(instance[0]) in self.tiles:
                self.controls.append(self.tiles[str(instance[0])])
            else:
                self.add_tile(str(instance[0]))
        self.update()
