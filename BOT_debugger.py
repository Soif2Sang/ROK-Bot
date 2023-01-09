from bot_adb import *
from tasks_lib import *
#from rkp import *
#from auto_upgrade import *

with open('user_settings.json') as config_file: data = json.load(config_file)
# with open('rkp_list.json') as config_file: data_rkp = json.load(config_file)

class Frame():
    def __init__(self, adb):
        self.adb = adb

class Bot():
    def __init__(self,adb):
        self.adb=adb
        self.device= adb.get_device()
        self.task= Tasks(Frame(self.adb)) #tasksGEM / tasks
        #self.task = Tasks(self.adb)
        self.task.set_sel(str(adb.number))
        #self.rkp = Rkp(self.adb)
        #self.rkp.set_sel('4')
        #self.up = Up(self.adb)
        #self.rkp.set_sel('3')

def lerp(p1: tuple, p2: tuple, points: int) -> list:
    '''
    Creates a list of points with len = points between p1 and p2 using lineal interpolation

    :param p1: First point.
    :param p2: Second point.
    :param points: Number of points in between.
    '''

    output = []
    header = [_p2 - _p1 for _p1, _p2 in zip(p1, p2)]
    for p in range(points + 1):
        percent = p / points
        output.append((p1[0] + percent * header[0], p1[1] + percent * header[1]))
    print(output)
    return output

class AdbInput:
    """
    Sends input events to a given adb device using ppadb and the sendevent shell command.
    """

    def __init__(self, bot : Bot, device: int = 0, eventId: int = 4):
        '''
        Creates an AdbInput object able to send inputs to an adb device
        :param client: The adb client.
        :param device: The index of the device (Default is 0)
        :param eventId: The event id. (Default is 2, change it if your device doesnt work)
        '''
        self.device = bot.device
        self.eventId = eventId

    def sendEvent(self, event: str):
        """
        Sends a raw adb event.
        :param event: The event. Composed by 3 DECIMAL numbers: Type Event Value
        """
        self.device.shell(f'sendevent /dev/input/event{self.eventId} {event}')

    def startTouch(self):
        """
        Starts a touch secuence
        (if you want to tap or swipe, use the functions \"tap\", \"swipe\" or \"smoothSwipe\")
        """

        # self.sendEvent('1 330 1')  # BTN_TOUCH Down
        # self.sendEvent('3 57 10')  # PRESSURE

    def setPosition(self, position: tuple):
        """
        Sends the POSITION_X and POSITION_Y events
        (if you want to tap or swipe, use the functions \"tap\" and \"swipe\")
        """

        self.sendEvent(f'3 53 {position[0]}')  # POSITION_X
        self.sendEvent(f'3 54 {position[1]}')  # POSITION_Y

    # Input functions
    def tap(self, position: tuple, duration: float = 0):
        """
        Taps the screen in the given location for a specific duration.
        :param position: The position to touch.
        :param duration: The duration of the tap.
        """

        # Start Tap
        self.startTouch()
        self.setPosition(position)
        self.sendEvent('0 0 0')  # SYN_REPORT
        self.device.shell(f'sleep {duration}')

        # End Tap
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')  # SYN_REPORT

    def swipe(self, positions: list):
        """
        Swipes in the screen going to the positions really fast
        :param positions: The points to reach
        """
        # Start the swipe
        self.startTouch()
        print("test")
        # Cycle through the positions
        for pos in positions:
            print(f"{pos = }")
            self.setPosition(pos)
            self.sendEvent('0 0 0')  # SYN_REPORT

        # End swipe
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')  # SYN_REPORT

    def smoothSwipe(self, positions: list, wait: float = 0, smoothness: int = 100):
        '''
        Swipes in the screen going to the positions \"smoothly\".

        :param positions: The points to reach.
        :param wait: The wait between touches (recomend using 0 or something really close)
        :param smoothness: The number of extra points added to each path to smooth it (Default = 10)
        '''

        # Get the needed points
        points = []
        for p in range(1, len(positions)):
            points += lerp(positions[p - 1] , positions[p] , smoothness)

        # Start swipe
        self.startTouch()

        # Cylce through points waiting the needed
        for point in points[:-1]:
            print(f"{point = }")
            self.setPosition(point)
            self.sendEvent('0 0 0')
            # self.device.shell(f'sleep {wait}')

        # End swipe
        self.sendEvent('1 330 0')  # BTN_TOUCH Up
        self.sendEvent('0 0 0')
        self.sendEvent('0000 0002 00000000')
        self.sendEvent('0000 0000 00000000')# SYN_REPORT
        self.sendEvent('0000 0002 00000000')
        self.sendEvent('0000 0000 00000000')# SYN_REPORT


if __name__ == "__main__":
    # Create client and AdbInput
    adb = Adb(1)
    bot = Bot(adb)
    bot.adb.connect_to_device()

    print(isinstance(array(bot.adb.get_curr_device_screen_img()), ndarray))
    # bot.task.send_nearest_troop_gem()
    # print(bot.adb.find_img("rokicon",0.8))
    # print(bot.task.run_game())
    # touch = AdbInput(bot, 4)
    # bot.task.heal_troops()
    # bot.task.current_profile="1"
    # print(change_resource_type("Second"))
    # 140 204
    # Touch
    # touch.smoothSwipe([(3600, 3000), (3600, 10000)])
    # def swipe(arg):
    #     final = []
    #     for tuples in arg:
    #         x = tuples[0] * (3600/140)
    #         y = tuples[1] * (9400/204)
    #         final.append((x,y))
    #     touch.smoothSwipe(final)
    # # bot.task.send_new_troop()
    # cos = bot.adb.find_multiple_img("choose_right", 0.8)
    # final = []
    # for co in cos:
    #     if co[0]>1060 and co[1]>200:
    #         final.append(co)
    # print(final)
    # threading.Thread(target=swipe, args=([(970, 395), (225, 395)],)).start()
    # threading.Thread(target=swipe, args=([(225, 300), (970, 300)],)).start()
    # Thread(target = swipe, arg=[(970, 395), (225, 395)]).start()
    # swipe([(225, 300), (970, 300)])
    # touch.smoothSwipe([(140, 140),
    # (140, 204)])
    # touch.smoothSwipe([(30000, 3000), (3600, 10000)])
    # touch.swipe([(200, 200), (200, 300), (300, 300)])


# # bot.task.leave_city_simple()
# pil_image = bot.adb.get_curr_device_screen_img()
# cv_image = array(pil_image)
# cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
# cropped_image = cv_image[541:568, 265:434]
# # cv2.imwrite("timer.png", cropped_image)
# string = pytesseract.image_to_string(cropped_image,
#                                      config=r'--oem 1 --psm 6 -c tessedit_char_whitelist=1234567890/,')
# string = string.replace("\n", "")
# for i in range(4):
#     string = string.replace(",", "")
# print(string)
# bot.device.shell("sendevent /dev/input/event4: 1 330 1")     # Puts down finger
# bot.device.shell("sendevent /dev/input/event4: 3 57 10")     # Sets pressure
# bot.device.shell("sendevent /dev/input/event4: 3 53 100")    # Sets X to 100
# bot.device.shell("sendevent /dev/input/event4: 3 54 230")    # Sets Y to 230
# bot.device.shell("sendevent /dev/input/event4: 0 0 0")       # "0 0 0" (its called a SYN_REPORT)
# bot.device.shell("sendevent /dev/input/event4: 1 330 0")     # Lift up finger
# bot.device.shell("sendevent /dev/input/event4: 0 0 0")
# print(bot.task.scan_gem())
# bot.task.from_city_upgrade()
# bot.adb.find_img_arg_conf("fort2",0.5)

# pil_image = bot.adb.get_curr_device_screen_img()
# cv_image = array(pil_image)
# cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2RGB)
#
# # cv_image = cv2.imread("maraudeur_screen.png")
# img_to_find = cv2.imread('resources\\heal_icon.png')
#
# result = cv2.matchTemplate(cv_image, img_to_find, cv2.TM_CCOEFF_NORMED)
# needle_w = img_to_find.shape[1]
# needle_h = img_to_find.shape[0]
# min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
# min_thresh = 0.85
# location = where(result >= min_thresh)
# location = list(zip(*location[::-1]))
# # print(location)
#
# rectangles = []
# for loc in location:
#     rect = [int(loc[0]), int(loc[1]), needle_w, needle_h]
#     rectangles.append(rect)
# # print(rectangles)
#
# localisations = []
#
# for i in range(len(rectangles)):
#     localisations.append((rectangles[i][0], rectangles[i][1]))
# element_to_delete = []
# for i in range(len(localisations) - 1):
#     if ((
#             (localisations[i][0] + 1 == localisations[i + 1][0]) or
#             (localisations[i][0] - 1 == localisations[i + 1][0]) or
#             (localisations[i][0] == localisations[i + 1][0])
#     ) and
#             (
#                     (localisations[i][1] + 1 == localisations[i + 1][1]) or
#                     (localisations[i][1] - 1 == localisations[i + 1][1]) or
#                     (localisations[i][1] == localisations[i + 1][1])
#             )):
#         element_to_delete.append(localisations[i])
#
# print(element_to_delete)
# for element in element_to_delete:
#     localisations.remove(element)
# print(localisations)

















