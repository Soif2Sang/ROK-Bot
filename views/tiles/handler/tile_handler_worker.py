import os
import platform
import re
from time import sleep

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from utils.context import contextManager
from utils.schemas.emulator_schemas import EmulatorSettingsSchema, ProfileSchema
from utils.schemas.worker_schemas import InstanceSchema, WorkerListSchema, WorkerSettingsSchema, WorkerTypeSchema

from utils.constants import VERSION_TYPE
from utils.flet_translations import translate
from utils.functions import get_dic_instances_ld, MacConfigParser, BluestacksConfigParser, \
    LdplayerConfigParser, PcConfigParser, find_file_in_all_drives, Ldplayer5ConfigParser
from utils.singletons import EmulatorSingleton, FileSingleton, SettingsSingleton, ss
from views.login.login import ClickableLink, links, sellix_icon, stripe_icon, tiers
from views.tiles.tile_worker import TileWorker
import shortuuid


class NavigationBar(ft.Row):
    def __init__(self, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.tileManager = tile_manager
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN

        self.button_refresh = ft.IconButton(
            icon=ft.icons.REFRESH_ROUNDED,
            on_click=lambda _: self.tileManager.refresh(),
            style=ButtonStyle(
                shape={
                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                },
                bgcolor=ft.colors.SURFACE_VARIANT,
            ),
        )

        stripe_col = ft.Column(col=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
        sellix_col = ft.Column(col=6, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

        for tier in links["stripe"]:
            stripe_col.controls.append(ClickableLink("Stipe Paywall", links["stripe"][tier], stripe_icon))
        for tier in links["sellix"]:
            sellix_col.controls.append(ClickableLink("Crypto Paywall", links["sellix"][tier], sellix_icon))

        diag = ft.AlertDialog(
            content=ft.Column(
                controls=[
                    ft.Text("Where to subscribe", size=20, color=ft.colors.GREY_700, weight=ft.FontWeight.W_400),
                    ft.ResponsiveRow(controls=[stripe_col, sellix_col]),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                height=100,
                width=370,
            ),
        )

        pattern = r"(\d+) Days left"
        match = re.search(pattern, ss.page.title)
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

        refresh_pay = ft.Row(controls=[self.button_refresh])

        def open_dlg(e):
            ss.page.dialog = diag
            diag.open = True
            ss.page.update()

        if VERSION_TYPE == "global":
            refresh_pay.controls.append(
                ft.OutlinedButton(
                    text="Renew",
                    icon=ft.icons.SHOPPING_CART_OUTLINED,
                    on_click=open_dlg,
                    style=button_style,
                )
            )
        self.controls.append(refresh_pay)
        self.controls.append(
            ft.IconButton(
                icon=ft.icons.MENU,
                on_click=lambda _: ss.page.go("/settings"),
            ),
        )


class TileHandlerWorker(ft.ListView):
    _instance = None
    initialized = False

    def __new__(cls, **kwargs):
        if cls._instance is None:
            cls._instance = super(TileHandlerWorker, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        # Check if the instance is already initialized
        if not hasattr(self, 'initialized') or not self.initialized:
            super().__init__(**kwargs)
            self.height = 300
            self.expand = 0
            self.spacing = 1
            self.FileSingleton = FileSingleton()
            self.tiles: dict[str, TileWorker] = {}
            self.navigation_bar: NavigationBar = NavigationBar(self)
            self.controls.append(self.navigation_bar)
            self.initialized = True

    def add_tile(self, number: str):
        if number not in self.tiles:
            self.tiles[number] = TileWorker(number)
            contextManager.add_worker(number, self.tiles[number])
        else:
            self.tiles[number].refresh_tile()

        self.controls.append(self.tiles[number])

        ss.page.update()

    def delete_tile(self, number: str):
        self.controls.remove(self.tiles[number])
        self.tiles.pop(number)
        ss.page.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            if isinstance(tile, TileWorker):
                # tile.button_select.selected = False
                for control in tile.controls:
                    control.bgcolor = ft.colors.SURFACE
        ss.page.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def refresh(self):
        ss = SettingsSingleton()

        instances = {}


        if ss.application_settings.paths.ldplayer.ldconsole:
            instances.update(LdplayerConfigParser().getConfig())
            ss.application_settings.paths.adb = ss.application_settings.paths.ldplayer.ldconsole.replace('ldconsole', 'adb')

        if ss.application_settings.paths.ldplayer5.ldconsole:
            print(ss.application_settings.paths.ldplayer5.ldconsole)
            instances.update(Ldplayer5ConfigParser().getConfig())



            ss.application_settings.paths.adb = ss.application_settings.paths.ldplayer5.ldconsole.replace('ldconsole', 'adb')

        print(LdplayerConfigParser().getConfig())
        print(Ldplayer5ConfigParser().getConfig())

        # if platform.system() == "Darwin":
        #     instances = MacConfigParser().getConfig()
        # elif emulator == "bluestacks":
        #     instances = BluestacksConfigParser().getConfig()
        # elif emulator == "ld":
        #     instances = LdplayerConfigParser().getConfig()
        # else:
        #     instances = PcConfigParser().getConfig()



        self.fetched_instances = instances

        worker_settings = ss.worker_settings


        for i, instance in enumerate(instances):
            unique_key = instances[instance]['emulator'] + '-' +instances[instance]["instance"]
            if instances[instance]["instance"] not in worker_settings.workers:
                worker_settings.workers[unique_key] = WorkerSettingsSchema(name=len(worker_settings.workers),instances=[InstanceSchema(instance=instance)])

            if instance not in ss.emulator_settings.emulators:
                ss.emulator_settings.emulators[unique_key] = EmulatorSettingsSchema(
                    emulator=instances[instance]['emulator'],
                    instance=unique_key,
                    name=instances[instance]["name"],
                    port=int(instances[instance]["port"]),
                )

                ss.emulator_settings.emulators[unique_key].schedules["1"].enabled = True
            else:
                ss.emulator_settings.emulators[unique_key].instance = unique_key
                ss.emulator_settings.emulators[unique_key].name = instances[instance]["name"]
                ss.emulator_settings.emulators[unique_key].port = int(instances[instance]["port"])

        ss.write_application_settings(ss.application_settings)
        ss.write_emulator_settings(ss.emulator_settings)
        ss.write_worker_settings(worker_settings)

        for i in range(len(self.controls) - 1):
            self.controls.pop()

        if instances:
            for worker in worker_settings.workers:
                if worker_settings.workers[worker].instances:
                    self.add_tile(worker)

        return ss.page.update()

        if instances:
            for instance in instances:
                if str(instance[0]) in self.tiles:
                    self.controls.append(self.tiles[str(instance[0])])
                    self.tiles[str(instance[0])].main_task.adb.update_port()
                    self.tiles[str(instance[0])].runner.adb.update_port()
                else:
                    self.add_tile(str(instance[0]))
                    # self.controls.append(ft.Divider(height=1, color="grey", opacity=0.5))
                self.tiles[str(instance[0])].config_overrider.items = []
                self.tiles[str(instance[0])].config_overrider.refresh()
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

        # self.padding = ft.padding.only(top=15, left=0, bottom=0)
