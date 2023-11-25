from random import shuffle, uniform

from tasks.Task import Task


class TroopTraining(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "TroopTraining"

    def run_upgrade(self):
        names = ['infantry', 'cavalry', 'archery', "siege"]
        pos = {
            "t1": [627, 180],
            "t2": [729, 180],
            "t3": [832, 180],
            "t4": [932, 180],
            "t5": [1032, 180],
        }
        shuffle(names)

        for name in names:
            if (co := self.find_img(target=f"{name}_badge_high_view", confidence=0.60)) is None:
                self.print(f"Unable to locate {name}")
                continue
            for i in range(2):
                self.click(co[0] + uniform(0, 8), co[1] + uniform(20, 35))
                self.better_sleep((1.2, 2.3))

            co = self.validate_co(self.find_img(target="upgrade_button_high_view", confidence=0.8))
            if not co:
                continue
            self.click(co[0] + uniform(90, 100), co[1] + uniform(-15, 0))
            self.better_sleep((1.2, 2.3))
            co = pos["t1"]
            self.click(co[0] + uniform(-15, 15), co[1] + uniform(-15, 15))
            self.better_sleep((1.2, 2.3))
            self.click(uniform(910, 1055), uniform(570, 600))
            self.better_sleep((1.2, 2.3))
            if (co := self.find_img(target=f"get_more_rss")) is not None:
                self.click(uniform(1000, 1020), uniform(129, 148))
                self.better_sleep((1, 1.425))
                self.click(uniform(1080, 1100), uniform(70, 90))
                self.better_sleep((1, 1.425))
            self.close_windows()

    def run(self):
        if self.tile.initial_page.UPGRADE:
            return self.run_upgrade()
        names = ['infantry', 'cavalry', 'archery', "siege"]
        pos = {
            "t1": [627, 180],
            "t2": [729, 180],
            "t3": [832, 180],
            "t4": [932, 180],
            "t5": [1032, 180],
        }
        shuffle(names)
        for name in names:
            if self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_enable"]:
                position = self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_camp"]
                if position is None or len(list(position)) < 2:
                    continue
                for i in range(2):
                    self.click(position[0] + uniform(-8, 8), position[1] + uniform(-8, 8))
                    self.better_sleep((1.2, 3))
                if (co := self.find_img(target=f"{name}_badge", confidence=0.75)) is None:
                    self.print(f"Unable to locate {name}")
                    continue
                if self.find_img(target=f"building_speedups", confidence=0.8) is not None:
                    self.print(f"Already training {name}")
                    continue
                self.click(co[0] + uniform(-8, 8), co[1] + uniform(-8, 8))
                self.better_sleep((1.2, 2.3))
                co = pos[self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"{name}_tier"]]
                self.click(co[0] + uniform(-15, 15), co[1] + uniform(-15, 15))
                self.better_sleep((1.2, 2.3))
                self.click(uniform(910, 1055), uniform(570, 600))
                self.better_sleep((1.2, 2.3))
                if (co := self.find_img(target=f"get_more_rss")) is not None:
                    self.click(uniform(1000, 1020), uniform(129, 148))
                    self.better_sleep((1, 1.425))
                    self.click(uniform(1080, 1100), uniform(70, 90))
                    self.better_sleep((1, 1.425))
                self.close_windows()
