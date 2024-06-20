import threading
from typing import Literal


class TaskWrapper:
    thread: threading.Thread
    status: Literal["running", "paused", "stopped", "idle"] = "idle"

    def __init__(self, thread):
        self.thread = thread

class ContextManager:
    runners: {str, TaskWrapper} = {}

    def start(self, runner, controls):
        if not self.runners.get(runner):
            self.runners[runner] = TaskWrapper(threading.Thread(target=runner.run, args=(controls,)))

        if self.runners[runner].thread.is_alive():
            raise Exception("Runner is already running")

        self.runners[runner].start()

    def pause(self, runner):
        if not self.runners.get(runner):
            raise Exception("Runner is not running")

        self.runners[runner].status = "paused"

    def stop(self, runner):
        if not self.runners.get(runner):
            raise Exception("Runner is not running")

        self.runners[runner].status = "stopped"

    def resume(self, runner):
        if not self.runners.get(runner):
            raise Exception("Runner is not running")

        self.runners[runner].status = "running"

contextManager = ContextManager()