import threading

import flet as ft

from utils.schemas.application_schemas import TileWorkerSchema
from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from tasks.TaskPC import Task as TaskPC
from tasks.TaskPC_runner import TaskRunner as TaskPCRunner
from tasks.Worker_runner import WorkerRunner
from utils.flet_translations import translate
from utils.singletons import EmulatorSingleton, ss, FileSingleton
from views.tiles.handler.config_handler import InstanceTabs
from views.tiles.tile_slave import TileSlave


class TileWorker(ft.ExpansionTile):
    def __init__(self, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.paused = False
        self.stopped = False

        # if EmulatorSingleton().getEmulatorType() == "pc":
        #     self.main_task = TaskPC(self)
        #     self.runner = TaskPCRunner(self.main_task, self)
        # else:
        #     self.main_task = Task(self)
        #     self.runner = TaskRunner(self.main_task, self)
        #
        # self.runner.worker = self
        # self.tasks_process = threading.Thread(target=self.runner.run4)

        self.runner = WorkerRunner(self.number, self)
        self.tasks_process = threading.Thread(target=self.runner.run, args=(self.controls,))

        self.button_select = ft.IconButton(
            icon=ft.icons.SETTINGS,
            selected_icon=ft.icons.SETTINGS,
            on_click=self.select,
        )

        self.button_start = ft.IconButton(icon=ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED, on_click=self.start)
        self.button_stop = ft.IconButton(icon=ft.icons.HIGHLIGHT_REMOVE_ROUNDED, disabled=True, on_click=self.stop)

        self.text_name = ft.Text(value=translate(f"Worker") + f" n°{self.number}", width=120, size=16)
        self.text_status = ft.Text(value="")
        self.tile_padding = ft.padding.all(0)
        self.title = ft.Row(
            [
                ft.Row(
                    controls=[
                        # self.button_select,
                        self.button_start,
                        self.button_stop,
                        self.text_name,
                        self.text_status,
                    ],
                    spacing=0,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        self.slaves = {}
        self.refresh_tile()


    def start(self, e):
        self.button_start.icon = ft.icons.PAUSE
        self.button_stop.disabled = False

        for slaves_tiles in self.controls:
            slaves_tiles.paused = False
            slaves_tiles.stopped = False

        self.paused = False
        self.stopped = False

        self.start_tasks()
        self.button_start.on_click = self.pause
        self.tasks_process.join()

        self.button_start.on_click = self.start

        for slaves_tiles in self.controls:
            slaves_tiles.paused = False
            slaves_tiles.stopped = False
        self.paused = False
        self.stopped = False

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True

        self.set_text("")
        for tiles in self.controls:
            tiles.set_text("")

    def resume(self, e):
        for slaves_tiles in self.controls:
            slaves_tiles.paused = False
        self.paused = False

        self.button_start.icon = ft.icons.PAUSE
        self.button_start.on_click = self.pause
        ss.page.update()

    def pause(self, e):
        for slaves_tiles in self.controls:
            slaves_tiles.paused = True
        self.paused = True

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_start.on_click = self.resume
        ss.page.update()

    def stop(self, e):
        for slaves_tiles in self.controls:
            slaves_tiles.paused = False
            slaves_tiles.stopped = True

        self.paused = False
        self.stopped = True

        self.button_start.icon = ft.icons.PLAY_CIRCLE_OUTLINE_ROUNDED
        self.button_stop.disabled = True
        ss.page.update()

    def start_tasks(self):
        if not self.tasks_process.is_alive():
            self.tasks_process = threading.Thread(target=self.runner.run, args=(self.controls,))
            self.tasks_process.start()
        else:
            self.add_text("Task is frozen, you may need to restart the bot.")
            ss.page.generate_toast("Warning", "Task is frozen, you may need to restart the bot.")

    def select(self, e):
        ss.page.tile_manager.unselect_all()
        self.button_select.selected = True

        if len(ss.page.body.controls) > 2:
            ss.page.body.controls.pop()

        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.body.controls.append(ss.page.frames[self.number])
        self.bgcolor = ft.colors.SURFACE_VARIANT
        ss.page.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        ss.page.update()

    def get_text(self):
        return self.text_status.value

    def add_text(self, phrase: str, color=None):
        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.frames[self.number].add_text(phrase, color)

    def add_divider(self):
        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.frames[self.number].add_divider()

    def add_tile(self, number):
        self.controls.append(TileSlave(number))

    def refresh_tile(self):
        self.controls = []
        # data = self.FileSingleton.getCachedData()
        emulator_type = EmulatorSingleton().getEmulatorType()

        worker_settings = ss.open_worker_settings()

        # for instance in data["workers"][emulator_type][self.number]["instances"]:
        #     if instance["instance"] not in self.slaves:
        #         self.slaves[instance["instance"]] = TileSlave(ss.page, instance["instance"])
        #     self.controls.append(self.slaves[instance["instance"]])

        for instanceSchema in worker_settings.worker_type[emulator_type].workers[self.number].instances:
            instance = instanceSchema.instance
            if instance not in self.slaves:
                self.slaves[instance] = TileSlave(instance)
            self.controls.append(self.slaves[instance])

        ss.page.update()
