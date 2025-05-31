from random import choice, uniform

from PIL import Image

from src.tasks.Task import Task
from src.tasks.Task_gather_rss import GatherRss
from src.utils.functions import get_class, get_name, rgetattr

# from utils.easyOcr import Reader


class GatherRssDefault(GatherRss):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.gather_rss

    def task_name(self):
        return "GatherRss"

    @get_name
    def select_resource_type(self, node_type: str) -> tuple[float, float]:
        icon_ranges = {
            "food": ((400, 472), (603, 663)),
            "wood": ((598, 670), (603, 663)),
            "stone": ((786, 870), (603, 663)),
            "gold": ((977, 1050), (603, 663)),
        }

        x_range, y_range = icon_ranges.get(node_type)

        x = uniform(x_range[0], x_range[1])
        y = uniform(y_range[0], y_range[1])

        return x, y

    @get_name
    def node_found(self) -> bool:
        if self.find_img(target="search_button") is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def click_search_by_node_type(self, node_type: str) -> None:
        icon_ranges = {
            "food": ((400, 472), (463, 512)),
            "wood": ((598, 670), (463, 512)),
            "stone": ((786, 870), (463, 512)),
            "gold": ((977, 1050), (463, 512)),
        }

        x_range, y_range = icon_ranges.get(node_type, ((400, 472), (463, 512)))

        x = uniform(x_range[0], x_range[1])
        y = uniform(y_range[0], y_range[1])

        self.click(x, y)

    @get_name
    def minable(self) -> bool:
        screen = self.adb.get_screen()
        if self.find_img(target="search_button", source=screen[720 // 2 :, : 1280 // 4]) is None and not self.find_cross(
            screen[230:480, 441:814]
        ):
            return True
        # self.print("Unable to gather this node")
        return False

    @get_name
    def set_search_level(self, level: int = 10) -> None:
        try:
            super().set_search_level(level)
        except TypeError:
            self.close_windows()
            self.leave_city_simple()
            return super().set_search_level(level)

    @get_class
    def run(self, node_place="First", node_type=None, resolved=False, level_decrease=0):
        self.run_game()
        if not resolved:
            resolved = self.check_captcha()

        screen = self.check_reconnect(self.adb.get_screen())
        screen = self.check_download_page(screen)
        self.check_log_back(screen)

        if node_place == "Done":
            self.click(uniform(600, 700), (uniform(250, 400)))
            self.better_sleep((2, 4))
            return

        if node_type is None:
            result = rgetattr(self.context_task, node_place.lower() + "_node").type
            if result == "nothing":
                return
            elif result == "random":
                result = choice(["food", "wood", "stone", "gold"])
            # else:
            node_type = result

        self.leave_city_simple()

        if self.free_troop_commander_list():
            self.check_reconnect()
            self.check_log_back()
            self.click_loop()

            x, y = self.select_resource_type(node_type)
            self.click(x, y)
            self.better_sleep((1.325, 3.795))

            target_level = rgetattr(self.context_task, node_place.lower() + "_node").level
            if target_level - level_decrease <= 0:
                node_place = self.next_place(node_place)
                self.print(f"Cannot decrease the current level.. Too low ! next choice : {node_place}")
                return self.run(node_place, None, resolved, 0)

            self.set_search_level(target_level - level_decrease)
            self.better_sleep((1.925, 2.795))
            self.click_search_by_node_type(node_type)
            self.better_sleep((5, 8))

            if self.node_found() is False or self.find_cross() is True:
                self.check_reconnect()
                self.check_log_back()
                self.click((1280 // 2) + uniform(-20, 20), (720 // 3) + uniform(-20, 20))
                self.better_sleep((1.325, 3.795))
                if level_decrease >= 1:
                    self.print("No node matched the requirements, changing node type..")
                    return self.run(self.next_place(node_place), None, resolved, 0)
                else:
                    self.print(f"{level_decrease+1 = }, {node_place = }")
                    self.print("No node matched the requirements, reducing the level..")
                    return self.run(node_place, node_type, resolved, level_decrease + 1)
                # self.better_sleep((5, 9))
            self.check_reconnect()
            self.check_log_back()
            if self.click_on_node() and not self.send_troop():
                self.click(uniform(200, 900), uniform(300, 500))
                self.better_sleep((2.325, 5.795))
                return "Done"
            if not resolved:
                resolved = self.check_captcha()
            node_place = self.next_place(node_place)
            return self.run(node_place, None, resolved, 0)
        return "Done"
