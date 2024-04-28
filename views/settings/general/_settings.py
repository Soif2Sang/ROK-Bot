import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from utils.flet_translations import translate
from utils.singletons import FileSingleton, SettingsSingleton
from views.settings.general.page_profiles import PageProfiles
from views.settings.general.page_redo import PageRedo
from views.settings.page_settings import PageSettings

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}

fs = FileSingleton()
ss = SettingsSingleton()


class AllSettings(PageSettings):
    def __init__(self, page, instance_index):
        super().__init__(page, instance_index, 1)
        self.content.height = None

    def clean(self):
        self.content.controls = []

    def reset(self):
        self.clean()
        self.init()
        self.initial_page.update()

    def add(self, *controls):
        for control in controls:
            self.content.controls.append(control)

    def init(self):
        self.application_settings = ss.application_settings

        if self.initial_page.UPGRADE:
            self.add(
                ft.Container(
                    content=ft.Text(
                        spans=[
                            ft.TextSpan(
                                text=translate("Emulator Workers"),
                                style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                            ),
                        ]
                    ),
                    bgcolor=ft.colors.SURFACE_VARIANT,
                    padding=ft.padding.all(10),
                    margin=ft.margin.only(top=5, bottom=3),
                ),
                ft.OutlinedButton(
                    text=translate("Configure Workers"),
                    icon=ft.icons.SETTINGS,
                    on_click=lambda _: self.initial_page.go("/configure-workers"),
                    style=ButtonStyle(
                        shape={
                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                        }
                    ),
                ),
                ft.Divider(),
            )

        self.add(
            ft.Container(
                content=ft.Text(
                    spans=[
                        ft.TextSpan(
                            text=translate("Captcha Solving"),
                            style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                        ),
                    ]
                ),
                bgcolor=ft.colors.SURFACE_VARIANT,
                padding=ft.padding.all(10),
                margin=ft.margin.only(top=5, bottom=3),
            ),
            ft.TextField(
                label=translate("Custom API key:"),
                value=self.application_settings.captcha.api_key,
                on_change=lambda e: self.submit_with_context(e, self.application_settings.captcha, "api_key", str),
                content_padding=ft.padding.all(10),
            ),
            ft.Divider(),
            ft.Container(
                content=ft.Text(
                    spans=[
                        ft.TextSpan(
                            text=translate("Interface & Discord Settings"),
                            style=ft.TextStyle(size=15, weight=ft.FontWeight.BOLD),
                        ),
                    ]
                ),
                bgcolor=ft.colors.SURFACE_VARIANT,
                padding=ft.padding.all(10),
                margin=ft.margin.only(top=5, bottom=3),
            ),
            ft.Switch(
                label=translate("Logger autoscroll"),
                value=self.application_settings.interface.enable_auto_scroll,
                on_change=lambda e: self.submit_with_context(e, self.application_settings.interface, "enable_auto_scroll", bool),
            ),
            ft.Switch(
                label=translate("Limit Logs to 200 (reduce lags)"),
                value=self.application_settings.interface.enable_limit_logs,
                on_change=lambda e: self.submit_with_context(e, self.application_settings.interface, "enable_limit_logs", bool),
            ),
            ft.Switch(
                label=translate("Enable Discord Notifications"),
                value=self.application_settings.discord.enabled,
                on_change=lambda e: self.submit_with_context(e, self.application_settings.discord, "enabled", bool),
            ),
            ft.TextField(
                label=translate("Your discord ID"),
                value=str(self.application_settings.discord.user_id),
                on_change=lambda e: self.submit_with_context(e, self.application_settings.discord, "user_id", int),
                content_padding=ft.padding.all(10),
            ),
        )

    def submit_with_context(self, e, context, keyword, method):
        setattr(context, keyword, method(e.control.value))
        ss.write_application_settings(self.application_settings)
