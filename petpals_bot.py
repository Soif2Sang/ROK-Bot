from threading import Thread
from petpals_adb import *
import cv2

import numpy as np

class Bot():
    def __init__(self,adb):
        self.adb: Adb =adb
        self.device= adb.get_device()

def get_bot(number):
    adb = Adb(number)
    bot = Bot(adb)
    bot.adb.connect_to_device()
    return bot

if __name__ == "__main__":
    # upgrade_all()

    bot = get_bot(59826)

    # Read image.
    while 1:
        print("get screen")
        # img = bot.adb.get_curr_device_screen_img()
        # print("got screen")

        img = bot.adb.get_cv2_img()[120:508, 650:]
        print("got screen")
        # Convert to grayscale.
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Blur using 3 * 3 kernel.
        gray_blurred = cv2.blur(gray, (3, 3))

        # Apply Hough transform on the blurred image.
        detected_circles = cv2.HoughCircles(gray_blurred,
                                            cv2.HOUGH_GRADIENT, 1, 50, param1=50,
                                            param2=30, minRadius=30, maxRadius=100)
        print(detected_circles)
        # Draw circles that are detected.
        if detected_circles is not None:

            # Convert the circle parameters a, b and r to integers.
            detected_circles = np.uint16(np.around(detected_circles))

            for pt in detected_circles[0, :]:
                a, b, r = pt[0], pt[1], pt[2]

                # Draw the circumference of the circle.
                cv2.circle(img, (a, b), r, (0, 255, 0), 2)

                # Draw a small circle (of radius 1) to show the center.
                cv2.circle(img, (a, b), 1, (0, 0, 255), 3)
                cv2.imshow("Detected Circle", img)
                print(a, b)
                bot.adb.click(650 + a, 120 + b)
                sleep(0.3)

