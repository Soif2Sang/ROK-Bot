import json
import os
import sys
import threading
from datetime import datetime, timezone
from time import sleep

import flet as ft
import gotrue

from functions import find_file_in_all_drives
from utils.discord_server import start_server
from utils.schemas.application_schemas import UserSchema

from utils.constants import BOT_NAME, VERSION_TYPE
from utils.flet_translations import translate
from utils.singletons import ApiSingleton, FileSingleton, ss, SettingsSingleton
from utils.supabase_auth import HwidAlreadyLinked, NoSubscriptionFound, SupabaseClient

links = {
    "stripe": {
        "default": "https://buy.stripe.com/dR66oX4ov0qldkQaEF",
        # "tier2": "https://buy.stripe.com/eVa6oXcV1dd7a8E4gi",
        # "tier3": "https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn",
        # "tier4": "https://buy.stripe.com/dR6fZxf39gpjfsY9AE",
    },
    "sellix": {
        "default": "https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099",
        # "tier2": "https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601",
        # "tier3": "https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3",
        # "tier4": "https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b",
    },
}

tiers = {"default": "Tier 1", "tier2": "Tier 2", "tier3": "Tier 3", "tier4": "Tier 4"}

sellix_icon = "https://play-lh.googleusercontent.com/k_QwUjQQ7ZLilxE4at86Pn6Bpmef-60p23x4FUve-SKtbDPGJcyYN791xPw2ml-xmc1E=s256-rw"
stripe_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"


def update_user_info(email, password):
    ss.application_settings.user = UserSchema(email=email, password=password)
    ss.write_application_settings(ss.application_settings)


textField = {
    "content_padding": ft.padding.all(10),
    "color": ft.colors.INVERSE_PRIMARY,
    "label_style": ft.TextStyle(color=ft.colors.SURFACE_VARIANT),
}


class LoginScreen(ft.ResponsiveRow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        button_style = ft.ButtonStyle(
            shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5)},
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK,
        )

        self.textfield_username = ft.TextField(label=translate("Email"), value=ss.application_settings.user.email, **textField)
        self.textfield_password = ft.TextField(label=translate("Password"), value=ss.application_settings.user.password, **textField)
        self.button_login = ft.OutlinedButton(text=translate("Submit"), style=button_style, col=12, on_click=self.login)

        auth_col = ft.Column(
            controls=[
                ft.Text(translate("Login"), size=20, color=ft.colors.BLACK, weight=ft.FontWeight.W_600),
                self.textfield_username,
                self.textfield_password,
                ft.ResponsiveRow(controls=[self.button_login]),
                ft.Text("Language:", color=ft.colors.BLACK, weight=ft.FontWeight.W_400),
                ft.SegmentedButton(
                    on_change=self.save_language,
                    selected={SettingsSingleton().application_settings.version_language},
                    allow_multiple_selection=False,
                    segments=[
                        ft.Segment(
                            value="en",
                            label=ft.Text("EN", color=ft.colors.BLACK),
                        ),
                        ft.Segment(
                            value="br",
                            label=ft.Text("BR", color=ft.colors.BLACK),
                        ),
                    ],
                )
            ],
        )

        stripe_col = ft.Column(col=6)
        sellix_col = ft.Column(col=6)

        for tier in links["stripe"]:
            stripe_col.controls.append(ClickableLink("Stipe Paywall", links["stripe"][tier], stripe_icon))
        for tier in links["sellix"]:
            sellix_col.controls.append(ClickableLink("Crypto Paywall", links["sellix"][tier], sellix_icon))

        if VERSION_TYPE == "global":
            tier_col = ft.Column(
                controls=[
                    ft.Text("Where to subscribe", size=20, color=ft.colors.GREY_700, weight=ft.FontWeight.W_400),
                    stripe_col,
                    sellix_col,
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        else:
            tier_col = ft.Column(
                controls=[
                    ClickableLink(
                        translate("Our Website"), "https://rokbotsbrasil.com/#", "https://rokbotsbrasil.com/images/willy%20wonka%20logo.png"
                    ),
                    ClickableLink(
                        "Discord",
                        "https://discord.com/invite/bGqsXm3HTs",
                        "https://assets.stickpng.com/images/62b2261f038aad4d3ed7ca48.png",
                    ),
                    ClickableLink(
                        "Whatsapp",
                        "https://api.whatsapp.com/send/?phone=5521989499644&text&type=phone_number&app_absent=0",
                        "https://static.whatsapp.net/rsrc.php/v3/y7/r/DSxOAUB0raA.png",
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            )
        self.controls = [
            ft.Container(
                bgcolor=ft.colors.GREY_100,
                col=6,
                height=1080 / 2,
                width=1920 / 4,
                content=ft.Container(content=auth_col, height=250, width=1920 / 7),
                alignment=ft.alignment.center,
            ),
            ft.Container(
                bgcolor="white",
                col=6,
                height=1080 / 2,
                width=1920 / 4,
                content=ft.Container(content=tier_col, height=210, width=1920 / 6, alignment=ft.alignment.center),
                alignment=ft.alignment.center,
            ),
        ]
        self.spacing = 0

    def save_language(self, e):
        print(e.data)
        SettingsSingleton().application_settings.version_language = json.loads(e.data)[0]
        SettingsSingleton().write_application_settings(SettingsSingleton().application_settings)

    def login(self, e):
        email = self.textfield_username.value.strip()
        password = self.textfield_password.value.strip()

        if email == "" or password == "":
            return

        # ss.page.splash = ft.ProgressBar()
        self.button_login.disabled = True
        ss.page.update()

        try:
            client = SupabaseClient()
            client.login(email, password)
            client.check_hwid()

            subscriptions = client.getSubscriptions()

            if not subscriptions:
                raise NoSubscriptionFound()

            for subscription in subscriptions:
                ApiSingleton().setTier(tier=subscription["tier"])
                target_date = datetime.fromisoformat(subscription["end_at"]).astimezone()

            update_user_info(email, password)
            captcha_key = client.getApiKey("2captcha")

            ss.page.subscription_checker = threading.Thread(target=self.verify_subscription, args=(email, password))
            ss.page.subscription_checker.start()

            ApiSingleton().setApiKey(captcha_key["value"])

            current_date = datetime.now(timezone.utc).astimezone()
            days = (target_date - current_date).days

            ss.page.title = f"{BOT_NAME} - {days} Days left"
            ss.page.update()

            if (not ss.application_settings.paths.ldplayer.ldconsole and not ss.application_settings.paths.ldplayer.ldconsole) or (not os.path.exists(ss.application_settings.paths.ldplayer.ldconsole) and not os.path.exists(ss.application_settings.paths.ldplayer5.ldconsole)):
                ss.page.go("/emulator-loading")
                ss.page.update()

                if ld9_path := find_file_in_all_drives(r"LDPlayer9\\ldconsole\.exe"):
                    ss.application_settings.paths.ldplayer.ldconsole = ld9_path
                    ss.write_application_settings(ss.application_settings)

                if ld5_path := find_file_in_all_drives(r"LDPlayer64\\ldconsole\.exe"):
                    ss.application_settings.paths.ldplayer5.ldconsole = ld5_path
                    ss.write_application_settings(ss.application_settings)

                if not (ld9_path and ld5_path):
                    ss.page.generate_toast("LD Missing", "Unable to load LdPlayer9 and LdPlayer5 configurations")
                    while 1:
                        sleep(1)

            ss.page.go("/emulator-choice")

            if email == "eduardo.duuh96@gmail.com":
                threading.Thread(target=start_server).start()

        except HwidAlreadyLinked:
            if hasattr(ss.page, "generate_toast"):
                ss.page.generate_toast(f"Cannot login to {BOT_NAME}.", "This account is already linked to another computer.")
            sleep(5)
        except gotrue.errors.AuthApiError as e:
            sleep(5)
        except NoSubscriptionFound:
            if hasattr(ss.page, "generate_toast"):
                ss.page.generate_toast("Subscription error", "You don't have a active subscription yet!")
            sleep(5)
        except Exception as e:
            ss.page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()
        finally:
            # ss.page.splash = None
            self.button_login.disabled = False
            ss.page.update()

    def verify_subscription(self, email, password):
        try:
            client = SupabaseClient()
            client.login(email, password)
            client.check_hwid()

            subscriptions = client.getSubscriptions()

            if not subscriptions:
                raise NoSubscriptionFound()

            for subscription in subscriptions:
                ApiSingleton().setTier(tier=subscription["tier"])
                target_date = datetime.fromisoformat(subscription["end_at"]).astimezone()

            current_date = datetime.now(timezone.utc).astimezone()
            days = (target_date - current_date).days

            ss.page.title = f"{BOT_NAME} - {days} Days left"
            ss.page.update()
            sleep(6 * 3600)
            return self.verify_subscription(email, password)
        except Exception as e:
            ss.page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()


class ClickableLink(ft.Container):
    def __init__(self, tier, link, image, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.height = 50
        self.width = 160
        self.bgcolor = ft.colors.SURFACE
        self.border_radius = 3

        self.content = ft.Row(
            controls=[ft.Container(content=ft.Image(src=image, width=40, height=50), padding=ft.padding.all(3)), ft.Text(tier)],
            spacing=5,
            alignment=ft.alignment.center_left,
        )

        self.bgcolor = ft.colors.SURFACE
        self.border = ft.border.all(2, ft.colors.SURFACE_VARIANT)
        self.on_hover = self.hover
        self.link = link
        self.on_click = self.click

    def click(self, e):
        self.page.launch_url(self.link)

    def hover(self, e):
        e.control.bgcolor = ft.colors.SURFACE_VARIANT if (e.data == "true") else ft.colors.SURFACE

        e.control.border = ft.border.all(1, ft.colors.GREY_300) if (e.data == "true") else ft.border.all(2, ft.colors.SURFACE_VARIANT)

        self.update()


def main(page: ft.Page):
    page.add(LoginScreen())


if __name__ == "__main__":
    ft.app(main)
