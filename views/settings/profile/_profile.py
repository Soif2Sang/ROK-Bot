import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from views.settings.profile.page_upgrade_city import PageUpgradeCity
from views.settings.page_settings import PageSettings
from views.settings.profile.page_character import PageCharacter
from views.settings.profile.page_logback import PageLogback
from views.settings.profile.page_barbs import PageBarbs
from views.settings.profile.page_fog import PageFog
from views.settings.profile.page_heal import PageHeal
from views.settings.profile.page_marauders import PageMarauders
from views.settings.profile.page_materials import PageMaterials
from views.settings.profile.page_rally import PageRally
from views.settings.profile.page_training import PageTraining
from views.settings.profile.page_transfer import PageTransfer
from views.settings.profile.page_rss import PageRss
from views.settings.profile.page_gem import PageGem
from utils.Task_utils import FileSingleton

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}


class ProfileSettings(PageSettings):
    def __init__(self, page, tab, instance_index: str, profile_index: int):
        super().__init__(page, tab, instance_index, profile_index)

    def clean(self):
        self.content.controls = []

    def reset(self):
        self.clean()
        self.init()
        self.initial_page.update()

    def init(self):

        self.create_advanced_switch("gather_gem", "Gem Gathering", PageGem)
        self.create_advanced_switch("gather_rss", "Resources Gathering", PageRss)
        self.create_normal_switch("collect_ressource", "Collect City Resources")
        self.create_normal_switch("use_enhanced_buff", "Apply Enhanced Buff")
        self.create_normal_switch("buy_merchant", "Buy Mysterious Merchant")
        self.create_normal_switch("check_donation", "Donate to Alliance")
        self.create_normal_switch("gather_alliance_pit", "Alliance Pit Gathering")

        # ##
        self.create_advanced_switch("material_production", "Produce Materials", PageMaterials)
        self.create_advanced_switch("train_troops", "Troops Training", PageTraining)
        self.create_normal_switch("claim_daily_vip", "Claim VIP Chests")
        self.create_normal_switch("claim_daily_chest", "Claim Daily Chests")
        self.create_normal_switch("claim_daily_quests", "Claim Daily Quests")
        self.create_normal_switch("claim_campaign", "Claim Expedition Rewards")
        self.create_normal_switch("claim_mails", "Claim Mails")
        self.create_normal_switch("alliance_help", "Help Alliance")
        #
        self.create_advanced_switch("defeat_barbarians", "Hunt Barbarians", PageBarbs)
        self.create_advanced_switch("start_fort", "Launch Barbarian Rally", PageRally)
        self.create_advanced_switch("kill_marauders", "Kill Marauders", PageMarauders)
        self.create_advanced_switch("scout_fog", "Explore Fog", PageFog)
        self.create_advanced_switch("upgrade_city", "Upgrade City", PageUpgradeCity)
        self.create_advanced_switch("heal_troop", "Troops Healing", PageHeal)
        self.create_advanced_switch("transfer_enable", "Transfer Resources", PageTransfer)
        #
        self.content.controls.append(ft.Divider())
        #
        self.create_normal_switch("auto_reconnect", "Reconnect on Network Issues")
        self.create_advanced_switch("auto_log_back", "Log Back on Device Switch", PageLogback)
        self.create_normal_switch("auto_captcha", "Solve Captcha")
        self.create_slow_mode()
        self.create_advanced_switch("switch_character", "Switch Characters", PageCharacter)

    def submit(self, e, keyword, method):
        self.data = self.FileSingleton.get_data()
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1", 'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
        elif keyword not in ["sleep_multiplicator", "defeat_barbarians"]:
            if e.control.value == '':
                self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(0)
            else:
                self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(
                    e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(
                e.control.value.replace("x", "").replace("level ", ""))
        self.FileSingleton.write_data(self.data)

    def page_character(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ))
        self.content.controls.append(ft.Divider(), )
        self.content.controls.append(
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    "leave_game_switch_character"] else False,
                on_change=lambda _: self.reverse_keyword("leave_game_switch_character")
            )
        )
        self.initial_page.update()

    def page_logback(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.extend([
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ),
            ft.Divider(),
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "Time to wait before the bot log  back from your connection(minutes):\n",
                        style=ft.TextStyle(size=15, color="black"),
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "log_back1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                     "log_back2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "log_back2", int)
                                 )
                ]
            )
        ]
        )

        self.initial_page.update()

    def page_redo(self):
        self.data = self.FileSingleton.get_data()
        self.clean()
        self.tabs.expand = True
        self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        # self.content = ft.ListView(height=500, expand=0, padding=ft.padding.only(right=20), )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(ft.Divider(), )
        self.content.controls.extend([
            ft.Text(
                spans=[
                    ft.TextSpan(
                        "*Randomise it as much as possible*\n",
                        style=ft.TextStyle(size=15, color="red", weight=ft.FontWeight.BOLD),
                    ),
                    ft.TextSpan(
                        "Time to wait before the bot re-do the tasks selected (minutes):\n",
                        style=ft.TextStyle(size=15, color="red"),
                    )
                ]
            ),
            ft.Row(
                controls=[
                    ft.TextField(label="Minimum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop1"],
                                 width=80,
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop1", int)
                                 ),
                    ft.Text("~"),
                    ft.TextField(label="Maximum",
                                 value=self.data[str(self.instance_index)]["time_to_wait_loop2"],
                                 width=90,
                                 on_change=lambda e: self.submit(e, "time_to_wait_loop2", int)
                                 )
                ]
            ),
            ft.Switch(label="Close the game after all the tasks are done",
                      value=self.data[str(self.instance_index)]["leave_game_loop"],
                      on_change=lambda _: self.reverse_keyword('leave_game_loop'))
        ]
        )
        self.initial_page.update()

    def reverse_keyword(self, keyword: str, index=None):
        if index is None:
            index = self.profile_index
        if keyword not in ["loop_task", "scheduler", "leave_game_loop"]:
            self.data[str(self.instance_index)]['schedules'][str(index)][keyword] = not \
                self.data[str(self.instance_index)]['schedules'][str(index)][keyword]
        else:
            # print(keyword, self.data[str(self.instance_index)][keyword])

            self.data[str(self.instance_index)][keyword] = not self.data[str(self.instance_index)][keyword]
        self.FileSingleton.write_data(self.data)

    def create_normal_switch(self, keyword: str, text: str):
        self.data = self.FileSingleton.get_data()
        self.content.controls.append(
            ft.Switch(
                label=text,

                value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                    keyword] else False,
                on_change=lambda _: self.reverse_keyword(keyword)
            )
        )

    def create_advanced_switch(self, keyword: str, text: str, function):
        self.data = self.FileSingleton.get_data()
        if keyword not in ["loop_task", "scheduler"]:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,

                            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                keyword] else False,
                            on_change=lambda _: self.reverse_keyword(keyword),

                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function(self)
                            , style=ButtonStyle(shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            })
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN
                )
            )
        else:
            self.content.controls.append(
                ft.Row(
                    controls=[
                        ft.Switch(
                            label=text,

                            value=True if self.data[str(self.instance_index)][keyword] else False,
                            on_change=lambda _: self.reverse_keyword(keyword),
                        ),
                        ft.OutlinedButton(
                            text="Settings",
                            icon=ft.icons.SETTINGS,
                            on_click=lambda _: function(), style=ButtonStyle(shape={
                                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                            }, ),
                        )
                    ],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                ),

            )

    def create_slow_mode(self):
        self.content.controls.append(ft.Row
            (
            controls=[
                ft.Switch(
                    label="Reduce bot speed",

                    value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                        "slow_mode"] else False,
                    on_change=lambda _: self.reverse_keyword("slow_mode")
                ),
                ft.Dropdown(
                    width=125,
                    label="Factor",
                    options=[
                        ft.dropdown.Option("1.0x"),
                        ft.dropdown.Option("1.25x"),
                        ft.dropdown.Option("1.5x"),
                        ft.dropdown.Option("1.75x"),
                        ft.dropdown.Option("2.0x"),
                        ft.dropdown.Option("2.25x"),
                        ft.dropdown.Option("2.5x"),
                        ft.dropdown.Option("2.75x"),
                        ft.dropdown.Option("3.0x"),
                    ],
                    value=str(self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                                  "sleep_multiplicator"]) + "x",
                    on_change=lambda e: self.submit(e, "sleep_multiplicator", str),
                    height=50,
                    content_padding=ft.Padding(left=5, top=3, right=5, bottom=3)  # modify to your likings
                )
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN
        )
        )
