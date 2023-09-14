import threading

from views.Flet_Frame import Frame
from tasks.Task import Task
import flet as ft

from tasks.Task_runner import TaskRunner
from utils.Task_utils import FileSingleton, get_all_vms_running


class ConfigOverrider(ft.PopupMenuButton):
    def __init__(self, page, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fileSingleton = FileSingleton()
        self.index = index
        self.initial_page = page
        self.config = self.fileSingleton.get_data()[self.index]
        self.init()

    def init(self):
        self.items.append(ft.PopupMenuItem(text="Override Configs"))
        self.items.append(ft.PopupMenuItem())
        for vms in get_all_vms_running():
            if str(vms[0]) != self.index:
                self.items.append(
                    ft.PopupMenuItem(
                        text=vms[1], on_click=self.override_settings, data=vms[0]
                    )
                )

    def update_config(self):
        self.config = self.fileSingleton.get_data()[self.index]

    def refresh(self):
        self.items = []
        self.init()
        self.initial_page.update()

    def override_settings(self, e):
        self.update_config()
        data = self.fileSingleton.get_data()

        instance = data[str(e.control.data)]["instance"]
        name = data[str(e.control.data)]["name"]
        host = data[str(e.control.data)]["host"]
        port = data[str(e.control.data)]["port"]

        data[str(e.control.data)] = self.config

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


class Tile(ft.Row):
    def __init__(self, page, number, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        self.number = number
        self.initial_page = page
        self.paused = False
        self.stopped = False
        self.tasks_process = None
        self.main_task = Task(self)
        self.runner = TaskRunner(self.main_task, self)

        if self.initial_page.UPGRADE:
            self.tasks_process = threading.Thread(target=self.runner.run_update)
        else:
            self.tasks_process = threading.Thread(target=self.runner.run)

        self.button_select = ft.IconButton(
            icon=ft.icons.SETTINGS_OUTLINED,
            selected_icon=ft.icons.SETTINGS,
            on_click=lambda _: self.select()
        )
        self.button_start = ft.IconButton(
            icon=ft.icons.NOT_STARTED_OUTLINED,
            on_click=lambda _: self.start()
        )
        self.button_stop = ft.IconButton(
            icon=ft.icons.STOP_OUTLINED,
            disabled=True,
            on_click=lambda _: self.stop()
        )

        self.config_overrider = ConfigOverrider(self.initial_page, number)
        self.text_name = ft.Text(value=data[str(number)]['name'], width=70)
        self.text_status = ft.Text(value="", width=120)

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.controls.extend([
            ft.Row(
                controls=[
                    self.button_select,
                    self.button_start,
                    self.button_stop,
                    self.text_name,
                    self.text_status,
                ]
            ),
            self.config_overrider
            ]
        )

    def select(self):
        self.initial_page.tile_manager.unselect_all()
        self.button_select.selected = True

        if len(self.initial_page.body.controls) > 2:
            self.initial_page.body.controls.pop()

        if self.number not in self.initial_page.frames:
            self.initial_page.frames[self.number] = Frame(self.initial_page, self.number)

        self.initial_page.body.controls.append(self.initial_page.frames[self.number])
        self.initial_page.update()

    def start(self):
        if not self.tasks_process.is_alive():
            self.button_start.icon = ft.icons.PAUSE
            self.button_stop.disabled = False
            self.paused = False
            self.stopped = False
            self.start_tasks()
        else:
            if self.paused:
                self.button_start.icon = ft.icons.PAUSE
                self.button_stop.disabled = False
                self.paused = False
                self.stopped = False
            else:
                self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
                self.button_stop.disabled = False
                self.paused = True
                self.stopped = False

        self.initial_page.update()

    def process_is_alive(self):
        self.tasks_process.join()
        self.paused = False
        self.stopped = False
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.initial_page.update()
        self.set_text("")

    def start_tasks(self):
        if not self.tasks_process.is_alive():
            if self.initial_page.UPGRADE:
                self.tasks_process = threading.Thread(target=self.runner.run_update)
            else:
                self.tasks_process = threading.Thread(target=self.runner.run)
            self.tasks_process.start()
        else:
            self.add_text("Task is frozen, you may need to restart the bot.")
            self.initial_page.generate_toast('Warning', "Task is frozen, you may need to restart the bot.")
            print("Task is frozen, you may need to restart the bot.")

    def stop(self):
        self.paused = False
        self.stopped = True

        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True

        self.tasks_process = threading.Thread(target=self.runner.run,daemon=True)
        self.initial_page.update()
        self.set_text("")

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
