import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder

from src.utils.constants import VERSION_TYPE
from src.views.settings.profile.page_logback_from_device_switch import PageLogbackFromDeviceSwitch
from src.views.settings.profile.page_logback_from_error import PageLogbackFromError

from src.utils.flet_translations import translate
from src.utils.functions import rgetattr, rsetattr
from src.utils.singletons import EmulatorSingleton, ss, ApiSingleton
from src.views.settings.page_settings import PageSettings
from src.views.settings.profile.page_academy_research import PageAcademyResearch
from src.views.settings.profile.page_barbs import PageBarbs
from src.views.settings.profile.page_character import PageCharacter
from src.views.settings.profile.page_expedition import PageExpedition
from src.views.settings.profile.page_fog import PageFog
from src.views.settings.profile.page_gem import PageGem
from src.views.settings.profile.page_heal import PageHeal
from src.views.settings.profile.page_marauders import PageMarauders
from src.views.settings.profile.page_materials import PageMaterials
from src.views.settings.profile.page_rally import PageRally
from src.views.settings.profile.page_rss import PageRss
from src.views.settings.profile.page_training import PageTraining
from src.views.settings.profile.page_transfer import PageTransfer
from src.views.settings.profile.page_upgrade_city import PageUpgradeCity

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


class SettingContainer(PageSettings):
    def __init__(self, instance_index: str, profile_index: str):
        super().__init__(instance_index, profile_index)

    def clean(self):
        self.content.controls = []

    def reset(self):
        self.clean()
        self.init()
        ss.page.update()

    def init(self):
        subscription_tier = ApiSingleton().getTier()

        self.create_advanced_switch("tasks.gather_gem.enabled", "Gem Gathering", PageGem)
        self.create_advanced_switch("tasks.gather_rss.enabled", "Resources Gathering", PageRss)

        self.create_normal_switch("tasks.collect_city_resources.enabled", "Collect City Resources")
        self.create_normal_switch("tasks.apply_buff.enabled", "Apply Enhanced Buff")
        self.create_normal_switch("tasks.buy_mysterious_merchant.enabled", "Buy Mysterious Merchant")
        self.create_normal_switch("tasks.alliance_donation.enabled", "Donate to Alliance")
        self.create_normal_switch("tasks.alliance_pit.enabled", "Alliance Pit Gathering")

        # ##
        self.create_advanced_switch("tasks.produce_materials.enabled", "Produce Materials", PageMaterials)
        self.create_advanced_switch("tasks.troop_training.enabled", "Troops Training", PageTraining)
        self.create_normal_switch("tasks.claim_daily_vip_chest.enabled", "Claim VIP Chests")
        self.create_normal_switch("tasks.claim_daily_chest.enabled", "Claim Daily Chests")
        self.create_normal_switch("tasks.claim_daily_quest.enabled", "Claim Daily Quests")
        self.create_advanced_switch("tasks.claim_daily_expedition_rewards.enabled", "Claim Expedition Rewards", PageExpedition)
        self.create_normal_switch("tasks.claim_mail.enabled", "Claim Mails")
        self.create_normal_switch("tasks.alliance_help.enabled", "Help Alliance")
        self.create_normal_switch("tasks.help_alliance_building.enabled", "Help Alliance Buildings")
        #
        self.create_advanced_switch("tasks.kill_barbarian.enabled", "Hunt Barbarians", PageBarbs)
        self.create_advanced_switch("tasks.alliance_fort.enabled", "Start Fort Rally", PageRally)
        self.create_advanced_switch("tasks.marauders.enabled", "Kill Marauders", PageMarauders)
        self.create_advanced_switch("tasks.explore_fog.enabled", "Explore Fog", PageFog)
        self.create_advanced_switch("tasks.upgrade_city.enabled", "Upgrade City", PageUpgradeCity)
        self.create_advanced_switch("tasks.academic_research.enabled", "Academic Research", PageAcademyResearch)

        self.create_advanced_switch("tasks.troop_healing.enabled", "Troops Healing", PageHeal)
        self.create_advanced_switch("tasks.resources_transfer.enabled", "Transfer Resources", PageTransfer)
        #
        self.content.controls.append(ft.Divider())
        #
        self.create_advanced_switch("log_back_from_error.enabled", "Reconnect on Network Issues", PageLogbackFromError)
        self.create_advanced_switch("log_back_from_device_switch.enabled", "Reconnect on Device Switch", PageLogbackFromDeviceSwitch)
        self.create_normal_switch("captcha_solver.enabled", "Solve Captcha")
        self.create_advanced_switch("switch_character.enabled", "Switch Characters", PageCharacter)

        self.create_slow_mode()

    def page_character(self):
        
        self.clean()
        self.content = ft.ListView(
            height=500,
            expand=0,
            padding=ft.padding.only(right=20),
        )
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: self.reset()),
                    ft.Text("Settings", size=20),
                ],
            )
        )
        self.content.controls.append(
            ft.Divider(),
        )
        self.content.controls.append(
            ft.Switch(
                label="Restart the game after switching\nto a new character (prevent freeze)",
                value=self.context.enable_switch_character_restart_during_game_load,
                on_change=self.submit_with_context,
                data={"path": "enable_switch_character_restart_during_game_load", "type": bool},
            )
        )
        ss.page.update()

    def handleSettings(self, function):
        function(self)
        ss.page.update()

    def submit_with_context(self, e):
        rsetattr(
            ss.emulator_settings.emulators[str(self.instance_index)].schedules[str(self.profile_index)],
            e.control.data["path"],
            e.control.data["type"](e.control.value),
        )
        ss.write_emulator_settings(ss.emulator_settings)

    def create_normal_switch(self, keyword: str, text: str):
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate(text),
                        value=rgetattr(self.context, keyword),
                        on_change=self.submit_with_context,
                        data={"path": keyword, "type": bool},
                    )
                ]
            )
        )

    def create_advanced_switch(self, keyword: str, text: str, function: callable):
        disabled = False

        if VERSION_TYPE == "brazilian":
            if keyword == "tasks.gather_gem.enabled":
                if ApiSingleton().getTier() == 'tier2':
                    disabled = True
            if keyword == "tasks.gather_rss.enabled":
                if ApiSingleton().getTier() == 'tier1':
                    disabled = True

        if disabled:
            value = False
        else:
            value = rgetattr(self.context, keyword)

        switch = ft.Switch(
                        label=translate(text),
                        value=value,
                        on_change=self.submit_with_context,
                        data={"path": keyword, "type": bool},
                        disabled=disabled
                    )

        if disabled:
            switch = ft.Tooltip(
                message="This feature is only available for other tiers",
                content=switch
            )
        self.content.controls.append(
            ft.Row(
                controls=[
                    switch,
                    ft.Row(
                        controls=[
                            ft.OutlinedButton(
                                text=translate("Settings"),
                                icon=ft.icons.SETTINGS,
                                on_click=lambda _: self.handleSettings(function),
                                style=ButtonStyle(
                                    shape={
                                        ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                                    }
                                )
                            )
                        ]
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )

    def create_slow_mode(self):
        self.content.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate("Reduce bot speed"),
                        value=self.context.sleep_factor.enabled,
                        on_change=self.submit_with_context,
                        data={"path": "sleep_factor.enabled", "type": bool},
                    ),
                    ft.Dropdown(
                        width=125,
                        label="Factor",
                        options=[
                            ft.dropdown.Option("0.5x"),
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
                        value=str(self.context.sleep_factor.factor) + "x",
                        on_change=self.submit_with_context,
                        data={"path": "sleep_factor.factor", "type": lambda element: float(element.replace("x", ""))},
                        height=50,
                        content_padding=ft.Padding(left=5, top=3, right=5, bottom=3),  # modify to your likings
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            )
        )
