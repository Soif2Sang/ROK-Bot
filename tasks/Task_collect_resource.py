from random import shuffle
from math import sqrt

from tasks.Task import Task
from utils.functions import filter_coordinate, get_class


class CollectResource(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.collect_city_resources
        self.execute_inside_city = True

    def task_name(self):
        return "CollectResource"

    def find_nearest_coordinate(self, coordinates):
        """Return the nearest coordinate to the center (720, 360)"""
        center_x, center_y = 720, 360
        return min(coordinates, key=lambda co: sqrt((co[0] - center_x) ** 2 + (co[1] - center_y) ** 2))

    def collect_resource(self, resource_type):
        """Generic method to collect resources based on the resource type."""
        co_max = self.adb.find_multiple_img(target=f"{resource_type}_max", confidence=0.8)
        co_min = self.adb.find_multiple_img(target=f"{resource_type}_min", confidence=0.8)
        co_max.extend(co_min)
        co_filtered = list(filter(filter_coordinate, co_max))

        if co_filtered:
            return self.find_nearest_coordinate(co_filtered)
        return None

    @get_class
    def run(self):
        resource_types = ["food", "wood", "stone", "gold"]  # Array of resource types
        shuffle(resource_types)  # Shuffle tasks to randomize the collection order

        for resource in resource_types:
            result = self.collect_resource(resource)
            if result is not None:
                self.print(f"{resource.capitalize()} successfully claimed")
                self.click(result[0] + 10, result[1] + 20)  # Minor offset for safe clicking
                self.better_sleep((0.695, 1))
            else:
                self.print(f"Unable to find {resource}")
