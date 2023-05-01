import json

import flet as ft

from Flet_Logger import Logger
from Flet_Setting import SettingContainer
from Task_utils import get_data, write_data


class InterfaceSettings(ft.Tab):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        
        data = get_data()
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
        write_data(data)
        self.content = ft.Column(
            controls=[        ft.Switch(
            label="Logger autoscroll",
            value=data["interface"]["auto_scroll"],
            on_change=lambda _: self.reverse_keyword("auto_scroll")
        )]
        )
        self.text="UI Settings"


    def reverse_keyword(self, keyword:str):
        
        data = get_data()
        data["interface"][keyword] = not data["interface"][keyword]
        write_data(data)
        if keyword == 'auto_scroll':
            for frame in self.page.frames:
                self.page.frames[frame].logger.auto_scroll = data["interface"][keyword]
            self.update()

class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = Logger(self,page)
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logger"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),3), text="Profile 3"))
        
        data = get_data()
        for profile in data[str(number)]['schedules']:
            print(self.settings.selected_index)
            if data[str(number)]['schedules'][profile]['enabled']:
                self.settings.selected_index=int(profile)-1
                break
    def add_text(self, texte:str):
        self.logger.add_text(texte)



class FrameUpgrade(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = self.page.logger
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logger"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),3), text="Profile 3"))
        
        data = get_data()
        for profile in data[str(number)]['schedules']:
            print(self.settings.selected_index)
            if data[str(number)]['schedules'][profile]['enabled']:
                self.settings.selected_index=int(profile)-1
                break
    def add_text(self, texte:str):
        self.logger.add_text(texte)

