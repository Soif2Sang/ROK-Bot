from __future__ import annotations

import threading
from typing import Literal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.views.tiles.handler.config_handler import InstanceTabs
    from src.views.tiles.tile_slave import TileSlave
    from src.views.tiles.tile_worker import TileWorker


class TaskWrapper:
    thread: threading.Thread
    status: Literal["running", "paused", "stopped", "idle"] = "idle"

    def __init__(self, thread):
        self.thread = thread

class ContextManager:
    tasks: {str, TaskWrapper} = {}
    workers: {str, TileWorker} = {}
    slaves: {str, TileSlave} = {}
    frames: {str, InstanceTabs} = {}

    def start(self, number, task):
        if not self.tasks.get(number) or not self.tasks[number].thread.is_alive():
            self.tasks[number] = TaskWrapper(threading.Thread(target=task.run))

        self.tasks[number].thread.start()

    def pause(self, number):
        if not self.tasks.get(number):
            raise Exception("Runner is not running")

        self.tasks[number].status = "paused"

    def stop(self, number):
        if not self.tasks.get(number):
            raise Exception("Runner is not running")

        self.tasks[number].status = "stopped"

    def resume(self, number):
        if not self.tasks.get(number):
            raise Exception("Runner is not running")

        self.tasks[number].status = "running"

    def join(self, number):
        if not self.tasks.get(number):
            raise Exception("Runner is not running")

        self.tasks[number].thread.join()

    def add_worker(self, number, worker):
        self.workers[number] = worker

    def add_slave(self, number, slave):
        self.slaves[number] = slave

    def add_frame(self, number, frame):
        self.frames[number] = frame

    def get_worker(self, number):
        return self.workers[number]

    def get_slave(self, number):
        return self.slaves[number]

    def get_frame(self, number):
        return self.frames[number]

contextManager = ContextManager()

