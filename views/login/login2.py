import os
import sys
import threading
from datetime import datetime, timezone
from time import sleep
import json
import flet as ft
import gotrue

from utils.constants import BREZILIAN, global_name, brezilian_name, ownerid, global_secret, brezilian_secret, url, key
from utils.flet_translations import translate
from utils.singletons import ApiSingleton, LinkSingleton, FileSingleton
from utils.supabase_auth import SupabaseClient

links = {
    "stripe": {
        'default': 'https://buy.stripe.com/dR66oX4ov0qldkQaEF',
        'tier2': 'https://buy.stripe.com/eVa6oXcV1dd7a8E4gi',
        'tier3': 'https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn',
        'tier4': 'https://buy.stripe.com/dR6fZxf39gpjfsY9AE',
    },
    "sellix": {
        'default': 'https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099',
        'tier2': 'https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601',
        'tier3': 'https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3',
        'tier4': 'https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b',
    }
}

tiers = {
    'default': 'Tier 1',
    'tier2': 'Tier 2',
    'tier3': 'Tier 3',
    'tier4': 'Tier 4'
}

sellix_icon = "https://consumersiteimages.trustpilot.net/business-units/5f038a919ab82900015059fc-198x149-2x.avif"
stripe_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"


def is_str_valid(username, password):
    for element in ["#", "$", "&", "|", "\0", "\n", "\r", "'", "'", '"', "\Z"]:
        if element in username or element in password:
            return False
    return True

def update_user_info(password, username):
    data = FileSingleton().get_data()
    data["user"] = {"username": username, "password": password}
    FileSingleton().write_data(data)

textField = {"content_padding" : ft.padding.all(10), "color":ft.colors.SURFACE_VARIANT, "label_style":ft.TextStyle(color=ft.colors.SURFACE_VARIANT)}

class NoSubscriptionFound(Exception):
    pass

class LoginScreen(ft.ResponsiveRow):
    def __init__(self, page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_page = page
        self.fileSingleton = FileSingleton()
        self.data = self.fileSingleton.get_data()

        button_style = ft.ButtonStyle(
            shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5)},
            color=ft.colors.WHITE,
            bgcolor=ft.colors.BLACK
        )

        self.textfield_username = ft.TextField(label="Username", **textField,
                             value=self.data.get("user", {}).get("username", ""))
        self.textfield_password = ft.TextField(label="Password",  **textField,
                             value=self.data.get("user", {}).get("password", ""))
        self.button_login = ft.OutlinedButton(text="Submit", style=button_style, col=12, on_click=self.login)

        auth_col = ft.Column(
            controls=[
                ft.Text("Login", size=20, color=ft.colors.BLACK, weight=ft.FontWeight.W_600),
                self.textfield_username,
                self.textfield_password,
                ft.ResponsiveRow(
                    controls=[
                        self.button_login
                    ]
                )
            ],
        )

        stripe_col = ft.Column(col=6)
        sellix_col = ft.Column(col=6)

        for tier in links['stripe']:
            stripe_col.controls.append(ClickableLink(tiers[tier], links['stripe'][tier], stripe_icon))
        for tier in links['sellix']:
            sellix_col.controls.append(ClickableLink(tiers[tier], links['sellix'][tier], sellix_icon))


        if not BREZILIAN:
            tier_col = ft.Column(
                controls=[ft.Text("Available Tiers", size=20, color=ft.colors.GREY_700, weight=ft.FontWeight.W_400),
                          ft.ResponsiveRow(controls=[stripe_col, sellix_col])],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER
            )
        else:
            tier_col = ft.Column(
                controls=[
                    ft.Text("Available Tiers", size=20, color=ft.colors.GREY_700, weight=ft.FontWeight.W_400),
                    ClickableLink("Tier 1", "https://rokbotsbrasil.com/#", "https://rokbotsbrasil.com/images/willy%20wonka%20logo.png"),
                    ClickableLink("Tier 2", "https://rokbotsbrasil.com/#", "https://rokbotsbrasil.com/images/willy%20wonka%20logo.png"),
                    ClickableLink("Tier 3", "https://rokbotsbrasil.com/#", "https://rokbotsbrasil.com/images/willy%20wonka%20logo.png"),
                    ClickableLink("Tier 4", "https://rokbotsbrasil.com/#", "https://rokbotsbrasil.com/images/willy%20wonka%20logo.png")

                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER

            )
        self.controls = [
            ft.Container(bgcolor=ft.colors.GREY_100, col=6, height=1080 / 2, width=1920 / 4,
                         content=ft.Container(content=auth_col, height=250, width=1920 / 7),
                         alignment=ft.alignment.center),
            ft.Container(bgcolor="white", col=6, height=1080 / 2, width=1920 / 4,
                         content=ft.Container(content=tier_col, height=350, width=1920 / 6),
                         alignment=ft.alignment.center),
        ]
        self.spacing = 0

    def login(self, e):
        username = self.textfield_username.value
        password = self.textfield_password.value

        if username == "" or password == "":
            return

        if not is_str_valid(username, password):
            self.initial_page.generate_toast("Invalid credentials", "Illegal characters..")
            return

        self.initial_page.splash = ft.ProgressBar()
        self.button_login.disabled = True
        self.initial_page.update()

        try:
            client = SupabaseClient()
            client.login(username, password)
            print("avant")
            subscriptions = client.getSubscriptions()
            print("apres")

            if (not subscriptions):
                raise NoSubscriptionFound()
            print(subscriptions, "subscriptions")
            for subscription in subscriptions:
                ApiSingleton().setTier(tier=subscription['tier'])
                target_date = datetime.fromisoformat(subscription['end_at']).astimezone()

            self.initial_page.subscription_checker = threading.Thread(
                target=self.verify_subscription,
                args=(username, password)
            )
            self.initial_page.subscription_checker.start()

            captcha_key = client.getApiKey('2captcha')
            ApiSingleton().setApiKey(captcha_key["value"])

            update_user_info(password, username)

            current_date = datetime.now(timezone.utc).astimezone()

            print(target_date, current_date)
            days = (target_date - current_date).days


            self.initial_page.title = f"RokNet - {days} Days left"
            self.initial_page.update()
            self.initial_page.go("/emulator-choice")

        except gotrue.errors.AuthApiError:
            sleep(5)
        except NoSubscriptionFound:
            if hasattr(self.initial_page, 'generate_toast'):
                self.initial_page.generate_toast("Subscription error", "You don't have a active subscription yet!")
            sleep(5)
        except Exception as e:
            print(e)
            self.initial_page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()
        finally:
            self.initial_page.splash = None
            self.button_login.disabled = False
            self.initial_page.update()

    def verify_subscription(self, username, password):
        try:
            client = SupabaseClient()
            client.login(username, password)
            subscriptions = client.getSubscriptions()

            if (not subscriptions):
                raise NoSubscriptionFound()

            for subscription in subscriptions:
                ApiSingleton().setTier(tier=subscription['tier'])
                target_date = datetime.fromisoformat(subscription['end_at']).astimezone()

            current_date = datetime.now(timezone.utc).astimezone()
            days = (target_date - current_date).days

            self.initial_page.title = f"RokNet - {days} Days left"
            self.initial_page.update()
            sleep(6)
            return self.verify_subscription(username, password)
        except Exception as e:
            print(e)
            self.initial_page.window_close()
            os.system("taskkill /f /im flet.exe >nul 2>&1")
            sys.exit()


class ClickableLink(ft.Container):
    def __init__(self, tier, link, image, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.height = 50
        self.width = 160
        self.bgcolor = ft.colors.SURFACE
        self.border_radius = 3

        self.content = ft.Row(controls=[ft.Container(content=ft.Image(src=image, width=40, height=50), padding=ft.padding.all(3)), ft.Text(tier)], spacing=15, alignment=ft.alignment.center_left)

        self.bgcolor = ft.colors.SURFACE
        self.border = ft.border.all(2, ft.colors.SURFACE_VARIANT)
        self.on_hover = self.hover
        self.link = link
        self.on_click = self.click


    def click(self, e):
        self.page.launch_url(self.link)

    def hover(self, e):
        e.control.bgcolor = (
            ft.colors.SURFACE_VARIANT
            if (e.data == "true")
            else ft.colors.SURFACE
        )

        e.control.border = (
            ft.border.all(1, ft.colors.GREY_300)
            if (e.data == "true")
            else ft.border.all(2, ft.colors.SURFACE_VARIANT)
        )

        self.update()

def main(page: ft.Page):
    page.add(LoginScreen(page))

if __name__ == "__main__":
    ft.app(main)