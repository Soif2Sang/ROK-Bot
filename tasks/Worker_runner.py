import dataclasses
from datetime import timedelta
from random import randint
from time import time
from typing import Literal

from tasks.Task import Task
from tasks.Task_runner import TaskRunner
from utils.functions import FileSingleton, colorize_name, colorize_output, current_time, get_name, string_to_co, string_to_co_slide
from utils.schemas.application_schemas import TileSlaveSchema, TileWorkerSchema
from utils.singletons import EmulatorSingleton


@dataclasses.dataclass
class WorkerRunner:
    instance_id: str
    tile_worker: TileWorkerSchema
    emulator_type: Literal["ld", "bluestacks"] = EmulatorSingleton().getEmulatorType()
    FileSingleton = FileSingleton()

    def update_data(self):
        self.data = self.FileSingleton.get_data()
        return self.data

    def run(self, tiles: [TileSlaveSchema]):
        self.data = self.update_data()

        loop_task = 1 if not self.data["workers"][self.emulator_type][self.instance_id]["loop_task"] else 9999999

        for i in range(loop_task):
            cycle_started_at = time()
            nb_tile = 0
            for enabled_tile in tiles:
                enabled_tile.set_text(f"In queue ({nb_tile})")
                nb_tile += 1

            for enabled_tile in tiles:
                runner_started_at = time()

                runner = TaskRunner(Task(enabled_tile), self.tile_worker)
                runner.run()

                if runner.has_started_once:
                    if self.data["workers"][self.emulator_type][self.instance_id]["close_emulator"]:
                        runner.kill_instance()
                        runner.print("Shutdown the emulator, waiting for 5 seconds")
                        runner.better_sleep((5, 5))

                    runner.print(
                        f"The bot took {timedelta(seconds=int(time() - runner_started_at))} to complete all the tasks on this emulator.",
                        "green",
                    )

            # Check if loop_task is enabled
            if self.data["workers"][self.emulator_type][self.instance_id]["loop_task"]:

                # Retrieve and sort the waiting cooldown times
                waiting_cooldown = self.data["workers"][self.emulator_type][self.instance_id]["waiting_cooldown"]
                waiting_cooldown.sort()

                # Extract the minimum and maximum waiting cooldown times
                min_cooldown, max_cooldown = waiting_cooldown

                # Calculate a random time before redoing tasks, within the range of min_cooldown and max_cooldown
                time_before_redo_tasks = int(randint(min_cooldown, max_cooldown) * 60) + randint(0, 60)

                # Iterate over the tiles
                for i, enabled_tile in enumerate(tiles):
                    # Add text to the tile indicating the time taken for the run
                    time_taken = (time() - cycle_started_at) / 60
                    enabled_tile.add_text(f"Run nb°{i} took {time_taken:0.1f} minutes to complete.")

                    # Update the tile's text to show its position in the queue
                    enabled_tile.set_text(f"In queue ({i})")

                # Set a timer for the first tile in the list
                Task(tiles[0]).set_timer(time_before_redo_tasks)
