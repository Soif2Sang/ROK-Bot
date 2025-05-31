from random import choice, randint, uniform
from time import sleep

from PIL import Image

from src.tasks.Task import Task
from src.utils.functions import current_time, get_class, get_name, rgetattr


class HuntBarbarians(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.kill_barbarian

    def task_name(self):
        return "HuntBarbarians"

    @get_name
    def select_lineup_color(self, color: str) -> None:
        """
        Change the line-up until the yellow line-up is selected.
        """
        deadstop = 0
        while self.find_img(target=f"{color}_icon", confidence=0.93) is None and self.find_img(target="troops_march_button") is not None:
            if deadstop == 5:
                self.click(uniform(700, 800), uniform(271, 300))
                self.better_sleep((0.557, 0.796))
                self.print("Error in line-up selection")
                self.set_status("Error in line-up selection")
                self.send_discord_message("Error in line-up selection, please fix the game")
                while True:
                    self.script_pause()
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(190, 200))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def send_new_troop(self, deadstop: int = 0, preset: str = "1") -> bool:
        """
        Send a new troop to gather the gem node
        :return: True is successfully
        :return: False is not successfully
        """

        self.print(f"Trying to send new troop.. {preset=}")
        if deadstop != 0:
            self.print(f"Send new troop count : {deadstop}")
        if deadstop == 5:
            self.click(uniform(700, 800), uniform(300, 500))
            self.better_sleep((1.325, 1.795))
            return False
        co = self.find_img(target="new_troops_button")
        if co is not None:
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
            self.better_sleep((1.825, 2.495))
            self.select_lineup_color(color="red")

            presets = {
                "first": 270,
                "second": 320,
                "third": 370,
                "fourth": 430,
                "fifth": 480,
                "sixth": 530,
                "seventh": 680,
            }
            self.click(uniform(1096, 1118), presets[preset])
            self.better_sleep((0.5, 1))
            co = self.find_img(target="troops_march_button")
            if co is None:
                return self.send_new_troop(deadstop=deadstop + 1, preset=preset)
            self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
            self.better_sleep((0.5, 0.7))
            if self.find_img(target="troops_march_button"):
                self.print("Unable to send a new troop")
                self.close_windows()
                return False
            self.print("New Troop sent !")
            return True
        co = self.find_img(target="march_bar")
        if co is not None and self.free_troop_selection():
            self.close_windows()
            self.better_sleep((0.5, 0.7))
            return self.send_new_troop(deadstop=deadstop + 1, preset=preset)
        self.print("Unable to send a new troop")
        return False

    @get_name
    def deploy_hunter_old(self):
        full_area = [(i, y) for i in range(420, 840, 5) for y in range(200, 530, 5) if not (795 > i > 490 and 210 < y < 490)]
        hunters = 0
        breakloop = False

        preset_indexes = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
        for preset in preset_indexes:
            if not rgetattr(self.context_task.presets_selection, preset):
                continue
            sent = False
            if breakloop:
                break
            while not sent:
                self.print(f"{hunters =}, {preset =}")
                if not full_area:
                    breakloop = True
                    break
                co = choice(full_area)
                # self.print(f"Choice {co}")
                for i in range(-65, 80, 5):
                    for y in range(-65, 70, 5):
                        if (co[0] + i, co[1] + y) in full_area:
                            full_area.remove((co[0] + i, co[1] + y))
                self.swipe_arg(co[0], co[1], co[0], co[1], randint(2500, 3475))
                self.better_sleep((1.325, 1.795))
                co = self.find_img(target="deploy_march_button")
                if co is not None:
                    self.click(co[0] + uniform(0, 140), co[1] + uniform(0, 4))
                    self.better_sleep((1.325, 1.795))
                    if self.find_img(target="new_troops_button"):
                        if not self.send_new_troop(preset=preset):
                            breakloop = True
                            break
                        else:
                            sent = True
                            hunters += 1
                    else:
                        self.click(uniform(150, 500), uniform(150, 500))
                    self.better_sleep((1.325, 1.795))

                if self.find_img(target="new_troops_button"):
                    self.close_windows()
        return hunters

    @get_name
    def deploy_hunter(self):
        full_area = [(i, y) for i in range(420, 840, 5) for y in range(200, 530, 5) if not (795 > i > 490 and 210 < y < 490)]

        hunters = 0

        entered = False
        while not entered:
            co = choice(full_area)
            # self.print(f"Choice {co}")
            for i in range(-65, 80, 5):
                for y in range(-65, 70, 5):
                    if (co[0] + i, co[1] + y) in full_area:
                        full_area.remove((co[0] + i, co[1] + y))
            self.swipe_arg(co[0], co[1], co[0], co[1], randint(2500, 3475))
            self.better_sleep((1.325, 1.795))
            co = self.find_img(target="deploy_march_button")
            if co is not None:
                self.click(co[0] + uniform(0, 140), co[1] + uniform(0, 4))
                self.better_sleep((1.525, 1.995))
                if co := self.find_img(target="new_troops_button", confidence=0.7):
                    self.click(co[0], co[1])
                    self.better_sleep((1.525, 1.995))
                    entered = True
                else:
                    self.click(uniform(150, 500), uniform(150, 500))
                    self.better_sleep((1.525, 1.995))

            if self.find_img(target="new_troops_button"):
                self.close_windows()

        self.select_lineup_color(color="red")

        self.click(1100, 640)
        self.better_sleep((1.525, 1.995))

        preset_indexes = {"first": 1, "second": 2, "third": 3, "fourth": 4, "fifth": 5, "sixth": 6, "seventh": 7}
        for preset, value in preset_indexes.items():
            if rgetattr(self.context_task.presets_selection, preset):
                hunters += 1
                continue
            else:
                self.click(1000, 205 + value * 55)
                self.better_sleep((1.325, 1.795))

        self.click(930, 630)
        self.better_sleep((1.325, 1.795))

        for _ in range(hunters):
            self.better_sleep((3, 3))
        return hunters

    @get_name
    def recall(self, nb_troop: int, wait=True) -> bool:
        self.print("Recalling troops")
        self.click(uniform(1170, 1183), uniform(160, 175))
        self.better_sleep((1.595, 2))
        nb_to_go = nb_troop
        breakint = 0
        while (nb_to_go > 0) & (breakint != 4):
            while (co := self.find_img(target="return_button")) is None and breakint != 4:
                print(f"[ {current_time()} ] [ {self.name} ] Return button not found")

                y, x = uniform(290, 480), uniform(460, 560)
                x2, y2 = x + uniform(-30, 30), y + uniform(-200, -100)
                self.swipe(x, y, x2, y2)
                self.better_sleep((2, 3))
                breakint += 1
            if co:
                self.click(co[0] + uniform(0, 10), co[1] + uniform(0, 10))
                self.better_sleep((1.695, 2))
                nb_to_go = nb_to_go - 1
            self.better_sleep((1.695, 2))

        self.close_windows()

        if wait:
            said = False
            while self.find_img(target="back_normal_view", confidence=0.9):
                if not said:
                    said = True
                    self.print("Waiting for the troop to come back..")
                self.better_sleep((10, 10))

    @get_name
    def check_ap_box(self) -> bool:
        self.print(f"Check if AP pop-op box is detected")
        if self.find_img(target="ap_bottle"):
            self.print(f"AP pop-op box Detected")
            if co := self.find_img(target="daily_ap_claim"):
                x, y = co[0] + uniform(0, 30), co[1] + uniform(0, 20)
                self.click(x, y)
                self.print("Claiming Free AP", "green")
                self.better_sleep((1.325, 1.795))
                self.close_windows()
                if co := self.find_img("march_bar"):
                    self.click(co[0] + uniform(0, 30), co[1] + uniform(0, 10))
                    self.better_sleep((2, 3))
                return False
            self.close_windows()
            self.click(uniform(700, 800), uniform(300, 400))
            return True
        self.print(f"AP pop-op box Not detected")
        return False

    @get_name
    def wait_until_kill(self):
        self.print(f"Waiting for the troops to kill the barbarian..")
        while self.find_img(target="troop_idle") is None or self.find_img(target="troop_walking") is not None:
            if not self.adb.is_game_alive():
                self.run_game()
                self.leave_city()
            self.script_pause()
            self.check_log_back()
            self.check_reconnect()
            self.check_captcha()
            self.better_sleep((8, 15))
            print(f"[ {current_time()} ] [ {self.name} ] Waiting for the troops to kill the barbarian..")

    @get_class
    def run(self):
        preset_selected = 0

        preset_indexes = ["first", "second", "third", "fourth", "fifth", "sixth", "seventh"]
        for preset in preset_indexes:
            if rgetattr(self.context_task.presets_selection, preset):
                preset_selected += 1

        if preset_selected == 0:
            return self.print("No presets selected, canceling the function", "red")

        if not self.enough_action_points():
            return self.print("It looks like you are low in AP, cancelling the function", "red")

        wanted_level = self.context_task.target_level
        hunter_selection = False
        self.leave_city()
        self.better_sleep((1, 1.3))
        nb_hunter = self.deploy_hunter()
        if nb_hunter == 0:
            return self.print("No PeaceKeeper sent, cancelling the function", "red")
        while not self.check_ap_box():
            self.run_game()
            self.better_sleep((1.5, 3))

            self.click_loop()  # Clicking on the loop
            self.better_sleep((1, 2))

            self.click(uniform(225, 285), uniform(607, 667))  # Selecting the barbarian section
            self.better_sleep((1, 1.3))
            self.set_search_level(wanted_level)  # Setting the barbarian level to the desired level

            self.click(uniform(200, 330), uniform(466, 506))  # Searching the barbarian
            self.better_sleep((1, 2))

            reduced_level = wanted_level
            while self.find_img(target="search_button") is not None:
                reduced_level = reduced_level - 1
                self.set_search_level(reduced_level)

                x, y = uniform(200, 330), uniform(466, 506)
                self.click(x, y)  # Searching the barbarian

                self.better_sleep((1, 2))
            wanted_level = reduced_level

            self.click(1280 // 2 + uniform(-10, 10), 720 // 2 + uniform(-10, 10))  # Selecting the barbarian
            self.better_sleep((1, 1.4))

            button_attack = self.find_img(target="attack_button")
            if button_attack is None:
                continue  # Skipping all the code bellow to re-execute the barbarian search
            self.click(button_attack[0] + uniform(0, 170), button_attack[1] + uniform(0, 40))
            self.better_sleep((1.5, 2))

            if not hunter_selection:
                self.print(f"Selecting the whole troops from scratch")
                self.better_sleep((2, 3))
                self.click(uniform(1163, 1180), uniform(670, 685))
                self.better_sleep((2.2, 3.5))
                tab = self.adb.find_multiple_img("selected_icon")
                if tab:
                    tab = tab[nb_hunter:-1]
                    for element in tab:
                        x, y = element[0] + uniform(0, 5), element[1] + uniform(0, 5)
                        self.click(x, y)
                        self.better_sleep((0.3, 0.5))
                    hunter_selection = True
                    one_hunter = False
                    self.click(uniform(1163, 1183), uniform(665, 685))
                    self.better_sleep((1.2, 1.5))
                else:
                    hunter_selection = True
                    one_hunter = True
            if not one_hunter:
                self.print("Selecting all the troops")
                self.click(uniform(1163, 1183), uniform(665, 685))
                self.better_sleep((2, 3))
            else:
                self.print("Selecting the single march..")
                self.click(uniform(1200, 1220), uniform(210, 230))
                self.better_sleep((2, 3))
            if co := self.find_img("march_bar"):
                self.click(co[0] + uniform(0, 30), co[1] + uniform(0, 10))
                self.better_sleep((2, 3))
            self.print(f"Check if AP pop-op box is detected")
            if self.check_ap_box():
                self.print("Pop-up found, recalling troops")
                break

            self.check_captcha()
            self.wait_until_kill()
        self.check_ap_box()
        self.better_sleep((2, 3))
        self.recall(nb_troop=nb_hunter)
