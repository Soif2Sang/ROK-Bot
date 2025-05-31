import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder
from src.utils.schemas.emulator_schemas import EmulatorSettingsSchema

from src.utils.flet_translations import translate
from src.utils.functions import rgetattr, rsetattr
from src.utils.singletons import ss
from src.views.settings.general.page_profiles import PageProfiles
from src.views.settings.general.page_redo import PageRedo
from src.views.settings.page_settings import PageSettings

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


class GeneralSettings(PageSettings):
    def __init__(self, instance_index):
        super().__init__(instance_index, "1")

    def clean(self):
        self.content.controls = []

    def reset(self):
        self.clean()
        self.init()

        if self.__getattribute__("page"):
            self.update()

    def add(self, *controls):
        for control in controls:
            self.content.controls.append(control)

    def init(self):
        self.add(
            ft.Container(
                content=ft.Text(
                    spans=[
                        ft.TextSpan(
                            translate("Shared Profile Preferences"),
                            style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                        ),
                    ]
                ),
                bgcolor=ft.colors.SURFACE_VARIANT,
                padding=ft.padding.all(10),
                margin=ft.margin.only(top=5, bottom=3),
            )
        )
        self.create_advanced_switch("scheduler", "run Multiple Profile", PageProfiles)

        # self.add(
        #     ft.TextField(
        #         label=translate("Custom API key:"),
        #         value=self.data[str(self.instance_index)]["API_KEY"],
        #         on_change=lambda e: self.submit(e, "API_KEY", str),
        #     ),
        #     ft.Container(
        #         content=ft.Text(
        #             spans=[
        #                 ft.TextSpan(
        #                     text=translate("Interface & Discord Settings"),
        #                     style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
        #                 ),
        #             ]
        #         ),
        #         bgcolor=ft.colors.SURFACE_VARIANT,
        #         padding=ft.padding.all(10),
        #         margin=ft.margin.only(top=5, bottom=3),
        #     ),
        #     ft.Switch(
        #         label=translate("Logger autoscroll"),
        #         value=self.data["interface"]["auto_scroll"],
        #         on_change=lambda _: self.reverse_keyword("auto_scroll"),
        #     ),
        #     ft.Switch(
        #         label=translate("Limit Logs to 200 (reduce lags)"),
        #         value=self.data["interface"].get("limit_logs", False),
        #         on_change=lambda _: self.reverse_keyword("limit_logs"),
        #     ),
        #     ft.Switch(
        #         label=translate("Enable Discord Notifications"),
        #         value=self.data["discord"]["enabled"],
        #         on_change=lambda _: self.reverse_keyword("enabled"),
        #     ),
        #     ft.TextField(
        #         label=translate("Your discord ID"),
        #         value=self.data["discord"]["user_id"],
        #         on_change=lambda e: self.submit(e, "user_id", int),
        #     ),
        # )

    def create_advanced_switch(self, keyword: str, text: str, function):
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate(text),
                        value=rgetattr(self.instance_context, keyword),
                        on_change=self.submit_with_context,
                        data={"path": keyword, "type": bool},
                    ),
                    ft.OutlinedButton(
                        text=translate("Settings"),
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: function(self),
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
        rsetattr(ss.emulator_settings.emulators[self.instance_index], e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)
