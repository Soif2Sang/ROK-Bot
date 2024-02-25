import os
import shutil
import sys
import zipfile
from datetime import datetime

# Get the input argument
global_input = sys.argv[1] if len(sys.argv) > 1 else None

# Modify the current_date based on the input
if global_input is None:
    current_date = datetime.now().strftime("%Y-%m-%d")
else:
    current_date = "-br-" + datetime.now().strftime("%Y-%m-%d")

new_filename = f".\\auth compiled\\test environnement\\bot_executable_{current_date}\\bot-{current_date}.exe"

os.makedirs(f".\\auth compiled\\test environnement\\bot_executable_{current_date}", exist_ok=True)

shutil.move(".\\Bot.exe", new_filename)
shutil.copytree(".\\resources", f".\\auth compiled\\test environnement\\bot_executable_{current_date}\\resources", dirs_exist_ok=True)
shutil.copytree(".\\assets", f".\\auth compiled\\test environnement\\bot_executable_{current_date}\\assets", dirs_exist_ok=True)


# Zip the folder
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            # this line will add each file to the zip file with path relative to the directory being zipped
            ziph.write(os.path.join(root, file), arcname=os.path.relpath(os.path.join(root, file), path))


zipf = zipfile.ZipFile(f"bot_executable_{current_date}.zip", "w", zipfile.ZIP_DEFLATED)
zipdir(f".\\auth compiled\\test environnement\\bot_executable_{current_date}", zipf)
zipf.close()

shutil.move(f".\\bot_executable_{current_date}.zip", f".\\auth compiled\\test environnement\\bot_executable_{current_date}.zip")
