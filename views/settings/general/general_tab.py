import flet as ft

from utils.flet_translations import translate
from utils.functions import FileSingleton, rsetattr
from utils.singletons import ss
from views.settings.general._instance import GeneralSettings


class InterfaceSettings(ft.Tab):
    def __init__(self, page, instance, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.instance = instance
        self.text = translate("Instance Settings")
        self.content = GeneralSettings(page, instance)
