import glob
from cv2 import imread

print("from cv2 import cvtColor, imread, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, imdecode, \
    IMREAD_COLOR, COLOR_BGR2HSV, inRange")
dir_path = r'resources/*.png'
# for file in glob.glob(dir_path, recursive=True):
#     a = "\\"
#     print(f'{file.split(a)[1].split(".")[0]} = ',end="")
#     print(imread(f'resources\\\\{file.split(a)[1].split(".")[0]}.png'))
# print("")
# print("def get_file_name(file_name):")
# for file in glob.glob(dir_path, recursive=True):
#     a = "\\"
#     print("    if file_name == ", end="")
#     print(f'"{file.split(a)[1].split(".")[0]}":')
#     print(f'        return {file.split(a)[1].split(".")[0]}')
# print("    else:")
# print("        return imread('resources\\' + file_name + '.png')")
#
file = 'resources.py'
with open(file, 'w') as f:
    f.write("from cv2 import cvtColor, imread, matchTemplate, minMaxLoc, COLOR_BGR2RGB, TM_CCOEFF_NORMED, imdecode, \
        IMREAD_COLOR, COLOR_BGR2HSV, inRange\n")
    dir_path = r'resources/*.png'
    for file in glob.glob(dir_path, recursive=True):
        # f.write(file.split("\\")[1])
        a = "\\"
        f.write(f'{file.split(a)[1].split(".")[0]}' f"= imread('resources\\\\{file.split(a)[1].split('.')[0]}.png')\n")
    f.write("\n")
    f.write("def get_file_name(file_name):\n")
    for file in glob.glob(dir_path, recursive=True):
        # f.write(file.split("\\")[1])
        a = "\\"
        f.write("    if file_name == "f'"{file.split(a)[1].split(".")[0]}":\n')
        f.write(f'        return {file.split(a)[1].split(".")[0]}\n')
        # f.write(f"= imread('resources\\\\{file.split(a)[1].split('.')[0]}')")
        # if file_name == "gem_icon_day_up_left":
        #     return gem_icon_day_up_left
    f.write("    else:\n")
    f.write("        return imread('resources\\\\' + file_name + '.png')\n")
