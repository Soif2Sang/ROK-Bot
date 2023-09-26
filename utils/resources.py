from cv2 import cvtColor, imread, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, imdecode,         IMREAD_COLOR, COLOR_BGR2HSV, inRange
import os
import warnings

dir = './resources'

class ImageSingleton:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.load_images()
        return cls.__instance

    def load_images(self):
        self.image_dict = {}
        for filename in os.listdir(dir):
            if filename.endswith(".png"):
                name = os.path.splitext(filename)[0]  # Extract the name without extension
                image = imread(os.path.join(dir, filename))
                self.image_dict[name] = image

    def get_file_name(self, file_name):
        return self.image_dict.get(file_name, imread(f"{dir}/{file_name}.png"))
