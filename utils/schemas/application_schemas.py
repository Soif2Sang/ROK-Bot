import threading
from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal

import flet as ft
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DiscordSettingsSchema:
    enabled: bool = False
    user_id: int = -1


@dataclass_json
@dataclass
class InterfaceSettingsSchema:
    enable_auto_scroll: bool = True
    enable_auto_refresh: bool = False
    enable_limit_logs: bool = True


@dataclass_json
@dataclass
class CaptchaSettingsSchema:
    api_key: str = ""


@dataclass_json
@dataclass
class BluestacksPathSchema:
    config: str = ""
    player: str = ""


@dataclass_json
@dataclass
class LdplayerPathSchema:
    ldconsole: str = ""


@dataclass_json
@dataclass
class PathSchema:
    bluestacks: BluestacksPathSchema = field(default_factory=BluestacksPathSchema)
    ldplayer: LdplayerPathSchema = field(default_factory=LdplayerPathSchema)


@dataclass_json
@dataclass
class UserSchema:
    email: str = ""
    password: str = ""


@dataclass_json
@dataclass
class ApplicationSettingsSchema:
    discord: DiscordSettingsSchema = field(default_factory=DiscordSettingsSchema)
    interface: InterfaceSettingsSchema = field(default_factory=InterfaceSettingsSchema)
    captcha: CaptchaSettingsSchema = field(default_factory=CaptchaSettingsSchema)
    paths: PathSchema = field(default_factory=PathSchema)
    user: UserSchema = field(default_factory=UserSchema)
    version_language: Literal["en", "pt", "ar"] = "en"

@dataclass_json
@dataclass
class DecoratedPageSchema(ft.Page):
    body: ft.Column
    tile_handler: ft.ListView

    def generate_toast(self, title, description, icon=ft.icons.INFO, bgcolor_title=ft.colors.ERROR_CONTAINER) -> None:
        pass


@dataclass_json
@dataclass
class TileSlaveSchema:
    number: str
    text_name: ft.Text
    text_status: ft.Text

    def set_text(self, phrase: str) -> None:
        pass

    def get_text(self) -> str:
        pass

    def add_text(self, phrase: str, color=None) -> None:
        pass

    def add_divider(self) -> None:
        pass


@dataclass_json
@dataclass
class TileWorkerSchema:
    number: str
    paused: bool
    stopped: bool

    runner: Any
    main_task: Any
    tasks_process: threading.Thread

    text_name: ft.Text
    text_status: ft.Text

    slaves: dict[str, TileSlaveSchema]

    def start(self, e) -> None:
        pass

    def pause(self, e) -> None:
        pass

    def stop(self, e) -> None:
        pass

    def resume(self, e) -> None:
        pass

    def start_tasks(self) -> None:
        pass

    def set_text(self, phrase: str) -> None:
        pass

    def get_text(self) -> str:
        pass

    def add_text(self, phrase: str, color=None) -> None:
        pass

    def add_divider(self) -> None:
        pass

    def add_tile(self, number: str) -> None:
        pass

    def refresh_tile(self) -> None:
        pass
