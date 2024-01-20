from __future__ import annotations

import copy
import threading

import flet as ft

from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from utils.functions import FileSingleton, get_all_vms_running, get_all_vms_running_ld
from utils.singletons import EmulatorSingleton
from views.tiles.handler.config_handler import Frame


class ConfigOverrider(ft.PopupMenuButton):
    def __init__(self, page, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fileSingleton = FileSingleton()
        self.index = index
        self.initial_page = page
        self.config = self.fileSingleton.getCachedData()[self.index]
        self.icon = ft.icons.FILE_UPLOAD_OUTLINED
        self.init()

    def init(self):
        self.items.append(ft.PopupMenuItem(text="Export Config"))
        self.items.append(ft.PopupMenuItem())

        vms = self.initial_page.tile_manager.fetched_instances

        for vm in vms:
            if str(vm) != self.index:
                self.items.append(ft.PopupMenuItem(text=vms[vm]['name'], on_click=self.override_settings, data=vm))

    def refresh(self):
        self.items = []
        self.init()
        self.initial_page.update()

    def override_settings(self, e):
        data = self.fileSingleton.getCachedData()
        self.config = copy.deepcopy(data[self.index])

        instance = data[str(e.control.data)]["instance"]
        name = data[str(e.control.data)]["name"]
        host = data[str(e.control.data)]["host"]
        port = data[str(e.control.data)]["port"]

        data[str(e.control.data)] = copy.deepcopy(self.config)

        data[str(e.control.data)]["instance"] = instance
        data[str(e.control.data)]["name"] = name
        data[str(e.control.data)]["host"] = host
        data[str(e.control.data)]["port"] = port

        self.fileSingleton.write_data(data)

        if str(e.control.data) in self.initial_page.frames:
            for tab in self.initial_page.frames[str(e.control.data)].settings.tabs:
                tab.content.content.controls = []
                tab.content.init()
        self.initial_page.update()


class Tile(ft.Container):
    def __init__(self, page, number, **kwargs):
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

        if self.initial_page.UPGRADE:
            self.tasks_process = threading.Thread(target=self.runner.run_update)
        else:
            self.tasks_process = threading.Thread(target=self.runner.run)

        self.button_select = ft.IconButton(
            icon=ft.icons.SETTINGS,
            selected_icon=ft.icons.SETTINGS,
            on_click=self.select,
        )
        self.button_start = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED, on_click=self.start)
        self.button_stop = ft.IconButton(icon=ft.icons.HIGHLIGHT_REMOVE_ROUNDED, disabled=True, on_click=self.stop)

        self.config_overrider = ConfigOverrider(self.initial_page, number)
        self.text_name = ft.Text(value=data[str(number)]["name"], width=80)
        self.text_status = ft.Text(value="", width=120)

        self.border_radius = 3
        self.bgcolor = ft.colors.SURFACE
        self.on_click = self.select
        self.on_hover = self.hover

        self.content = ft.Row(
            [
                ft.Row(
                    controls=[
                        # self.button_select,
                        self.button_start,
                        self.button_stop,
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
        self.button_select.selected = True

        if len(self.initial_page.body.controls) > 2:
            self.initial_page.body.controls.pop()

        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.body.controls.append(self.initial_page.frames[self.number])
        self.bgcolor = ft.colors.SURFACE_VARIANT
        self.initial_page.update()

    def start(self, e):
        self.button_start.icon = ft.icons.PAUSE
        self.button_stop.disabled = False

        self.paused = False
        self.stopped = False

        self.start_tasks()
        self.button_start.on_click = self.pause
        self.tasks_process.join()
        self.button_start.on_click = self.start
        self.paused = False
        self.stopped = False
        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True
        self.set_text("")

    def resume(self, e):
        self.paused = False

        self.button_start.icon = ft.icons.PAUSE
        self.initial_page.update()
        self.button_start.on_click = self.pause

    def pause(self, e):
        self.paused = True

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_start.on_click = self.resume
        self.initial_page.update()

    def stop(self, e):
        self.paused = False
        self.stopped = True
        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True
        self.initial_page.update()

    def start_tasks(self):
        if not self.tasks_process.is_alive():
            if self.initial_page.UPGRADE:
                self.tasks_process = threading.Thread(target=self.runner.run_update)
            else:
                self.tasks_process = threading.Thread(target=self.runner.run)
            self.tasks_process.start()
        else:
            self.add_text("Task is frozen, you may need to restart the bot.")
            self.initial_page.generate_toast("Warning", "Task is frozen, you may need to restart the bot.")
            print("Task is frozen, you may need to restart the bot.")

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
