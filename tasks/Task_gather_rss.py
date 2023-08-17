import traceback
from random import uniform
from time import sleep

from PIL import Image

from tasks.Task import Task
from utils.Task_utils import get_name, get_class


# from utils.easyOcr import Reader

class GatherRss(Task):
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

    @get_name
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0
        while self.find_img(target=f'{color}_icon', confidence=0.95) is None and self.find_img(target=
                                                                                               "troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(271, 300))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_text("Error in line-up selection")
                self.send_discord_message("Error in line-up selection, human interaction required.")
                while True:
                    self.script_pause()
                    sleep(0.1)
            self.click(uniform(1092, 1114), uniform(190, 200))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def send_new_troop(self, deadstop: int = 0, color: str = 'yellow') -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """
        try:
            self.print("Trying to send new troop..")
            self.print(f"Send new troop count : {deadstop}")
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(300, 500))
                self.better_sleep((1.325, 1.795))
                return False
            co = self.find_img(target="new_troops_button", confidence=0.70)
            if co is not None:
                # print("Home button found")
                x, y = co[0], co[1]
                x, y = x + uniform(0, 20), y + uniform(0, 20)
                self.click(x, y)
                self.better_sleep((1.825, 2.495))
                x_click, y_click = uniform(1090, 1111), uniform(329, 348)
                self.better_sleep((1.225, 1.795))
                self.select_lineup_color(color=color)
                default_image = self.adb.get_cv2_img()
                for i in range(7):  # change if you have 6-7 troops
                    default_color = default_image[260 + i * 50, 1100]
                    x_click, y_click = uniform(1096, 1118), uniform(260 + i * 50, 275 + i * 50)
                    self.click(x_click, y_click)
                    self.better_sleep((1, 2))
                    new_image = self.adb.get_cv2_img()
                    if (default_color != new_image[260 + i * 50, 1100]).all():
                        x, y = self.find_img(target="troops_march_button")
                        x, y = x + uniform(0, 20), y + uniform(0, 20)

                        self.click(x, y)
                        self.better_sleep((0.5, 0.7))
                        self.print("New Troop sent !", "green")
                        return True
                co = self.find_img(target="troops_march_button")
                if co is None:
                    return self.send_new_troop(deadstop=deadstop + 1)
                x, y = co[0], co[1]
                x, y = x + uniform(0, 20), y + uniform(0, 20)
                self.click(x, y)

                self.better_sleep((0.5, 0.7))
                self.print("New Troop sent !", "green")
                return True
            co = self.find_img(target="march_bar")
            if co is not None and self.free_troop_selection():
                return self.send_new_troop(deadstop=deadstop + 1)
            self.print("Unable to send a new troop", "red")
            return False
        except Exception as e:
            traceback.print_exc()
            self.print("Error sending a new march to the gem node !", "red")

    @get_name
    def click_on_node(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        self.print("Clicking on the node..")
        while self.find_img(target="resource_gather_button", confidence=0.7) is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.995, 1.4))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        co = self.find_img(target="resource_gather_button", confidence=0.7)
        if co is not None:
            x, y = co[0], co[1]
            self.click(x + uniform(0, 150), y + uniform(0, 30))
            self.better_sleep((1.325, 2.795))
            return True
        else:
            self.print("Unable to click on the node, leaving the node !")
            return False

    @get_name
    def send_troop(self) -> bool:
        self.better_sleep((1.8, 3))
        self.print("Trying to send a new troop..")
        if self.data[str(self.sel)]['schedules'][self.current_profile]['rss_custom_preset']:
            self.send_new_troop()
            self.better_sleep((0.7, 1.1))
        else:
            co = self.find_img(target="new_troops_button", confidence=0.7)
            if co is None:
                return False
            x, y = co[0], co[1]
            x, y = x + uniform(0, 160), y + uniform(0, 30)
            self.click(x, y)
            self.better_sleep((2.325, 2.795))
            x, y = self.find_img(target="troops_march_button")
            x, y = x + uniform(0, 80), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((1.1, 2))
        if self.find_img(target="troops_march_button") is not None:
            self.click(uniform(1106, 1123), uniform(36, 55))
            self.better_sleep((1.1, 1.5))
            self.print("Cannot send the troop")
            return False
        self.print("Troop sent !", "green")
        return True

    @get_name
    def next_resource_type(self, place: str) -> str:
        # print(f'[ {current_time()} ] [ {self.name} ] next_resource_type call')
        if place == "First":
            return "Second"
        elif place == "Second":
            return "Third"
        elif place == "Third":
            return "Fourth"
        elif place == "Fourth":
            return "Fifth"
        elif place == "Fifth":
            return "Sixth"
        elif place == "Sixth":
            return "Seventh"
        elif place == "Seventh":
            return "Done"

    @get_class
    def run1(self, node_type=None, resolved=False, level_decrease=0):
        if not resolved:
            resolved = self.check_captcha()
        if node_type is None:
            node_type = "First"
        if node_type == "Done":
            self.click(uniform(600, 700), (uniform(250, 400)))
            self.better_sleep((2, 4))
            return

        nbsearch = 0
        self.check_reconnect()
        self.leave_city_simple()
        # self.better_sleep((2, 4))
        # Vérifie si y'a une troupe
        level_verified = False
        while self.free_troop_commander_list():
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
                print(f"{level_decrease = }, {node_type = }")
                return self.run(node_type, resolved, level_decrease)

            if level_verified is False:
                self.set_search_level(self.data.get(self.sel).get('schedules').get(self.current_profile).get(
                    f"{node_type}_level") - level_decrease)
                self.better_sleep((0.925, 2.795))
                level_verified = True
            print(f"{node_type =}")
            self.click_search_adapted_node(node_type)
            self.better_sleep((5, 9))

            # Tant que la node trouvée n'est pas minable (pas de cross, plus dans le menu des rss)
            while not self.minable():
                self.check_reconnect()
                # self.better_sleep((1.325, 3.795))
                # Si y'a plus de node on return le prochain rss

                if self.node_found() is False:
                    self.click(uniform((1280 // 2) - 20, (1280 // 2) + 20), uniform((720 // 3) - 20, (720 // 3) + 20))
                    self.better_sleep((0.425, 1.495))
                    if level_decrease >= 2:
                        self.print("No node matched the requirements, changing node type..")
                        return self.run(self.next_resource_type(node_type), resolved, 0)
                    else:
                        self.print(f"{level_decrease+1 = }, {node_type = }")
                        self.print("No node matched the requirements, reducing the level..")
                        return self.run(node_type, resolved, level_decrease + 1)

                # Si y'a une cross
                # self.better_sleep((2, 5.5))
                if self.find_cross() is True:
                    # Au bout de deux search ca va au charbon avec le prochain rss
                    if nbsearch == 2:
                        self.print("nbsearch == 2")
                        self.click((1280 // 2) + uniform(- 20, 20),
                                   (720 // 3) + uniform(- 20, + 20))
                        self.better_sleep((0.225, 2.295))

                        if level_decrease >= 2:
                            self.print("No node matched the requirements, changing node type..")
                            return self.run(self.next_resource_type(node_type), resolved, 0)
                        else:
                            self.print(f"{level_decrease+1 = }, {node_type = }")
                            self.print("No node matched the requirements, reducing the level..")
                            return self.run(node_type, resolved, level_decrease + 1)
                    else:
                        nbsearch += 1
                        self.print("nbsearch != 2")
                        self.print("Looking for a new node")
                        self.click_loop()
                        self.better_sleep((0.625, 1.995))
                        self.click_search_adapted_node(node_type)
                self.better_sleep((5, 9))
            self.check_reconnect()
            if self.click_on_node() and not self.send_troop():
                self.click(uniform(200, 900), uniform(300, 500))
                self.better_sleep((2.325, 5.795))
                return "Done"
            self.better_sleep((1, 2.895))
            resolved = self.check_captcha()
            node_type = self.next_resource_type(node_type)
        self.click(uniform(22, 90), uniform(625, 675))
        return "Done"

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
