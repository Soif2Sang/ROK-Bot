import flet as ft
from utils.schemas.application_schemas import ApplicationSettingsSchema

from utils.functions import FileSingleton
from utils.singletons import ss

fileSingleton = FileSingleton()


class Logger(ft.ListView):
    def __init__(self, frame, page, **kwargs):
        super().__init__(**kwargs)
        self.parent = frame
        self.initial_page = page

        application_settings: ApplicationSettingsSchema = ss.application_settings

        self.auto_scroll = application_settings.interface.enable_auto_scroll
        self.limit_logs = application_settings.interface.enable_limit_logs
        self.auto_refresh = application_settings.interface.enable_auto_refresh

    def add_text(self, texte: str, color=None):
        text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color)

        if self.limit_logs and len(self.controls) > 140:
            self.controls.pop(0)
        self.controls.append(text)
        self.initial_page.update()

    def add_divider(self):
        if self.limit_logs and len(self.controls) > 140:
            self.controls.pop(0)
        self.controls.append(ft.Divider())
        self.initial_page.update()


def get_date():
    pass


class LoggerUpgrade(ft.ListView):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        data = fileSingleton.get_data()
        if "interface" not in data:
            data["interface"] = {"auto_scroll": True, "auto_refresh": True}
        fileSingleton.write_data(data)
        self.auto_scroll = True
        self.initial_page = page

    def add_text(self, texte: str, color=None):
        if color is None:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600)
        else:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color)
        self.controls.append(text)
        self.initial_page.update()

    def add_divider(self):
        self.controls.append(ft.Divider())
        self.initial_page.update()
