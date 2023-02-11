import json
import shutil
from os.path import exists

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
        self.tiles = {}
        self.navigation_bar = NavigationBar(self)
        self.controls.append(self.navigation_bar)

    def add_tile(self, number: str):
        self.tiles[number] = Tile(self.page, number)
        self.controls.append(self.tiles[number])
        self.update()

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
                "The path you provided is wrong ! We are looking for something like : \n r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'")

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
            if str(instance[0]) in self.tiles:
                self.controls.append(self.tiles[str(instance[0])])
            else:
                self.add_tile(str(instance[0]))
        self.update()
