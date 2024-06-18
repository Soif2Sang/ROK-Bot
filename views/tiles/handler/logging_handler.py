import flet as ft
from utils.schemas.application_schemas import ApplicationSettingsSchema

from utils.singletons import FileSingleton
from utils.singletons import ss

fileSingleton = FileSingleton()


class Logger(ft.ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        application_settings: ApplicationSettingsSchema = ss.application_settings

        self.auto_scroll = application_settings.interface.enable_auto_scroll
        self.limit_logs = application_settings.interface.enable_limit_logs
        self.auto_refresh = application_settings.interface.enable_auto_refresh

    def add_text(self, text: str, color=None):
        text = ft.Text(value=text, weight=ft.FontWeight.W_600, color=color)

        if self.limit_logs and len(self.controls) > 140:
            self.controls.pop(0)
        self.controls.append(text)

        if self.__getattribute__("page"):
            self.update()

    def add_divider(self):
        if self.limit_logs and len(self.controls) > 140:
            self.controls.pop(0)
        self.controls.append(ft.Divider())

        if self.__getattribute__("page"):
            self.update()