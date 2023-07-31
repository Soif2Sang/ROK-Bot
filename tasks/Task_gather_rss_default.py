import traceback
from random import uniform
from time import sleep

from PIL import Image

from Task_gather_rss import GatherRss
from tasks.Task import Task
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader

class GatherRssDefault(GatherRss):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "GatherRss"

    @get_name
    def select_resource_type(self, place: str) -> tuple[float, float]:
        food_icon = ((400, 472), (603, 663))
        wood_icon = ((598, 670), (603, 663))
        stone_icon = ((786, 870), (603, 663))
        gold_icon = ((977, 1050), (603, 663))
        if self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "food":
            x, y = uniform(food_icon[0][0], food_icon[0][1]), uniform(food_icon[1][0], food_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "wood":
            x, y = uniform(wood_icon[0][0], wood_icon[0][1]), uniform(wood_icon[1][0], wood_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "stone":
            x, y = uniform(stone_icon[0][0], stone_icon[0][1]), uniform(stone_icon[1][0], stone_icon[1][1])
        else:  # Gold
            x, y = uniform(gold_icon[0][0], gold_icon[0][1]), uniform(gold_icon[1][0], gold_icon[1][1])
        # print(f'[ {current_time()} ] [ {self.name} ] chance rss type call')
        return x, y

    @get_name
    def node_found(self) -> bool:
        if self.find_img(target='search_button') is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def click_search_adapted_node(self, place: str) -> None:
        self.print(f"Looking for : {self.data[str(self.sel)]['schedules'][self.current_profile].get(place)} {place}")
        if self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "food":
            x = uniform(400, 472)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "wood":
            x = uniform(598, 670)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "stone":
            x = uniform(786, 870)
            y = uniform(463, 512)
            self.click(x, y)
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "gold":
            x = uniform(977, 1050)
            y = uniform(463, 512)
            self.click(x, y)

    @get_name
    def minable(self) -> bool:
        if self.find_img(target="search_button") is None and not self.find_cross():
            return True
        # self.print("Unable to gather this node")
        return False

    @get_class
    def run(self, node_type=None, resolved=False, level_decrease=0):
        self.run_game()
        if not resolved:
            resolved = self.check_captcha()
        self.check_reconnect()
        self.check_log_back()
        self.check_download_page()
        if node_type is None:
            node_type = "First"
        if node_type == "Done":
            self.click(uniform(600, 700), (uniform(250, 400)))
            self.better_sleep((2, 4))
            return
        if self.data[str(self.sel)]['schedules'][self.current_profile][node_type] == 'nothing':
            return
        self.leave_city_simple()
        # self.better_sleep((2, 4))
        # Vérifie si y'a une troupe
        if self.free_troop_commander_list():
            self.check_log_back()
            self.check_reconnect()
            self.click_loop()
            x, y = self.select_resource_type(node_type)
            # self.better_sleep((1.325, 1.795))
            self.click(x, y)
            self.better_sleep((1.325, 3.795))

            if self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                    f"{node_type}_level") - level_decrease <= 0:
                node_type = self.next_resource_type(node_type)
                self.print(f"Cannot decrease the current level.. Too low ! next type : {node_type}")
                return self.run(node_type, resolved, 0)

            self.set_search_level(self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                f"{node_type}_level") - level_decrease)
            self.better_sleep((0.925, 2.795))
            self.click_search_adapted_node(node_type)
            self.better_sleep((5, 9))

            # Tant que la node trouvée n'est pas minable (pas de cross, plus dans le menu des rss)
            # if not self.minable():

            # self.better_sleep((1.325, 3.795))
            # Si y'a plus de node on return le prochain rss
            if self.node_found() is False or self.find_cross() is True:
                self.check_reconnect()
                self.check_log_back()
                self.click((1280 // 2) + uniform(-20, 20), (720 // 3) + uniform(-20, 20))
                self.better_sleep((1.325, 3.795))
                if level_decrease >= 1:
                    self.print("No node matched the requirements, changing node type..")
                    return self.run(self.next_resource_type(node_type), resolved, 0)
                else:
                    self.print(f"{level_decrease+1 = }, {node_type = }")
                    self.print("No node matched the requirements, reducing the level..")
                    return self.run(node_type, resolved, level_decrease + 1)
                # self.better_sleep((5, 9))
            self.check_reconnect()
            self.check_log_back()
            if self.click_on_node() and not self.send_troop():
                self.click(uniform(200, 900), uniform(300, 500))
                self.better_sleep((2.325, 5.795))
                return "Done"
            self.better_sleep((1, 2.895))
            if not resolved:
                resolved = self.check_captcha()
            node_type = self.next_resource_type(node_type)
            return self.run(node_type, resolved, 0)
        # self.click(uniform(22, 90), uniform(625, 675))
        return "Done"
