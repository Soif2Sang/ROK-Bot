from random import shuffle, uniform
from time import sleep

import cv2

from tasks.Task import Task
from utils.functions import get_class, get_name


class RssTransfer(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.herite(MainTask)

    def task_name(self):
        return "RssTransfert"

    @get_name
    def get_capacity(self):
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        default_image = self.adb.get_cv2_img()
        default_image = cv2.cvtColor(default_image, cv2.COLOR_BGR2GRAY)
        transport_capacity = default_image[558:590, 285:435]
        tax_rate = default_image[450:480, 374:420]

        # cv2.imwrite("transport.png", transport_capacity)
        # cv2.imwrite("tax.png", tax_rate)
        transport_capacity = self.extract_text(transport_capacity, allowlist="0123456789/,")
        transport_capacity = int(transport_capacity.split("/")[1].replace(",", ""))

        tax_rate = self.extract_text(tax_rate, allowlist="0123456789%")
        print(tax_rate)

        tax_rate = tax_rate.replace("%", "")
        if len(tax_rate) == 2 and tax_rate[0] == "8":
            tax_rate = tax_rate[:-1]
        if len(tax_rate) == 3:
            tax_rate = tax_rate[:-1]
        tax_rate = int(tax_rate)

        print(transport_capacity)
        print(tax_rate)
        return transport_capacity * (1 + tax_rate / 100)

    # @get_name
    # def get_capacity(self):
    #     """
    #             :return: True if there's a empty queue
    #             :return: False if queues are occupied
    #             """
    #     pil_image = self.adb.get_curr_device_screen_img()
    #     cv_image = self.pil_to_array(pil_image)
    #     cropped_image3 = cv_image[558:590, 285:435]
    #     cv_image = cv2.cvtColor(cropped_image3, cv2.COLOR_BGR2HSV)
    #     native_text = pytesseract.image_to_string(cv_image,
    #                                               config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789/,')
    #     return int(native_text.split("/")[1].replace(",",""))

    @get_name
    def setup_ui(self, deadstop=0):
        if deadstop == 3:
            raise ValueError()

        city = self.data[str(self.sel)]["schedules"][str(self.current_profile)][f"city_transfer"]
        self.click(city[0] + uniform(-10, 10), city[1] + uniform(-10, 10))
        self.better_sleep((1, 2))
        co = self.find_img(target="assist_button")
        if co is None:
            self.close_windows()
            return self.setup_ui(deadstop=deadstop + 1)
        self.click(co[0] + uniform(0, 40), co[1] + uniform(0, 20))
        self.better_sleep((1, 2))

    @get_name
    def check_captcha(self, chest=True):
        if not chest:
            super().check_captcha(chest=chest, DefaultApiKey=False)
            sleep(1)
        super().check_captcha(chest=chest, DefaultApiKey=False)

    @get_name
    def send_rss(self, type):
        types = {
            "food": uniform(210, 230),
            "wood": uniform(300, 320),
            "stone": uniform(390, 410),
            "gold": uniform(470, 490),
        }
        start = (uniform(589, 597), types[type])
        end = (uniform(1045, 1100), types[type] + uniform(-10, 10))
        self.swipe(start[0], start[1], end[0], end[1])
        self.better_sleep((0.1, 1.4))
        self.click(uniform(700, 850), uniform(570, 600))
        self.better_sleep((0.1, 1.4))

    @get_name
    def better_sleep(self, limits: tuple[float, float]):
        if self.data[str(self.sel)]["schedules"][self.current_profile].get("fast_rss_transfer", False):
            a = limits[0]
            if self.data[str(self.sel)]["schedules"][self.current_profile]["slow_mode"]:
                a *= self.data[str(self.sel)]["schedules"][self.current_profile]["sleep_multiplicator"]

            interval_duration = 0.01  # Durée de chaque intervalle (en secondes)
            num_intervals = int(a / interval_duration)

            for _ in range(num_intervals):
                sleep(interval_duration)
                self.script_pause()
            return
        return super().better_sleep(limits)

    @get_class
    def run(self, type=None, quantity=None):
        if self.data["API_KEY"] == "":
            self.generate_toast(
                "Warning",
                "This feature require a custom ApiKey.",
            )
            return self.print("This feature require a custom ApiKey")
        self.check_captcha()

        self.setup_ui()
        self.better_sleep((0.7, 1.4))
        transportation_capacity = self.get_capacity()

        print(f"{transportation_capacity = }")
        to_send = []
        for type in ["food", "wood", "stone", "gold"]:
            transfert_wanted = self.data[str(self.sel)]["schedules"][str(self.current_profile)][f"transfer_{type}"] * 1_000_000
            loop = int(transfert_wanted / transportation_capacity)
            if transportation_capacity * loop < transfert_wanted:
                loop += 1
            print(f"{transfert_wanted = }")
            for i in range(loop):
                to_send.append(type)

        shuffle(to_send)
        total_sent = {"food": 0, "wood": 0, "stone": 0, "gold": 0}
        for type in to_send:
            total_sent[type] += transportation_capacity
            self.send_rss(type)
            print(f"{type} amount sent : {total_sent[type]}")

            if self.data[str(self.sel)]["schedules"][self.current_profile].get("fast_rss_transfer", False):
                self.check_captcha(chest=False)
            else:
                self.check_captcha(chest=True)

            self.setup_ui()

        self.close_windows()
