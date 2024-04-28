import copy
import platform
import re

import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from utils.constants import VERSION_TYPE, default_dic, default_profile, default_worker_settings
from utils.flet_translations import translate
from utils.functions import get_dic_instances, get_dic_instances_ld
from utils.singletons import EmulatorSingleton, FileSingleton
from views.login.login import ClickableLink, links, sellix_icon, stripe_icon, tiers
from views.tiles.tile_worker import TileWorker


class NavigationBar(ft.Row):
    def __init__(self, page, tile_manager, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
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

        refresh_pay = ft.Row(controls=[self.button_refresh])

        def open_dlg(e):
            page.dialog = diag
            diag.open = True
            page.update()

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
                on_click=lambda _: self.initial_page.go("/settings"),
            ),
        )


class TileHandlerWorker(ft.ListView):
    def __init__(self, page: ft.Page, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.height = 300
        self.expand = 0
        self.spacing = 1
        self.FileSingleton = FileSingleton()
        self.tiles: dict[str, TileWorker] = {}
        self.navigation_bar: NavigationBar = NavigationBar(self.initial_page, self)
        self.controls.append(self.navigation_bar)

    def add_tile(self, number: str):
        if number not in self.tiles:
            self.tiles[number] = TileWorker(self.initial_page, number)
        else:
            self.tiles[number].refresh_tile()

        self.controls.append(self.tiles[number])
        self.initial_page.update()

    def delete_tile(self, number: str):
        self.controls.remove(self.tiles[number])
        self.tiles.pop(number)
        self.initial_page.update()

    def unselect_all(self):
        for tile in self.controls[1:]:
            if isinstance(tile, TileWorker):
                # tile.button_select.selected = False
                for control in tile.controls:
                    control.bgcolor = ft.colors.SURFACE
        self.initial_page.update()

    def set_status(self, number: str, phrase: str):
        self.tiles[number].set_text(phrase)

    def refresh(self):
        data = self.FileSingleton.get_data()

        emulator = EmulatorSingleton().getEmulator()

        if platform.system() == "Darwin":
            instances = {"pc": {'name': 'pc', 'instance': 'pc', 'port': -1}}
        elif emulator == "bluestacks":
            instances = get_dic_instances()
        elif emulator == "ld":
            instances = get_dic_instances_ld()
        else:
            instances = {"pc": {"name": "pc", "instance": "pc", "port": -1}}

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

            data[instance].update(
                {"instance": instances[instance]["instance"], "name": instances[instance]["name"], "port": int(instances[instance]["port"])}
            )

        self.FileSingleton.write_data(data)

        for i in range(len(self.controls) - 1):
            self.controls.pop()

        if instances:
            for worker in data["workers"][emulator]:
                if data["workers"][emulator][worker]["instances"]:
                    self.add_tile(worker)

        self.initial_page.update()
        return
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
