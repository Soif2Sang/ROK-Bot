import flet as ft

from utils.functions import FileSingleton
from views.tiles.handler.logging_handler import Logger
from viewscod.Flet_Setting_cod import SettingContainer


class InterfaceSettings(ft.Tab):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        if "interface" not in data:
            data["interface"] = {"auto_scroll": True, "auto_refresh": True}
            self.FileSingleton.write_data(data)
        self.content = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Switch(
                            label="Logger autoscroll",
                            value=data["interface"]["auto_scroll"],
                            on_change=lambda _: self.reverse_keyword("auto_scroll"),
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.Switch(
                            label="Enable Discord Notifications",
                            value=data["discord"]["enabled"],
                            on_change=lambda _: self.reverse_keyword("enabled"),
                        )
                    ]
                ),
                ft.Row(
                    controls=[
                        ft.TextField(
                            label="Your discord ID",
                            value=data["discord"]["user_id"],
                            on_change=self.submit,
                        )
                    ]
                ),
            ]
        )
        self.text = "General Settings"

    def reverse_keyword(self, keyword: str):
        if keyword == "auto_scroll":
            data = self.FileSingleton.get_data()
            data["interface"][keyword] = not data["interface"][keyword]
            self.FileSingleton.write_data(data)
            if keyword == "auto_scroll":
                for frame in self.page.frames:
                    self.page.frames[frame].logger.auto_scroll = data["interface"][keyword]
                self.update()
        else:
            data = self.FileSingleton.get_data()
            data["discord"][keyword] = not data["discord"][keyword]
            self.FileSingleton.write_data(data)

    def submit(self, e):
        data = self.FileSingleton.get_data()
        data["discord"]["user_id"] = e.control.value
        self.FileSingleton.write_data(data)


class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.width = 400
        self.logger = Logger(self, page)
        self.tabs.append(ft.Tab(content=self.settings, text="Settings"))
        self.tabs.append(ft.Tab(content=self.logger, text="Logs"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 3), text="Profile 3"))
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        for profile in data[str(number)]["schedules"]:
            print(self.settings.selected_index)
            if data[str(number)]["schedules"][profile]["enabled"]:
                self.settings.selected_index = int(profile) - 1
                break

    def add_text(self, texte: str):
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
        self.tabs.append(ft.Tab(content=self.logger, text="Logs"))
        self.tabs.append(InterfaceSettings(page))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 1), text="Profile 1"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 2), text="Profile 2"))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(page, int(number), 3), text="Profile 3"))
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        for profile in data[str(number)]["schedules"]:
            print(self.settings.selected_index)
            if data[str(number)]["schedules"][profile]["enabled"]:
                self.settings.selected_index = int(profile) - 1
                break

    def add_text(self, texte: str):
        self.logger.add_text(texte)
