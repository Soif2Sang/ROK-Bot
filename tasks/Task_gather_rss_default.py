import traceback
from random import choice, uniform
from time import sleep

from PIL import Image

from tasks.Task import Task
from tasks.Task_gather_rss import GatherRss
from utils.functions import get_class, get_name

# from utils.easyOcr import Reader


class GatherRssDefault(GatherRss):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask)
        self.herite(MainTask)

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
        screen = self.adb.get_cv2_img()
        if self.find_img(target="search_button", source=screen[720//2:,:1280//4]) is None and not self.find_cross(screen[230:480, 441:814]):
            return True
        # self.print("Unable to gather this node")
        return False

    @get_class
    def run(self, node_place=None, node_type=None, resolved=False, level_decrease=0):
        self.run_game()
        if not resolved:
            resolved = self.check_captcha()

        self.check_reconnect()
        self.check_log_back()
        self.check_download_page()

        if node_place is None:
            node_place = "First"

        if node_place == "Done":
            self.click(uniform(600, 700), (uniform(250, 400)))
            self.better_sleep((2, 4))
            return

        if self.data[str(self.sel)]["schedules"][self.current_profile][node_place] == "nothing":
            return

        if self.data[str(self.sel)]["schedules"][self.current_profile][node_place] == "random":
            if node_type is None:
                node_type = choice(["food", "wood", "stone", "gold"])
        else:
            node_type = self.data[str(self.sel)]["schedules"][self.current_profile][node_place]

        self.leave_city_simple()

        if self.free_troop_commander_list():
            self.check_log_back()
            self.check_reconnect()
            self.click_loop()

            self.print(f"Looking for : {node_type}")
            x, y = self.select_resource_type(node_type)

            self.click(x, y)
            self.better_sleep((1.325, 3.795))

            if self.data.get(self.sel).get("schedules").get(self.current_profile).get(f"{node_place}_level") - level_decrease <= 0:
                node_place = self.next_place(node_place)
                self.print(f"Cannot decrease the current level.. Too low ! next choice : {node_place}")
                return self.run(node_place, None, resolved, 0)

            self.set_search_level(
                self.data.get(self.sel).get("schedules").get(self.current_profile).get(f"{node_place}_level") - level_decrease
            )
            self.better_sleep((0.925, 2.795))
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
