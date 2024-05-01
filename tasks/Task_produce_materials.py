from random import uniform

from tasks.Task import Task
from utils.functions import get_class, rgetattr


class ProduceMaterials(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)
        self.context_task = self.context_profile.tasks.produce_materials

    def task_name(self):
        return "ProduceMaterials"

    @get_class
    def run(self):
        # co = self.find_img("forge_icon")
        # if co is not None:
        #     self.click(co[0] + uniform(0, 24), co[1] + uniform(80, 100))
        #     self.better_sleep((1, 1.5))
        # else:
        strings = [
            "forge_icon",
            "bones_icon",
            "ebony_icon",
            "leather_icon",
            "stone_icon",
        ]

        keys = {
            1 :"first_choice",
            2 :"second_choice",
            3 :"third_choice",
            4 :"fourth_choice",
            5: "fifth_choice",
        }

        # Claim the materials from the forge
        for string in strings:
            co = self.find_img(target=string, confidence=0.8)
            if co is not None:
                if string != "forge_icon":
                    self.click(co[0] + uniform(0, 24), co[1] + uniform(0, 24))
                    self.better_sleep((1, 1.5))
                self.click(co[0] + uniform(0, 24), co[1] + uniform(80, 100))
                self.better_sleep((1, 1.5))
                break
        co = self.find_img(target="forge_button")
        if co is not None:
            self.click(co[0] + uniform(0, 50), co[1] + uniform(0, 60))
            self.better_sleep((1, 1.5))
            cv_image = self.adb.get_cv2_img()

            number_of_available_slots = 0
            for i in range(1, 6):
                co = self.find_img(target=f"forge_{i}", source=cv_image, confidence=0.9)
                if co is not None:
                    number_of_available_slots = 6 - i
                    break

            if number_of_available_slots != 0:
                for i in range(1, number_of_available_slots + 1):

                    materials = {
                        "leather": (uniform(737, 785), uniform(208, 255)),
                        "stone": (uniform(830, 880), uniform(208, 255)),
                        "ebony": (uniform(922, 972), uniform(208, 255)),
                        "bones": (uniform(1018, 1064), uniform(208, 255)),
                    }


                    type = rgetattr(self.context_task, keys[i]).type
                    self.print(f"Producing {type}")
                    self.click(materials[type][0], materials[type][1])
                    self.better_sleep((0.5, 1.2))
            self.close_windows()
