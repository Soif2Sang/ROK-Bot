import flet as ft
from src.utils.schemas.emulator_schemas import EmulatorSettingsSchema

from src.utils.flet_translations import translate
from src.utils.singletons import ss, FileSingleton
from src.views.settings.general.general_tab import InterfaceSettings
from src.views.settings.profile.profile import SettingContainer
from src.views.tiles.handler.logging_handler import Logger

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


class InstanceTabs(ft.Tabs):
    def __init__(self, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.logger = Logger()

        self.tabs.append(ft.Tab(content=self.logger, text=translate("Activity Logs")))
        self.tabs.append(ft.Tab(content=self.settings, text=translate("Settings")))
        self.tabs.append(InterfaceSettings(number))

        self.settings.tabs.append(ft.Tab(content=SettingContainer(number, "1"), text=translate("Profile 1")))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(number, "2"), text=translate("Profile 2")))
        self.settings.tabs.append(ft.Tab(content=SettingContainer(number, "3"), text=translate("Profile 3")))

        emulator_settings: EmulatorSettingsSchema = ss.emulator_settings.emulators[str(self.number)]

        for key, schedule in emulator_settings.schedules.items():
            if schedule.enabled:
                self.settings.selected_index = int(key) - 1
                break

    def add_text(self, texte: str, color=None):
        self.logger.add_text(texte, color)

    def add_divider(self):
        self.logger.add_divider()
