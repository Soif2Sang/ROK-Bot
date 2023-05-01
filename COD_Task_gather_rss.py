import json
from time import sleep

import numpy as np
from PIL import Image
from numpy import array
from random import uniform

import cv2
from pytesseract import pytesseract

from COD_Task import Task
from Task_utils import get_name, current_time, get_class, get_data

pytesseract.tesseract_cmd = r'.\\tesseract\\tesseract.exe'

class CodGatherRss(Task):
    def __init__(self, MainTask: Task):
        super().__init__(MainTask.tile)
        self.data = get_data()
        self.current_profile = MainTask.current_profile
        self.frame = MainTask.tile
        self.adb = MainTask.adb
        self.ppid = MainTask.ppid
        self.pid = MainTask.pid
        self.language = MainTask.language
        self.name = MainTask.name
        self.sel = MainTask.sel

    def task_name(self):
        return "GatherRss"

    @get_name
    def leave_city_simple(self) -> bool:
        """
        -Enter and leave city if not in city
        -Leave city if in city
        """
        print(f'[ {current_time()} ] [ {self.name} ] leave_city_simple call')
        if self.in_city():
            print(f'[ {current_time()} ] [ {self.name} ] quiting city')
            self.click(uniform(24, 91), uniform(625, 680))
            self.better_sleep((1.5, 3))
        return True

    @get_name
    def free_troop(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """
        pil_image = self.adb.get_curr_device_screen_img()
        cv_image =self.pil_to_array(pil_image)
        cropped_image3 = cv_image[162:179, 1210:1242]
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2HSV)
        # cropped_image1 = cv_image[162:179, 1212:1224]
        # cropped_image2 = cv_image[162:178, 1228:1241]
        # cropped_image3 = cv_image[162:179, 1210:1242]
        # cv_image1 = cv2.cvtColor(cropped_image1, cv2.COLOR_BGR2GRAY)
        # cv_image2 = cv2.cvtColor(cropped_image2, cv2.COLOR_BGR2GRAY)
        # cv2.imwrite("test1.png", cropped_image1)
        # cv2.imwrite("test2.png", cropped_image2)
        # cv2.imwrite("test3.png", cropped_image3)
        native_text = pytesseract.image_to_string(cropped_image3,
                                                  config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # text1 = pytesseract.image_to_string(cropped_image1,
        #                                     config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # text2 = pytesseract.image_to_string(cropped_image2,
        #                                     config=r'--oem 1 --psm 13 -c tessedit_char_whitelist=12345670/')
        # print(text0)
        # text1 = text1.replace("\n", "")
        # text2 = text2.replace("\n", "")
        # print(f"Text 1 : {text1} , Text 2 : {text2}")
        # self.set_text(f'[{current_time()}] Text 1 : {text1} , Text 2 : {text2}')
        # print(len(text1), len(text2))
        # logging.info(f"[{self.name}] Text 1 : {text1} , Text 2 : {text2}")
        # logging.info(f"[{self.name}] len(text1) : {len(text1)}, len(text2) : {len(text2)}")
        # if text1 == "" or text2 == "":
        #     return True
        print(f"[ {current_time()} ] [ {self.name} ] {native_text =}")
        if "/" in native_text:
            # list_text = text0.split("/")
            enhanced_text = native_text.split("/")[0] + native_text.split("/")[1]
        else:
            enhanced_text = native_text
        enhanced_text = enhanced_text.replace("\n", "")
        print(f"[ {current_time()} ] [ {self.name} ] {enhanced_text =}")
        if len(enhanced_text) < 2:
            return True
        if len(enhanced_text) == 2:
            return enhanced_text[0] < enhanced_text[1]
        # return text1 < text2 if len(text1) == 1 and len(text2) == 1 else False

    @get_name
    def click_loop(self) -> None:
        if not self.find_img(target="cod_search_loop"):
            self.leave_city()
            self.better_sleep((2, 3))
        self.click(uniform(33, 76), uniform(517, 560))
        self.better_sleep((2, 4))

    @get_name
    def select_resource_type(self, place: str) -> tuple[float, float]:
        gold_icon = ((400, 472), (632, 663))
        wood_icon = ((598, 670), (632, 663))
        stone_icon = ((823, 870), (632, 663))
        mana_icon = ((1020, 1060), (632, 663))
        if self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "gold":
            x, y = uniform(gold_icon[0][0], gold_icon[0][1]), uniform(gold_icon[1][0], gold_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "wood":
            x, y = uniform(wood_icon[0][0], wood_icon[0][1]), uniform(wood_icon[1][0], wood_icon[1][1])
        elif self.data[str(self.sel)]['schedules'][self.current_profile].get(place) == "stone":
            x, y = uniform(stone_icon[0][0], stone_icon[0][1]), uniform(stone_icon[1][0], stone_icon[1][1])
        else:  # Gold
            x, y = uniform(mana_icon[0][0], mana_icon[0][1]), uniform(mana_icon[1][0], mana_icon[1][1])
        # print(f'[ {current_time()} ] [ {self.name} ] chance rss type call')
        return x, y

    @get_name
    def set_search_level(self, level: int = 10) -> None:
        cv_image = self.adb.get_cv2_img()
        co = self.find_img(source=cv_image, target="cod_level_slider", confidence=0.8)
        if co is None:
            self.print(f'Cannot find the button_level')
            # self.set_text(f"[{current_time()}] Cannot find the level button")
            self.click_loop()
            self.better_sleep((1, 1.7))
        else:
            # x,y = uniform(225,285) , uniform(607,667)
            # self.click(x,y)
            cv_image = cv_image[co[1] - 30:co[1] -5, co[0] - 80:co[0] + 80]
            # cv2.imwrite("level.png", cv_image)
            string = pytesseract.image_to_string(cv_image,
                                                 config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=level:1234567890')
            print(string)
            string = string.replace("\n", "")
            # self.set_text(f"[{current_time()}] Current level : {string[1]}")
            try:
                level_to_go = level - int(string[-1])
                self.print(f'Current level : {string[-1]}')
            except:
                x, y = self.find_img(target='cod_search_minus_button')
                for i in range(6):
                    self.click(x+ uniform(0, 20),y +uniform(0, 20))
                    self.better_sleep((0.450, 1))
                level_to_go = level
            if level_to_go > 0:
                word = "Increasing"
                x, y = self.find_img(target='cod_search_plus_button')
            else:
                word = "Decreasing"
                x, y = self.find_img(target='cod_search_minus_button')
            self.print(f'{word} the level by : {abs(level_to_go)}')
            # self.set_text(f"[{current_time()}] {word} the level by : {abs(level_to_go)}")
            for _ in range(abs(level_to_go)):
                x2 = x + uniform(0, 30)
                y2 = y + uniform(0, 27)
                self.click(x2, y2)
                self.better_sleep((0.450,1))
            return

    @get_name
    def node_found(self) -> bool:
        if self.find_img(target='cod_search_button') is not None:
            self.print("Node not found")
            return False
        return True

    @get_name
    def click_search_adapted_node(self, place: str) -> None:
        self.print(f"Looking for : {self.data[str(self.sel)]['schedules'][self.current_profile].get(place)} {place}")
        co = self.find_img("cod_search_button")
        self.click(co[0], co[1])

    @get_name
    def minable(self) -> bool:
        if self.find_img(target="search_button") is None:
            return True
        # self.print("Unable to gather this node")
        return False

    @get_name
    def find_cross(self) -> bool:
        """
        :return: True if node is occupied or someone is coming to the node
        :return: False if node is free to gather
        """
        self.print("Scanning the node..")
        cv_image = self.adb.get_cv2_img()
        cropped_image = cv_image[230:480, 441:814]
        img = Image.fromarray(cropped_image)
        for i in range(img.size[0]):
            for y in range(img.size[1]):
                if (((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] < 5) and (img.getpixel((i, y))[2] > 175) and (img.getpixel((i, y))[2] < 196) and ((img.getpixel((i, y))[0] != 2) and (img.getpixel((i, y))[1] != 4) and (
                             img.getpixel((i, y))[2] != 183)))
                        or
                        ((img.getpixel((i, y))[0] == 233) and (img.getpixel((i, y))[1] == 233) and (img.getpixel((i, y))[2] == 233)) or
                        ((img.getpixel((i, y))[0] == 247) and (img.getpixel((i, y))[1] == 156) and (
                                img.getpixel((i, y))[2] == 47)) or
                        ((img.getpixel((i, y))[0] == 207) and (img.getpixel((i, y))[1] == 131) and (
                                img.getpixel((i, y))[2] == 40)) or
                        ((img.getpixel((i, y))[0] == 248) and (img.getpixel((i, y))[1] == 157) and (
                                img.getpixel((i, y))[2] == 48)) or
                        ((img.getpixel((i, y))[0] == 239) and (img.getpixel((i, y))[1] == 205) and (
                                img.getpixel((i, y))[2] == 165)) or
                        ((img.getpixel((i, y))[2] < 179) and (img.getpixel((i, y))[2] > 175) and (
                                img.getpixel((i, y))[1] > 116) and (img.getpixel((i, y))[1] < 119) and (
                                 img.getpixel((i, y))[0] < 2)) or
                        ((img.getpixel((i, y))[0] < 5) and (img.getpixel((i, y))[1] > 144) and (img.getpixel((i, y))[1] < 150) and (img.getpixel((i, y))[2] < 200) and (img.getpixel((i, y))[2] > 190)) or
                        (img.getpixel((i, y)) == (0, 0, 178)) or
                        (img.getpixel((i, y)) == (2, 204, 2)) or
                        (img.getpixel((i, y)) == (195, 142, 0)) or
                        (img.getpixel((i, y)) == (0, 154, 14)) or
                        (img.getpixel((i, y)) == (0, 154, 13)) or
                        (img.getpixel((i, y)) == (1, 186, 0)) or
                        (img.getpixel((i, y)) == (0, 142, 193)) or
                        (img.getpixel((i, y)) == (12, 154, 1)) or
                        (img.getpixel((i, y)) == (1, 215, 0)) or
                        (img.getpixel((i, y)) == (1, 215, 0)) or
                        (img.getpixel((i, y)) == (1, 216, 0)) or
                        (img.getpixel((i, y)) == (253, 253, 253)) or
                        (img.getpixel((i, y)) == (49, 161, 255)) or
                        (img.getpixel((i, y)) == (2, 197, 2)) or
                        (img.getpixel((i, y)) == (247, 210, 167)) or
                        (img.getpixel((i, y)) == (255, 161, 49)) or
                        (img.getpixel((i, y)) == (253, 253, 253)) or
                        img.getpixel((i, y)) in [(167, 121, 28), (28, 121, 167)]):
                    self.print(f"{img.getpixel((i, y))}")
                    self.print("Node occupied","red")
                    return True
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
                    sleep(1)
            self.click(uniform(1092, 1114), uniform(225, 248))
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

        self.print("Trying to send new troop..")
        print(f"[ {current_time()} ] [ {self.name} ] Send new troop count : {deadstop}")
        if deadstop == 5:
            self.click(uniform(700, 800), uniform(300, 500))
            self.better_sleep((1.325, 1.795))
            return False
        co = self.find_img(target="cod_create_legion")
        if co is not None:
            # print("Home button found")
            x, y = co[0], co[1]
            x, y = x + uniform(0, 20), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((1.825, 2.495))
            co = self.find_img(target="cod_march_button")
            if co is None:
                return self.send_new_troop(deadstop=deadstop + 1)
            x, y = co[0], co[1]
            x, y = x + uniform(0, 20), y + uniform(0, 20)
            self.click(x, y)
            self.better_sleep((0.5, 0.7))
        co = self.find_img(target="cod_march_button")
        if co is not None:
            self.close_windows()
            self.print("Unable to send a new troop", "red")
            return False
        else:
            self.print("New Troop sent !","green")
            return True


    @get_name
    def free_troop_gem(self) -> bool:
        """
        :return: True if there's a empty queue
        :return: False if queues are occupied
        """

        pil_image = self.adb.get_curr_device_screen_img()
        cv_image =self.pil_to_array(pil_image)
        cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
        cropped_image = cv_image[13:35, 1225:1254]
        cv_image = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
        text = pytesseract.image_to_string(cv_image)
        text = text.replace("\n", "")
        if len(text) == 3:
            if text[0] < text[2]:
                self.print("Empty queue found")
                return True
            else:
                return False
        else:
            return False
        # return text[0] < text[2] if len(text) == 3 else False

    @get_name
    def click_on_node(self) -> bool:
        """
        Click on node and click on send troop menu
        :return: True is successful
        :return: False is not successful
        """
        i = 0
        self.print("Clicking on the node..")
        while self.find_img(target="cod_gather_button") is None:
            x, y = uniform(610, 650), uniform(340, 388)
            self.click(x, y)
            self.better_sleep((0.995,1.4))
            i = i + 1
            if i == 4:
                return False
        self.better_sleep((1.0, 1.395))
        co = self.find_img(target="cod_gather_button")
        if co is not None:
            x, y = co[0], co[1]
            self.click(x + uniform(0, 50), y + uniform(0, 30))
            self.better_sleep((1.325, 2.795))
            return True
        else:
            self.print("Unable to click on the node, leaving the node !")
            return False

    @get_name
    def send_troop(self) -> bool:
        self.better_sleep((1.8,3))
        self.print("Trying to send a new troop..")
        co = self.find_img(target="cod_create_legion")
        if co is None:
            return False
        x, y = co[0], co[1]
        x, y = x + uniform(0, 160), y + uniform(0, 30)
        self.click(x, y)
        self.better_sleep((2.325, 2.795))
        x, y = self.find_img(target="cod_march_button")
        x, y = x + uniform(0, 80), y + uniform(0, 20)
        self.click(x, y)
        self.better_sleep((1.1,2))
        if self.find_img(target="cod_march_button") is not None:
            self.close_windows()
            self.print("Cannot send the troop")
            return False
        self.print("Troop sent !","green")
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
    def run(self, node_type=None, level_decrease=0):
        # self.run_game()
        # self.check_reconnect()
        # self.check_log_back()
        # self.check_download_page()
        if node_type is None:
            node_type = "First"
        if node_type == "Done":
            self.click(uniform(600,700),(uniform(250,400)))
            self.better_sleep((2, 4))
            return
        if self.data[str(self.sel)]['schedules'][self.current_profile][node_type] == 'nothing':
            return
        self.leave_city_simple()
        # self.better_sleep((2, 4))
        # Vérifie si y'a une troupe
        if True:
            self.check_log_back()
            self.check_reconnect()
            self.click_loop()
            x, y = self.select_resource_type(node_type)
            # self.better_sleep((1.325, 1.795))
            self.click(x, y)
            self.better_sleep((1.325, 3.795))


            if self.data.get(self.sel).get('schedules').get(self.current_profile).get(f"{node_type}_level") - level_decrease <= 0:
                node_type = self.next_resource_type(node_type)
                self.print(f"Cannot decrease the current level.. Too low ! next type : {node_type}")
                return self.run(node_type, 0)

            self.set_search_level(self.data.get(self.sel).get('schedules').get(self.current_profile).get(f"{node_type}_level") - level_decrease)
            self.better_sleep((0.925, 2.795))
            self.click_search_adapted_node(node_type)
            self.better_sleep((5,9))

            # Tant que la node trouvée n'est pas minable (pas de cross, plus dans le menu des rss)
            # if not self.minable():

                # self.better_sleep((1.325, 3.795))
                # Si y'a plus de node on return le prochain rss
            if self.node_found() is False:
                self.check_reconnect()
                self.check_log_back()
                self.click((1280 // 2) + uniform(-20, 20), (720 // 3) +uniform(-20, 20))
                self.better_sleep((1.325, 3.795))
                if level_decrease >=1:
                    self.print("No node matched the requirements, changing node type..")
                    return self.run(self.next_resource_type(node_type), 0)
                else:
                    self.print(f"{level_decrease+1 = }, {node_type = }")
                    self.print("No node matched the requirements, reducing the level..")
                    return self.run(node_type, level_decrease + 1)
                # self.better_sleep((5, 9))
            self.check_reconnect()
            self.check_log_back()
            if self.click_on_node() and not self.send_troop():
                self.click(uniform(200, 900), uniform(300, 500))
                self.better_sleep((2.325, 5.795))
                return "Done"
            self.better_sleep((1, 2.895))
            node_type = self.next_resource_type(node_type)
            return self.run(node_type,0)
        # self.click(uniform(22, 90), uniform(625, 675))
        return "Done"
