from random import choice, uniform

from tasks.Task import Task, get_name
from tasks.Task_alliance_help import AllianceHelp
from utils.functions import get_class


class AcademyResearch(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.academic_research

    def task_name(self):
        return "AcademyResearch"

    @get_name
    def academy_coordinates(self):
        return self.context_task.academy_position

    @get_name
    def enter_academy(self):
        for _ in range(2):
            academy_coordinates = self.academy_coordinates()
            self.click(academy_coordinates.x, academy_coordinates.y)
            self.better_sleep((0.9, 1.5))
        if self.find_img("building_speedups") is None:
            if co := self.find_img("academy"):
                self.click(co[0] + uniform(0, 20), co[1] + uniform(0, 20))
                self.better_sleep((0.9, 1.5))
                return True
            else:
                return False
        else:
            self.print("Academy already researching")
            return False

    @get_name
    def select_tech(self, swipes=0):
        source = self.adb.get_cv2_img()
        techs = self.adb.find_multiple_img(target="research_tech", source=source, confidence=0.7)
        cards = self.adb.find_multiple_img(target="research_card", source=source, confidence=0.9)

        duos = set()
        for card in cards:
            for tech in techs:
                if (card[1] > tech[1] > card[1] - 50) and (card[0] + 50 > tech[0] > card[0] - 100):
                    duos.add(card)

        if duos:
            co = choice(list(duos))
            self.click(co[0] + uniform(-5, 5), co[1] + uniform(-5, 5))
            self.better_sleep((0.9, 1.2))
            self.research_tech()
            self.better_sleep((0.9, 1.2))
        else:
            if swipes < 5:
                self.swipe_right_low()
                self.better_sleep((3, 3.5))
                return self.select_tech(swipes + 1)
            else:
                return

    @get_name
    def research_tech(self):
        self.click(uniform(950, 1040), uniform(510, 555))
        self.better_sleep((0.9, 1.2))

    @get_class
    def run(self):
        if self.academy_coordinates() and self.enter_academy():
            self.better_sleep((0.9, 1.2))
            if self.adb.find_img("tech_speedup") is None:
                self.click(73, 178)
                self.better_sleep((0.9, 1.2))
                self.select_tech()
            self.close_windows()
            self.better_sleep((5, 9))
            AllianceHelp(self).run()
