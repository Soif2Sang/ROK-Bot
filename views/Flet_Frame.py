import flet as ft

from views.Flet_general_settings import InterfaceSettings
from views.Flet_Logger import Logger
from views.Flet_Setting import SettingContainer
from utils.Task_utils import FileSingleton

class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = Logger(self,page)
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logs"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),3), text="Profile 3"))
        self.FileSingleton = FileSingleton()

        data = self.FileSingleton.get_data()
        for profile in data[str(number)]['schedules']:
            # print(self.settings.selected_index)
            if data[str(number)]['schedules'][profile]['enabled']:
                self.settings.selected_index=int(profile)-1
                break

    def add_text(self, texte: str, color=None):
        self.logger.add_text(texte, color)

    def add_divider(self):
        self.logger.add_divider()


class FrameUpgrade(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.page = page
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = self.page.logger
        self.FileSingleton = FileSingleton()

        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logs"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page,self, int(number),3), text="Profile 3"))
        
        data = self.FileSingleton.get_data()
        for profile in data[str(number)]['schedules']:
            # print(self.settings.selected_index)
            if data[str(number)]['schedules'][profile]['enabled']:
                self.settings.selected_index=int(profile)-1
                break
    def add_text(self, texte:str):
        self.logger.add_text(texte)

