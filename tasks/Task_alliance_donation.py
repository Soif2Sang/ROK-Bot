import random
from random import randint, uniform

from tasks.Task import Task
from utils.functions import get_class, get_name


class AllianceDonation(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.sel, MainTask.contextManager)
        self.herite(MainTask)

    def task_name(self):
        return "AllianceDonation"

    @get_name
    def collect_alliance_resources(self) -> None:
        source = self.adb.get_cv2_img()
        co = self.find_img(source=source, target="alliance_flag1", confidence=0.9)
        if co is None:
            co = self.find_img(source=source, target="alliance_flag2", confidence=0.9)
        if co is None:
            return
        self.print("Collecting the alliance resources")
        self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 10))
        self.better_sleep((1.0, 1.395))
        x, y = uniform(955, 1067), uniform(122, 150)
        self.click(x, y)
        self.better_sleep((0.78, 1.095))
        x, y = uniform(1100, 1130), uniform(30, 58)
        self.click(x, y)
        self.better_sleep((1.0, 1.395))

    @get_name
    def donate_to_alliance(self):
        alliance_tech_logo = self.find_img(target="alliance_tech")
        if alliance_tech_logo is not None:
            self.click(
                alliance_tech_logo[0] + uniform(0, 30),
                alliance_tech_logo[1] + uniform(0, 15),
            )
            self.better_sleep((2, 3))

            source = self.adb.get_cv2_img()

            missing_steps = self.adb.find_multiple_img(target="tech", source=source, confidence=0.7)
            bottom_corners = self.adb.find_multiple_img(target="research_card", source=source, confidence=0.9)
            recommendation_badge = self.find_img(target="donation_recommendation", source=source, confidence=0.79)

            technologies_to_donate = set()
            recommended_technology = None
            
            for card in bottom_corners:
                for tech in missing_steps:
                    if (card[1] > tech[1] > card[1] - 50) and (card[0] + 50 > tech[0] > card[0] - 100):
                        if recommendation_badge:
                            if (recommendation_badge[1] + 80 > tech[1] > recommendation_badge[1] +150) and (recommendation_badge[0] + 90 > tech[0] > recommendation_badge[0] - 300):
                                recommended_technology = card
                        technologies_to_donate.add(card)
                        

            print(f"{recommended_technology= }")
            print(f"{technologies_to_donate= }")

            technologies_to_donate = list(technologies_to_donate)
            random.shuffle(technologies_to_donate)

            if recommended_technology is not None:
                technologies_to_donate.remove(recommended_technology)
                technologies_to_donate.insert(0, recommended_technology)

            nb_check = 0

            for i in range(len(technologies_to_donate)):
                if nb_check == 4:
                    break

                nb_check += 1
                donation_logo = random.choice(list(technologies_to_donate))
                technologies_to_donate.remove(donation_logo)

                self.click(donation_logo[0] + uniform(0, 10), donation_logo[1] + uniform(0, 10))
                self.better_sleep((1, 2))

                if not self.find_img(target="donate_button"):
                    cos = self.adb.find_multiple_img(target="close_window", confidence=0.7)
                    if not cos:
                        self.close_windows()
                        return
                    co = cos[-1]
                    self.adb.click(co[0] + uniform(3, 9), co[1] + uniform(3, 9))
                    self.better_sleep((1.3, 2.8))
                    continue

                # Hold  ing click on the donation button
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
                break

            x, y = uniform(1100, 1130), uniform(60, 80)
            self.click(x, y)
            self.better_sleep((1.8, 2.125))

    @get_class
    def run(self):
        self.open_alliance_menu()
        self.collect_alliance_resources()
        self.donate_to_alliance()
        self.close_windows()
