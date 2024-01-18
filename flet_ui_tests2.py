import flet as ft
from utils.constants import BREZILIAN, global_name, brezilian_name, ownerid, global_secret, brezilian_secret
import json

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
        print("here")
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
    links = {
        "stripe" : {
            'default' : 'https://buy.stripe.com/dR66oX4ov0qldkQaEF',
            'tier2' : 'https://buy.stripe.com/eVa6oXcV1dd7a8E4gi',
            'tier3' : 'https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn',
            'tier4' : 'https://buy.stripe.com/dR6fZxf39gpjfsY9AE',

        },
        "sellix" : {
            'default' : 'https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099',
            'tier2' : 'https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601',
            'tier3' : 'https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3',
            'tier4' : 'https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b',
        }
    }

    tiers = {
        'default': 'Tier 1',
        'tier2': 'Tier 2',
        'tier3': 'Tier 3',
        'tier4': 'Tier 4'
    }
    
    sellix_icon = "https://consumersiteimages.trustpilot.net/business-units/5f038a919ab82900015059fc-198x149-2x.avif"
    strie_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"

    stripe_col = ft.Column(controls=[ft.Text("Stripe")])
    sellix_col = ft.Column(controls=[ft.Text("Sellix")])


    for tier in links['stripe']:
        stripe_col.controls.append(ClickableLink(tiers[tier], links['stripe'][tier], strie_icon))
    for tier in links['sellix']:
        sellix_col.controls.append(ClickableLink(tiers[tier], links['stripe'][tier], sellix_icon))

    page.add(ft.Row(controls=[stripe_col, sellix_col]))



def main(page: ft.Page):
    page.window_width = 1920 / 2
    page.window_height = 1080 / 2
    page.padding = 0

    button_style = ft.ButtonStyle(
        shape={ft.MaterialState.DEFAULT: ft.RoundedRectangleBorder(radius=5)},
        color=ft.colors.WHITE,
        bgcolor=ft.colors.BLACK
    )

    auth_col = ft.Column(
        controls=[
            ft.Text("Login", size=20, color=ft.colors.BLACK, weight=ft.FontWeight.W_600),
            ft.TextField(label="Username",                              content_padding=ft.padding.all(10),
),
            ft.TextField(label="Password",                             content_padding=ft.padding.all(10),
),
            ft.ResponsiveRow(
                controls=[
                    ft.OutlinedButton(text="Submit", style=button_style, col=12),
                    # ft.OutlinedButton(text="Subscribe", style=button_style, col=6),
                ]
            )
        ],
    )


    links = {
        "stripe" : {
            'default' : 'https://buy.stripe.com/dR66oX4ov0qldkQaEF',
            'tier2' : 'https://buy.stripe.com/eVa6oXcV1dd7a8E4gi',
            'tier3' : 'https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn',
            'tier4' : 'https://buy.stripe.com/dR6fZxf39gpjfsY9AE',

        },
        "sellix" : {
            'default' : 'https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099',
            'tier2' : 'https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601',
            'tier3' : 'https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3',
            'tier4' : 'https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b',
        }
    }

    tiers = {
        'default': 'Tier 1',
        'tier2': 'Tier 2',
        'tier3': 'Tier 3',
        'tier4': 'Tier 4'
    }
    
    sellix_icon = "https://consumersiteimages.trustpilot.net/business-units/5f038a919ab82900015059fc-198x149-2x.avif"
    strie_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"

    stripe_col = ft.Column(col=6)
    sellix_col = ft.Column(col=6)


    for tier in links['stripe']:
        stripe_col.controls.append(ClickableLink(tiers[tier], links['stripe'][tier], strie_icon))
    for tier in links['sellix']:
        sellix_col.controls.append(ClickableLink(tiers[tier], links['sellix'][tier], sellix_icon))

    tier_col = ft.Column(controls=[ft.Text("Available Tiers", size=20, color=ft.colors.GREY_700, weight=ft.FontWeight.W_400), ft.ResponsiveRow(controls=[stripe_col, sellix_col])], horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    page.add(
        ft.ResponsiveRow(
            controls=[
                ft.Container(bgcolor=ft.colors.GREY_100, col=6, height=1080 / 2, width = 1920 / 4, content=ft.Container(content=auth_col, height=250,  width = 1920 / 7), alignment=ft.alignment.center),
                ft.Container(bgcolor="white", col=6, height=1080 / 2, width = 1920 / 4, content=ft.Container(content=tier_col, height=350,  width = 1920 / 6), alignment=ft.alignment.center),
                ],
            spacing=0,
        ),
    )

ft.app(target=main)
