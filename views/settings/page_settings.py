import flet as ft
from utils.singletons import ss

color_bank = {"1": "#3b8ed0", "2": "#ba4543", "3": "#dec433"}


class PageSettings(ft.Container):
    def __init__(self, instance_index: str, profile_index: str):
        super().__init__()
        self.instance_index = instance_index
        self.profile_index = profile_index

        self.padding = ft.padding.only(top=5, left=0, bottom=0)
        self.content: ft.ListView = ft.ListView(height=400, expand=1, padding=1, spacing=0)

        self.tasks = ss.emulator_settings.emulators[str(self.instance_index)].schedules[str(self.profile_index)].tasks
        self.context = ss.emulator_settings.emulators[str(self.instance_index)].schedules[str(self.profile_index)]
        self.instance_context = ss.emulator_settings.emulators[str(self.instance_index)]

        self.theme = ft.Theme(color_scheme=ft.ColorScheme(primary=color_bank[self.profile_index]))
        self.init()

    def add(self, *control):
        for ctrl in control:
            self.content.controls.append(ctrl)

    def goBack(self):
        self.content.controls = []
        # self.data = self.FileSingleton.get_data()
        self.init()

        if self.__getattribute__("page"):
            self.update()

    def init(self):
        pass
