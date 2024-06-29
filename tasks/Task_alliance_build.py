from random import randint, uniform
from time import sleep

from tasks.Task import Task
from utils.functions import get_class, get_name


class AllianceBuilding(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)

    def task_name(self):
        return "AllianceFlag"

    @get_name
    def open_territory_menu(self) -> None:
        source = self.adb.get_cv2_img()
        co = self.find_img(source=source, target="alliance_flag1", confidence=0.9)
        if co is None:
            co = self.find_img(source=source, target="alliance_flag2", confidence=0.9)
        if co is None:
            return
        self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 10))
        self.better_sleep((1.0, 1.395))

    @get_name
    def is_pit_ready(self):
        screen = self.adb.get_cv2_img()
        alliance_pits = self.find_img(target="alliance_pits", source=screen, confidence=0.79)
        if not alliance_pits:
            return False

        is_alliance_pit_expended = self.find_img(
            target="is_alliance_pit_expended",
            source=screen[alliance_pits[1] + 15 : alliance_pits[1] + 40, 1076:1151],
            confidence=0.75,
        )
        if not is_alliance_pit_expended:
            self.click(alliance_pits[0], alliance_pits[1])
            self.better_sleep((1, 2))

        available_to_gather = self.find_img("pit_gathering", confidence=0.75)
        if not available_to_gather:
            return False
        self.click(available_to_gather[0], available_to_gather[1] - 20)
        self.better_sleep((5, 9))
        return True

    @get_name
    def open_alliance_menu(self):
        # Open du menu
        self.open_menu()
        # Open alliance menu
        x, y = uniform(1010, 1050), uniform(650, 690)
        self.click(x, y)
        self.better_sleep((1.725, 2.295))

    @get_name
    def donate_to_alliance(self):
        alliance_tech_logo = self.find_img(target="alliance_tech")
        if alliance_tech_logo is not None:
            self.click(
                alliance_tech_logo[0] + uniform(0, 30),
                alliance_tech_logo[1] + uniform(0, 15),
            )
            self.better_sleep((2, 3))
            donation_logo = self.find_img(target="tech_2", confidence=0.97)
            # if donation_logo is None:
            # donation_logo = self.find_img(target="tech_2",confidence=0.97)
            if donation_logo is not None:
                self.click(donation_logo[0] + uniform(0, 10), donation_logo[1] + uniform(0, 10))
                self.better_sleep((1, 2))
                # Holding click on the donation button
                talked = False
                while self.find_img(target="donate_button"):
                    if not talked:
                        self.print("Donating to the alliance")
                        talked = True
                    x, y, arg = (
                        uniform(910, 1040),
                        uniform(550, 580),
                        randint(2500, 3475),
                    )
                    self.swipe_arg(x, y, x, y, arg)
                    self.better_sleep((0.7, 1.3))
                # Check if the resources pop-up comes
                if self.find_img(target="get_more_rss") is not None:
                    self.click(uniform(1000, 1020), uniform(129, 148))
                    self.better_sleep((1, 1.425))
                self.click(uniform(1080, 1100), uniform(70, 90))
                self.better_sleep((1, 1.425))

            x, y = uniform(1100, 1130), uniform(60, 80)
            self.click(x, y)
            self.better_sleep((1.8, 2.125))

    @get_name
    def click_on_pit(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        self.print("Clicking on the pit..")
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
            self.print("Unable to click on the pit !", "red")
            return False

    @get_name
    def send_troop(self) -> bool:
        self.better_sleep((1.8, 3))
        self.print("Trying to send a new troop..")
        self.send_new_troop()
        self.better_sleep((0.7, 1.1))

        if self.find_img(target="troops_march_button") is not None:
            self.click(uniform(1106, 1123), uniform(36, 55))
            self.better_sleep((1.1, 1.5))
            self.print("Cannot send the troop")
            return False
        self.print("Troop sent !", "green")
        return True

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
                self.send_discord_message("Error in line-up selection, human interaction required.")
                while True:
                    self.script_pause()
                    sleep(0.1)
            self.click(uniform(1092, 1114), uniform(190, 200))
            self.better_sleep((0.557, 0.796))
            deadstop = deadstop + 1
            self.print("Switching between line-up..")

    @get_name
    def send_new_troop(self, deadstop: int = 0, color: str = "yellow") -> bool:
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
                # x_click, y_click = uniform(1090, 1111), uniform(329, 348)
                # self.better_sleep((1.225, 1.795))

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
            print(e)
            self.print(e)
            self.print("Error sending a new march to the rss node !", "red")

    def close_all_collapible(self):
        """
        Close all the collapible menu
        """
        screen = self.adb.get_cv2_img()

        images = self.adb.find_multiple_img("is_alliance_pit_expended", confidence=0.79, source=screen[0:720, 1076:1151])
        if images:
            for image in images:
                self.click(image[0] + 1076, image[1])
                self.better_sleep((0.7, 1.1))

    @get_class
    def run(self):
        self.open_alliance_menu()
        self.open_territory_menu()
        self.better_sleep((1, 2))

        self.close_all_collapible()

        self.better_sleep((1, 2))

        if not (co := self.find_img(target="alliance_building_alert_icon")):
            self.print("No Alliance build available.", "red")
            return self.close_windows()

        self.click(co[0], co[1] + 30)
        self.better_sleep((1.3, 2))

        if co := self.find_img(target="join_fortress_icon"):
            self.click(co[0], co[1])
            self.better_sleep((1.3, 2))

        self.send_troop()
