import copy

import flet as ft
from utils.schemas.emulator_schemas import EmulatorSettingsSchema

from utils.singletons import FileSingleton
from utils.singletons import ss
from views.tiles.handler.config_handler import InstanceTabs

# from views.tiles.handler.config_handler import Frame

class ConfigOverrider(ft.PopupMenuButton):
    def __init__(self, index, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.index = index
        self.icon = ft.icons.FILE_UPLOAD_OUTLINED
        self.init()

    def init(self):
        self.items.append(ft.PopupMenuItem(text="Export Config"))
        self.items.append(ft.PopupMenuItem())

        vms = ss.page.tile_manager.fetched_instances

        for vm in vms:
            if str(vm) != self.index:
                self.items.append(ft.PopupMenuItem(text=vms[vm]["name"], on_click=self.override_settings, data=vm))

    def refresh(self):
        self.items = []
        self.init()
        ss.page.update()

    def override_settings(self, e):
        instance = ss.emulator_settings.emulators[str(e.control.data)].instance
        name = ss.emulator_settings.emulators[str(e.control.data)].name
        host = ss.emulator_settings.emulators[str(e.control.data)].host
        port = ss.emulator_settings.emulators[str(e.control.data)].port

        ss.emulator_settings.emulators[str(e.control.data)] = copy.deepcopy(ss.emulator_settings.emulators[str(self.index)])

        ss.emulator_settings.emulators[str(e.control.data)].instance = instance
        ss.emulator_settings.emulators[str(e.control.data)].name = name
        ss.emulator_settings.emulators[str(e.control.data)].host = host
        ss.emulator_settings.emulators[str(e.control.data)].port = port

        ss.write_emulator_settings(ss.emulator_settings)

        if str(e.control.data) in ss.page.frames:
            for tab in ss.page.frames[str(e.control.data)].settings.tabs:
                tab.content.reset()

        ss.page.update()


class TileSlave(ft.Container):
    def __init__(self, number, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.context: EmulatorSettingsSchema = ss.emulator_settings.emulators[str(self.number)]

        self.padding = ft.padding.only(left=10)
        self.margin = ft.margin.only(bottom=3, left=15)

        self.text_name = ft.Text(value=self.context.name, width=80)
        self.text_status = ft.Text(value="")

        self.config_overrider = ConfigOverrider(number)

        self.border_radius = 3
        self.bgcolor = ft.colors.SURFACE
        self.on_click = self.select
        self.on_hover = self.hover

        self.content = ft.Row(
            [
                ft.Row(
                    controls=[
                        self.text_name,
                        self.text_status,
                    ]
                ),
                self.config_overrider,
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

    def hover(self, e):
        e.control.bgcolor = (
            ft.colors.SURFACE_VARIANT
            if (e.data == "true" or ss.page.body.controls[-1] == ss.page.frames.get(self.number, False))
            else ft.colors.SURFACE
        )
        ss.page.update()

    def select(self, e):
        ss.page.tile_manager.unselect_all()

        if len(ss.page.body.controls) > 2:
            ss.page.body.controls.pop()

        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.body.controls.append(ss.page.frames[self.number])
        self.bgcolor = ft.colors.SURFACE_VARIANT
        ss.page.update()

    def set_text(self, phrase: str):
        self.text_status.value = phrase
        ss.page.update()

    def get_text(self):
        return self.text_status.value

    def add_text(self, phrase: str, color=None):
        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.frames[self.number].add_text(phrase, color)

    def add_divider(self):
        if self.number not in ss.page.frames:
            ss.page.frames[self.number] = InstanceTabs(self.number)

        ss.page.frames[self.number].add_divider()
