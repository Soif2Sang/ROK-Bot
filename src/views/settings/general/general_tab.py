import flet as ft

from src.utils.flet_translations import translate
from src.views.settings.general._instance import GeneralSettings


class InterfaceSettings(ft.Tab):
    def __init__(self, instance, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.text = translate("Instance Settings")
        self.content = GeneralSettings(instance)
