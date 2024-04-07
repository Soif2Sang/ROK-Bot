import copy
import re

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from utils.constants import (VERSION_TYPE, default_dic, default_profile,
                             default_worker_settings)
from utils.flet_translations import translate
from utils.functions import (get_all_vms_running, get_all_vms_running_ld,
                             get_dic_instances, get_dic_instances_ld)
from utils.singletons import EmulatorSingleton, FileSingleton
from views.tiles.handler.tile_handler_worker import NavigationBar
from views.tiles.tile import Tile


class TileHandlerPC(ft.ListView):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.height = 250
        self.expand = 0
        self.spacing = 5
        self.FileSingleton = FileSingleton()
        self.tiles: dict[str, Tile] = {}
        self.navigation_bar: NavigationBar = NavigationBar(self.initial_page, self)
        self.controls.append(self.navigation_bar)

    def add_tile(self, number: str):
        self.tiles[number] = Tile(self.initial_page, number)
        self.controls.append(self.tiles[number])
        self.initial_page.update()

    def delete_tile(self, number: str):
        self.controls.remove(self.tiles[number])
        self.tiles.pop(number)
        self.initial_page.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            if isinstance(tile, Tile):
                # tile.button_select.selected = False
                tile.bgcolor = ft.colors.SURFACE
        self.initial_page.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def refresh(self):
        data = self.FileSingleton.get_data()

        emulator = EmulatorSingleton().getEmulator()

        instances = {"pc": {'name': 'pc', 'instance': 'pc', 'port': -1}}

        self.fetched_instances = instances

        default_dic["emulator"] = emulator

        for i in range(1, 4):
            default_dic["schedules"][i] = copy.deepcopy(default_profile)
        default_dic["schedules"][1]["enabled"] = True

        for i, instance in enumerate(instances):
            if str(i) not in data["workers"][emulator]:
                data["workers"][emulator][str(i)] = {**default_worker_settings, "instances": [{"instance": instance}]}
            else:
                data["workers"][emulator][str(i)] = {**default_worker_settings, **data["workers"][emulator][str(i)]}

            if instance not in data:
                data[instance] = copy.deepcopy(default_dic)
            else:
                for key in default_dic:
                    if key not in data[instance]:
                        data[instance][key] = copy.deepcopy(default_dic[key])

                for key in default_profile:
                    for i in range(1, 4):
                        if key not in data[instance]["schedules"][str(i)]:
                            data[instance]["schedules"][str(i)][key] = copy.deepcopy(default_profile[key])

            data[instance].update({
                "instance": instances[instance]["instance"],
                "name": instances[instance]["name"],
                "port": int(instances[instance]["port"])
            })

        self.FileSingleton.write_data(data)

        if emulator == "bluestacks":
            instances = get_all_vms_running()
        elif emulator == "pc":
            instances = [["pc", "pc"]]
        else:
            instances = get_all_vms_running_ld()

        for i in range(len(self.controls) - 1):
            self.controls.pop()


        return self.add_tile("pc")
        if instances:
            for instance in instances:
                if str(instance[0]) in self.tiles:
                    self.controls.append(self.tiles[str(instance[0])])
                    # self.tiles[str(instance[0])].main_task.adb.update_port()
                    # self.tiles[str(instance[0])].runner.adb.update_port()
                else:
                    self.add_tile(str(instance[0]))
                    # self.controls.append(ft.Divider(height=1, color="grey", opacity=0.5))
                # self.tiles[str(instance[0])].config_overrider.items = []
                # self.tiles[str(instance[0])].config_overrider.refresh()
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

        # self.initial_page.update()
        self.initial_page.update()

        # self.padding = ft.padding.only(top=15, left=0, bottom=0)
