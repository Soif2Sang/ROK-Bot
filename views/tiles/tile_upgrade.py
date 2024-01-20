from __future__ import annotations

from time import sleep

import flet as ft

from utils.singletons import EmulatorSingleton
from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from views.tiles.handler.config_handler import FrameUpgrade, Frame
from views.tiles.tile import ConfigOverrider

from utils.functions import FileSingleton


class TileUpgrade(ft.Container):
    def __init__(self, page, number:str, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.getCachedData()
        self.number = number
        self.initial_page = page
        self.tasks_process = None
        self.paused = False
        self.stopped = False

        self.main_task = Task(self)
        self.runner = TaskRunner(self.main_task, self)

        self.tile_manager = self.initial_page.tile_manager
        self.selected = False

        self.button_select = ft.IconButton(
            icon=ft.icons.SETTINGS,
            selected_icon=ft.icons.SETTINGS,
            on_click=self.select,
        )

        # self.enable_switch = ft.Switch(on_change=lambda _: self.change(), value=False)
        self.enable_switch = ft.Checkbox(on_change=lambda _: self.change(), value=False)

        self.config_overrider = ConfigOverrider(self.initial_page, number)
        self.text_name = ft.Text(value=data[str(number)]["name"], width=150)
        self.text_status = ft.Text(value="", width=160)

        # self.vertical_alignment = ft.CrossAxisAlignment.CENTER
        # self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        # self.controls.extend(
        #     [
        #         ft.Row(controls=[self.button_select, self.enable_switch, self.text_name, self.text_status]),
        #         self.config_overrider,
        #     ]
        # )

        self.border_radius = 3
        self.bgcolor = ft.colors.SURFACE
        self.on_click = self.select
        self.on_hover = self.hover

        self.content = ft.Row(
            controls=[
                ft.Row(controls=[self.enable_switch, self.text_name, self.text_status]),
                self.config_overrider,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )
    def long_press(self, e):
        self.enable_switch = not self.enable_switch
        self.selected = not self.selected
        self.initial_page.update()

    def change(self):
        self.selected = not self.selected
        #
        # limit = EmulatorSingleton().getEmulatorLimit()
        #
        # if len(self.initial_page.tile_manager.get_enabled_sel_object()) >= limit:
        #     self.initial_page.tile_manager.disable_all_unselected_tiles()
        # else:
        #     self.initial_page.tile_manager.enable_all_unselected_tiles()

    def hover(self, e):
        e.control.bgcolor = (
            ft.colors.SURFACE_VARIANT
            if (e.data == "true" or self.initial_page.body.controls[-1] == self.initial_page.frames.get(self.number, False))
            else ft.colors.SURFACE
        )
        self.initial_page.update()

    def select(self, e):
        self.initial_page.tile_manager.unselect_all()
        self.button_select.selected = True

        if len(self.initial_page.body.controls) > 3:
            self.initial_page.body.controls.pop()

        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.body.controls.append(self.initial_page.frames[self.number])
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.initial_page.update()

    def get_enabled_sel(self):
        return self.tile_manager.get_enabled_sel()

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

    def get_enabled_sel_object(self):
        return self.tile_manager.get_enabled_sel_object()
