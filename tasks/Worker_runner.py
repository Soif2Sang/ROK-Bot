from __future__ import annotations

import dataclasses
from datetime import timedelta
from random import randint
from time import time
from typing import Literal
from utils.context import contextManager

from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from utils.singletons import EmulatorSingleton, ss
from utils.schemas.application_schemas import TileSlaveSchema, TileWorkerSchema


@dataclasses.dataclass
class WorkerRunner:
    instance_id: str
    emulator_type: Literal["ld", "bluestacks"] = EmulatorSingleton().getEmulatorType()

    def run(self):
        self.emulator_type: Literal["ld", "bluestacks"] = EmulatorSingleton().getEmulatorType()
        self.slaves = ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].instances

        loop_task = 1 if not ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].loop_task else 9999999

        for i in range(loop_task):
            contextManager.tasks.get(self.instance_id).status = "running"
            cycle_started_at = time()
            nb_tile = 0

            for slave in self.slaves:
                contextManager.get_slave(slave.instance).set_status(f"In queue ({nb_tile})")
                nb_tile += 1

            for slave in self.slaves:
                runner_started_at = time()
                runner = TaskRunner(Task(slave.instance))
                runner.run()

                if runner.has_started_once:
                    if ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].close_emulator:
                        runner.kill_instance()
                        runner.print("Shutdown the emulator, waiting for 5 seconds")
                        runner.better_sleep((5, 5))

                    runner.print(
                        f"The bot took {timedelta(seconds=int(time() - runner_started_at))} to complete all the tasks on this emulator.",
                        "green",
                    )

            # Check if loop_task is enabled
            if ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].loop_task:

                # Retrieve and sort the waiting cooldown times
                waiting_cooldown = ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].waiting_cooldown
                waiting_cooldown.sort()

                # Extract the minimum and maximum waiting cooldown times
                min_cooldown, max_cooldown = waiting_cooldown.min, waiting_cooldown.max

                # Calculate a random time before redoing tasks, within the range of min_cooldown and max_cooldown
                time_before_redo_tasks = int(randint(min_cooldown, max_cooldown) * 60) + randint(0, 60)

                for slave in self.slaves:
                    # Add text to the tile indicating the time taken for the run
                    time_taken = (time() - cycle_started_at) / 60
                    contextManager.get_slave(slave.instance).add_text(f"Run nb°{i} took {time_taken:0.1f} minutes to complete.")

                    # Update the tile's text to show its position in the queue
                    contextManager.get_slave(slave.instance).set_status(f"In queue ({i})")

                # Set a timer for the first tile in the list
                Task(self.slaves[0].instance).set_timer(time_before_redo_tasks)

            contextManager.tasks.get(self.instance_id).status = "idle"

    def get_screen(self):
        self.emulator_type = "ld"
        self.slaves = ss.worker_settings.worker_type[self.emulator_type].workers[self.instance_id].instances

        for slave in self.slaves:
            runner = TaskRunner(Task(slave.instance))
            return runner.adb.get_cv2_img()