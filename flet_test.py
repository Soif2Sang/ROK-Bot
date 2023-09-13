from time import sleep

import flet as ft

from Flet_TileManager import NavigationBar, TileManager
from utils.Task_utils import get_all_vms_running, FileSingleton

print(get_all_vms_running())

class ConfigOverrider(ft.PopupMenuButton):
    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fileSingleton = FileSingleton()
        self.index = index
        self.config = self.fileSingleton.get_data()[self.index]

    def init(self):
        self.clean()
        self.items.append(ft.PopupMenuItem(text="Override Configs"))
        self.items.append(ft.PopupMenuItem())
        for vms in get_all_vms_running():
            self.items.append(
                ft.PopupMenuItem(
                    text=vms[1], on_click=self.override_settings, data=vms[0]
                )
            )

    def update_config(self):
        self.config = self.fileSingleton.get_data()[self.index]

    def refresh(self):
        self.init()
        self.update()

    def override_settings(self, e):
        self.update_config()
        data = self.fileSingleton.get_data()

        instance = data["instance"]
        name = data["name"]
        host = data["host"]
        port = data["port"]

        data[str(e.control.data)] = self.config

        data[str(e.control.data)]["instance"] = instance
        data[str(e.control.data)]["name"] = name
        data[str(e.control.data)]["host"] = host
        data[str(e.control.data)]["port"] = port

        self.fileSingleton.write_data(data)


def main(page: ft.Page):
    def check_item_clicked(e):
        e.control.text += " ✓"
        e.control.update()
        sleep(1)
        e.control.text = e.control.text[:-2]
        e.control.update()



    pb = ft.PopupMenuButton(
    )
    pb.items.append(ft.PopupMenuItem(text="Override Configs"))
    pb.items.append(ft.PopupMenuItem())

    for vms in get_all_vms_running():
        pb.items.append(
            ft.PopupMenuItem(
                text=vms[1], on_click=check_item_clicked,
            )
        )
    cfg = ConfigOverrider("0")
    page.add(cfg)
    cfg.init()
    page.update()

class NavigationBar2(NavigationBar):
    def __init__(self, tile_manager, **kwargs):
        super().__init__(tile_manager, **kwargs)
        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.controls.append(
            ft.PopupMenuButton(
                icon=ft.icons.ADD_SHOPPING_CART,
                items=[
                    ft.PopupMenuItem(
                        content=ft.Row(
                            [
                                ft.Icon(ft.icons.LINK),
                                ft.Text("Pay with Stripe"),
                            ]
                        ),
                        on_click=lambda _: self.page.launch_url("https://buy.stripe.com/dR66oX4ov0qldkQaEF"),
                    ),
                    ft.PopupMenuItem(
                        content=ft.Row(
                            [
                                ft.Icon(ft.icons.LINK),
                                ft.Text("Pay with Cryptos"),
                            ]
                        ),
                        on_click=lambda _:  self.page.launch_url("https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099"),
                    ),
                ]
            )
        )

def main(page: ft.Page):
    page.UPGRADE = True
    page.add(NavigationBar2(TileManager(page)))
ft.app(target=main)