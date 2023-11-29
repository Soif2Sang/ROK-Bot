import os
import re

from utils.flet_translations import translations


def check_translations_in_files(directory, translations):
    translate_pattern = re.compile(r'translate\("(.*?)"\)')

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                with open(os.path.join(root, file), 'r') as f:
                    try:
                        content = f.read()
                    except:
                        continue
                    matches = re.findall(translate_pattern, content)

                    for match in matches:
                        if not translations.get(match, False):
                            print(f"Missing translation for: {match} in file: {os.path.join(root, file)}")


# Call the function with the 'views' directory and your translations dictionary
check_translations_in_files('views', translations)
