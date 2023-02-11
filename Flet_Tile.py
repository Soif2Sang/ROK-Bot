import json
import threading
from time import sleep

from Flet_Frame import Frame
from Task import Task
import flet as ft

from Task_runner import TaskRunner

class Tile(ft.Row):
    def __init__(self, page, number, **kwargs):
        super().__init__(**kwargs)

        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        self.page = page
        self.number = number

        self.started = False
        self.stopped = False
        self.tasks_process = None
        self.main_task = Task(self)
        self.runner = TaskRunner(self.main_task, self)
        self.tasks_process = threading.Thread(target=self.runner.run)

        self.button_select = ft.IconButton(
            icon=ft.icons.PAGEVIEW,
            selected_icon=ft.icons.REMOVE_RED_EYE_OUTLINED,
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
        self.text_name = ft.Text(value=data[str(number)]['name'], width=70)
        self.text_status = ft.Text(value="Active")

        self.controls.extend([
            self.button_select,
            self.button_start,
            self.button_stop,
            self.text_name,
            self.text_status,
        ]
        )

    def select(self):
        self.page.tile_manager.unselect_all()
        self.button_select.selected = True
        self.button_select.update()

        if self.page.frames == {}:
            print("Frame empty")
            self.page.frames[self.number] = Frame(self.page, self.number)
            self.page.add(self.page.frames[self.number])
            self.page.update()
        else:
            print(f"{len(self.page.controls)>2 =}")
            if len(self.page.controls)>2:
                self.page.controls.pop()
            if self.number not in self.page.frames:
                self.page.frames[self.number] = Frame(self.page, self.number)
            self.page.add(self.page.frames[self.number])
            self.page.update()

    def start(self):
        self.started = not self.started
        if self.started:
            self.button_start.icon = ft.icons.PAUSE
            self.button_stop.disabled = False
        else:
            self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
            self.button_stop.disabled = True
        self.start_tasks()
        self.update()

    def process_is_alive(self):
        while True:
            if not self.tasks_process.is_alive():
                self.started = False
                self.stopped = False
                self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
                self.button_stop.disabled = True
                self.page.update()
                return self.set_text("")
            sleep(1)

    def start_tasks(self):
        # print(f"{self.tasks_process.is_alive() = }")
        if not self.tasks_process.is_alive():
            self.tasks_process = threading.Thread(target=self.runner.run)
            self.tasks_process.daemon = True
            self.tasks_process.start()
            # asyncio.create_task(run(self.runner.run))
            is_alive = threading.Thread(target=self.process_is_alive)
            is_alive.deamon = True
            is_alive.start()
        else:
            print("Task is running")

    def stop(self):
        self.started = False
        self.stopped = True
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.set_text("")
        self.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        self.update()

    def add_text(self, phrase: str, color = "black"):
        # print(self.page.frames)
        if self.number not in self.page.frames:
            self.page.frames[self.number] = Frame(self.page, self.number)
        self.page.frames[self.number].logger.add_text(phrase, color)
        self.page.update()

    def set_timer(self, seconds:int):
        threading.Thread(target=self.set_timer2, args=(seconds))

    def set_timer2(self, seconds: int):
        condition = True
        while seconds and condition:
            hours, mins = divmod(seconds, 3600)
            mins, secs = divmod(mins, 60)
            self.set_text(f"{hours:02d}:{mins:02d}:{secs:02d}")
            seconds -= 1
            condition = ":" in self.text_status.value
            sleep(1)
