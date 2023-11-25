import threading

import flet as ft

from taskscod.COD_Task import Task
from taskscod.COD_Task_runner import TaskRunner
from utils.functions import FileSingleton
from viewscod.Flet_Frame_cod import Frame


class Tile(ft.Row):
    def __init__(self, page, number, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()

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
        self.text_status = ft.Text(value="")

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
        # print(f"{len(self.page.controls)>2 =}")
        if len(self.page.controls)>2:
            self.page.controls.pop()
        if self.number not in self.page.frames:
            self.page.frames[self.number] = Frame(self.page, self.number)
        self.page.add(self.page.frames[self.number])
        # self.page.title = f"{time()}"
        self.page.update()

    def start(self):
        self.started = not self.started
        self.stopped = False
        if self.started:
            self.button_start.icon = ft.icons.PAUSE
            self.button_stop.disabled = False
        else:
            self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
            self.button_stop.disabled = False
        self.start_tasks()
        self.button_start.update()
        self.button_stop.update()

    def process_is_alive(self):
        self.tasks_process.join()
        self.started = False
        self.stopped = False
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.button_start.update()
        self.button_stop.update()
        self.set_text("")

    def start_tasks(self):
        # print(f"{self.tasks_process.is_alive() = }")
        if not self.tasks_process.is_alive():
            self.tasks_process = threading.Thread(target=self.runner.run)
            self.tasks_process.daemon = True
            self.tasks_process.start()
            # asyncio.create_task(run(self.runner.run))
            # is_alive = threading.Thread(target=self.process_is_alive)
            # is_alive.deamon = True
            # is_alive.start()
        else:
            self.add_text("Task is froze for an unknown reason, you may want to restart the bot..")
            print("Task is froze for an unknown reason, you may want to restart the bot..")

    def stop(self):
        self.started = False
        self.stopped = True
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.set_text("")
        self.button_start.update()
        self.button_stop.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        self.text_status.update()

    def get_text(self):
        return self.text_status.value

    def add_text(self, phrase: str, color = None):
        # # print(self.page.frames)
        # if len(self.page.controls) > 2:
        #     self.page.controls.pop()
        if self.number not in self.page.frames:
            self.page.frames[self.number] = Frame(self.page, self.number)
            # self.page.add(self.page.frames[self.number])
            # self.page.update()

        self.page.frames[self.number].logger.add_text(phrase, color)

        # self.page.update()
