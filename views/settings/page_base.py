import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder
from utils.schemas.emulator_schemas import ProfileSchema, TaskLibrarySchema

from utils.flet_translations import translate
from utils.functions import rgetattr, rsetattr
from utils.singletons import ss, FileSingleton


class BasePage:
    def __init__(self, profile):
        super().__init__()
        self.instance_index = profile.instance_index
        self.profile_index = profile.profile_index
        self.profile = profile
        self.profile.content.controls = []

        self.context: ProfileSchema = ss.emulator_settings.emulators[str(self.instance_index)].schedules[str(self.profile_index)]

        self.tasks: TaskLibrarySchema = self.context.tasks

        self.add_control(
            ft.Container(
                content=ft.Row(
                    controls=[
                        ft.IconButton(
                            icon=ft.icons.ARROW_BACK,
                            on_click=lambda _: self.profile.goBack(),
                        ),
                        ft.Text(value=translate("Settings"), size=20),
                    ],
                ),
                padding=ft.padding.only(top=5, left=0, bottom=0),
            ),
            ft.Divider(),
        )

        self.profile.content.scroll_to(delta=-1000, duration=1)
        ss.page.update()

    def add_control(self, *control):
        for ctrl in control:
            self.profile.content.controls.append(ctrl)

    def create_normal_switch(self, keyword: str, text: str, data=None):
        return ft.Switch(label=translate(text), value=rgetattr(self.context, keyword), on_change=self.submit_with_context, data=data)

    def create_advanced_switch(self, keyword: str, text: str, function, data=None):
        self.data = self.FileSingleton.get_data()
        if keyword not in ["loop_task", "scheduler"]:
            return ft.Row(
                controls=[
                    ft.Switch(
                        label=translate(text),
                        value=True if self.data[str(self.instance_index)]["schedules"][str(self.profile_index)][keyword] else False,
                        on_change=self.submit_with_context,
                        data=data,
                    ),
                    ft.OutlinedButton(
                        text=translate("Settings"),
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: function(),
                        style=ButtonStyle(
                            shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            }
                        ),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        else:
            return (
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=translate(text),
                            value=True if self.data[str(self.instance_index)][keyword] else False,
                            on_change=lambda _: self.reverse_keyword(keyword),
                        ),
                        ft.OutlinedButton(
                            text=translate("Settings"),
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function(),
                            style=ButtonStyle(
                                shape={
                                    ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                                },
                            ),
                        ),
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),
            )

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
