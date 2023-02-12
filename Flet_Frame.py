import json

import flet as ft

from Flet_Logger import Logger
from Flet_Setting import SettingContainer


class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = Logger()
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logger"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),3), text="Profile 3"))
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        for profile in data[str(number)]['schedules']:
            print(self.settings.selected_index)
            if data[str(number)]['schedules'][profile]['enabled']:
                self.settings.selected_index=int(profile)-1
                break
    def add_text(self, texte:str):
        self.logger.add_text(texte)

