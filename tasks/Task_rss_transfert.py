from time import sleep

from random import uniform

import cv2
from pytesseract import pytesseract

from tasks.Task import Task
from utils.Task_utils import get_name, get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'


class RssTransfer(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = MainTask.data
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "RssTransfert"

    @get_name
    def get_capacity(self):
        """
                :return: True if there's a empty queue
                :return: False if queues are occupied
                """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image = self.pil_to_array(pil_image)
        transport_capacity = cv_image[558:590, 285:435]
        transport_capacity = cv2.cvtColor(transport_capacity, cv2.COLOR_BGR2HSV)
        transport_capacity = pytesseract.image_to_string(transport_capacity,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789/,')

        cv_image = self.pil_to_array(pil_image)
        tax_rate = cv_image[450:480, 374:420]
        tax_rate = cv2.cvtColor(tax_rate, cv2.COLOR_BGR2HSV)
        tax_rate = pytesseract.image_to_string(tax_rate,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=0123456789%,')
        print(tax_rate)
        return int(transport_capacity.split("/")[1].replace(",","")) + (int(transport_capacity.split("/")[1].replace(",",""))*int(tax_rate.replace("%","")) /100)

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
    def setup_ui(self,deadstop = 0):
        if deadstop ==3:
            raise ValueError()

        # city = self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"city_transfer"]
        # print(city)
        if int(self.sel) == 0:
            city = [430,140]
        else:
            city = [220,350]
        self.click(city[0]+uniform(-10,10),city[1]+uniform(-10,10))
        self.better_sleep((1,2))
        co = self.find_img(target="assist_button")
        if co is None:
            self.close_windows()
            return self.setup_ui(deadstop = deadstop+1)
        self.click(co[0]+ uniform(0,40),co[1] + uniform(0,20))
        self.better_sleep((1,2))

    @get_name
    def solve(self,path, sel, defaultApiKey=False):
        return super().solve(path,sel,defaultApiKey)

    @get_name
    def check_captcha(self,chest=True):
        if not chest:
            super().check_captcha(chest)
            sleep(1)
        super().check_captcha(chest)

    @get_name
    def send_rss(self, type):
        types = {'food':uniform(210,230),
                 'wood':uniform(300,320),
                 'stone': uniform(390, 410),
                 'gold':uniform(470,490)}
        start = (uniform(589,597),types[type])
        end = (uniform(1045,1100), types[type]+uniform(-10,10))
        self.swipe(start[0],start[1],end[0],end[1])
        self.better_sleep((0.7,1.4))
        self.click(uniform(700,850),uniform(570,600))
        self.better_sleep((0.7, 1.4))

    @get_class
    def run(self,type = None,quantity = None):
        if self.data[self.sel]['API_KEY'] =="":
            return self.print("This feature require a custom ApiKey")
        self.check_captcha()

        self.setup_ui()
        self.better_sleep((0.7, 1.4))
        transportation_capacity = self.get_capacity()

        print(f"{transportation_capacity = }")
        for type in ["food","wood","stone","gold"]:

            rss_sent = 0
            transfert_wanted = self.data[str(self.sel)]['schedules'][str(self.current_profile)][f"transfer_{type}"] * 1_000_000
            loop = int(transfert_wanted / transportation_capacity)
            if transportation_capacity * loop < transfert_wanted:
                loop += 1
            print(f"{transfert_wanted = }")
            for i in range(loop):

                rss_sent += transportation_capacity
                self.send_rss(type)
                print(f"{type} amount sent : {rss_sent}")
                self.better_sleep((1,2))
                self.check_captcha(chest=True)
                self.setup_ui()


        self.close_windows()