import re
import pyautogui
import icecream

from utils.resources import ImageSingleton
#
with open('average.txt', 'r') as file:
    lines = file.readlines()

time_pattern = re.compile(r'fastest is (\d{2}):(\d{2}):(\d{2})$')

all_times_in_seconds = []

for line in lines:
    match = time_pattern.search(line)
    if match:
        hours, minutes, seconds = map(int, match.groups())
        total_seconds = hours * 3600 + minutes * 60 + seconds
        all_times_in_seconds.append(total_seconds)

if all_times_in_seconds:
    average_time = sum(all_times_in_seconds) / len(all_times_in_seconds)
    print(f'Average time: {average_time} seconds')
else:
    print('No matching lines found in the file.')
exit()
images = ImageSingleton()
import cv2
def find_img(target):
    img_to_find = images.get_file_name(target)


    result = cv2.matchTemplate(cv2.imread('captcha_slider.png'), img_to_find, cv2.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)

    return max_val
        

for keyword in ["menu_button", "map_icon", "hammer", "inbox", "mightiest_gov"]:
    print(find_img(target=keyword))
    
    
