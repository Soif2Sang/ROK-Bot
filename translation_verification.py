import os
import re

from googletrans import Translator

from utils.flet_translations import translations


def check_translations_in_files(directory, translations):
    translate_pattern = re.compile(r'translate\("(.*?)"\)')
    need_translation = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                with open(os.path.join(root, file), "r", encoding="utf-8") as f:
                    try:
                        content = f.read()
                    except:
                        continue
                    matches = re.findall(translate_pattern, content)

                    for match in matches:
                        if not translations.get(match, False):
                            print(f"Missing translation for: {match} in file: {os.path.join(root, file)}")
                            # Automatically add translation to the dictionary
                            need_translation.append(match)
    print(need_translation)
    trans = translate_to_portuguese(need_translation)
    print(trans)
    for translation in trans:
        translations[translation.origin] = translation.text

def translate_to_portuguese(text):
    translator = Translator()
    return translator.translate(text, src='en', dest='pt')

# Call the function with the 'views' directory and your translations dictionary
check_translations_in_files("views", translations)

# Save the updated translations dictionary back to the file
with open("utils/flet_translations.py", "r") as f:
    lines = f.readlines()

with open("utils/flet_translations.py", "w") as f:
    for line in lines:
        if line.strip().startswith("}"):
            for key, value in translations.items():
                f.write(f'    "{key}": "{value}",\n')
        f.write(line)
