import flet as ft


class ClickableLink(ft.Container):
    def __init__(self, tier, link, image, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.height = 50
        self.width = 130
        self.bgcolor = ft.colors.SURFACE
        self.border_radius = 3

        self.content = ft.Row(controls=[ft.Image(src=image, width=40, height=50), ft.Text(tier)])

        self.bgcolor = ft.colors.SURFACE
        self.border = ft.border.all(2, ft.colors.SURFACE_VARIANT)
        self.on_hover = self.hover
        self.link = link
        self.on_click = self.click

    def click(self, e):
        print("here")
        self.page.launch_url(self.link)

    def hover(self, e):
        e.control.bgcolor = ft.colors.SURFACE_VARIANT if (e.data == "true") else ft.colors.SURFACE

        e.control.border = ft.border.all(1, ft.colors.GREY_300) if (e.data == "true") else ft.border.all(2, ft.colors.SURFACE_VARIANT)

        self.update()


def main(page: ft.Page):
    links = {
        "stripe": {
            "default": "https://buy.stripe.com/dR66oX4ov0qldkQaEF",
            "tier2": "https://buy.stripe.com/eVa6oXcV1dd7a8E4gi",
            "tier3": "https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn",
            "tier4": "https://buy.stripe.com/dR6fZxf39gpjfsY9AE",
        },
        "sellix": {
            "default": "https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099",
            "tier2": "https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601",
            "tier3": "https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3",
            "tier4": "https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b",
        },
    }

    tiers = {"default": "Tier 1", "tier2": "Tier 2", "tier3": "Tier 3", "tier4": "Tier 4"}

    sellix_icon = "https://consumersiteimages.trustpilot.net/business-units/5f038a919ab82900015059fc-198x149-2x.avif"
    strie_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"

    stripe_col = ft.Column(controls=[ft.Text("Stripe")])
    sellix_col = ft.Column(controls=[ft.Text("Sellix")])

    # for tier in links["stripe"]:
    #     stripe_col.controls.append(ClickableLink(tiers[tier], links["stripe"][tier], strie_icon))
    # for tier in links["sellix"]:
    #     sellix_col.controls.append(ClickableLink(tiers[tier], links["stripe"][tier], sellix_icon))

    page.add(ft.Row(controls=[stripe_col, sellix_col]))


def payment_methods():
    links = {
        "stripe": {
            "default": "https://buy.stripe.com/dR66oX4ov0qldkQaEF",
            "tier2": "https://buy.stripe.com/eVa6oXcV1dd7a8E4gi",
            "tier3": "https://buy.stripe.com/dR614Dg7d6OJ3Kg5kn",
            "tier4": "https://buy.stripe.com/dR6fZxf39gpjfsY9AE",
        },
        "sellix": {
            "default": "https://awesomeseller.mysellix.io/pay/7e1e3c-8597df2730-7d6099",
            "tier2": "https://awesomeseller.mysellix.io/pay/53e135-2364923c3c-4f3601",
            "tier3": "https://awesomeseller.mysellix.io/pay/824e23-05d0f69c1d-b899c3",
            "tier4": "https://awesomeseller.mysellix.io/pay/e90d40-1cb16b1010-e7922b",
        },
    }

    tiers = {"default": "Tier 1", "tier2": "Tier 2", "tier3": "Tier 3", "tier4": "Tier 4"}

    sellix_icon = "https://s3-eu-west-1.amazonaws.com/tpd/logos/5f038a919ab82900015059fc/0x0.png"
    stripe_icon = "https://play-lh.googleusercontent.com/2PS6w7uBztfuMys5fgodNkTwTOE6bLVB2cJYbu5GHlARAK36FzO5bUfMDP9cEJk__cE"

    stripe_col = ft.Column(
        controls=[ft.Text("Stripe")], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER, col=6
    )
    sellix_col = ft.Column(
        controls=[ft.Text("Sellix")], alignment=ft.alignment.center, horizontal_alignment=ft.CrossAxisAlignment.CENTER, col=6
    )

    for tier in links["stripe"]:
        stripe_col.controls.append(ClickableLink(tiers[tier], links["stripe"][tier], stripe_icon))
    for tier in links["sellix"]:
        sellix_col.controls.append(ClickableLink(tiers[tier], links["sellix"][tier], sellix_icon))

    return ft.ResponsiveRow(controls=[stripe_col, sellix_col], width=300, alignment=ft.alignment.center)
