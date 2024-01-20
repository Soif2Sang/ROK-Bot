import copy
import threading

import flet as ft

from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from views.tiles.tile import ConfigOverrider
from utils.functions import FileSingleton, get_all_vms_running, get_all_vms_running_ld
from utils.singletons import EmulatorSingleton
from views.tiles.handler.config_handler import Frame

class TileSlave(ft.Container):
    def __init__(self, page, number, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.getCachedData()
        self.number = number
        self.initial_page = page
        self.padding = ft.padding.only(left=10)
        self.margin = ft.margin.only(bottom=3, left=15)
        self.text_name = ft.Text(value=data[str(number)]["name"], width=80)
        self.text_status = ft.Text(value="")
        self.config_overrider = ConfigOverrider(self.initial_page, number)

        self.border_radius = 3
        self.bgcolor = ft.colors.SURFACE
        self.on_click = self.select
        self.on_hover = self.hover

        self.content = ft.Row(
            [
                ft.Row(
                    controls=[
                        self.text_name,
                        self.text_status,
                    ]
                ),
                self.config_overrider,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def hover(self, e):
        e.control.bgcolor = (
            ft.colors.SURFACE_VARIANT
            if (e.data == "true" or self.initial_page.body.controls[-1] == self.initial_page.frames.get(self.number, False))
            else ft.colors.SURFACE
        )
        self.initial_page.update()

    def select(self, e):
        self.initial_page.tile_manager.unselect_all()

        if len(self.initial_page.body.controls) > 2:
            self.initial_page.body.controls.pop()

        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.body.controls.append(self.initial_page.frames[self.number])
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.initial_page.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        self.initial_page.update()

    def get_text(self):
        return self.text_status.value

    def add_text(self, phrase: str, color=None):
        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.frames[self.number].add_text(phrase, color)

    def add_divider(self):
        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.frames[self.number].add_divider()
