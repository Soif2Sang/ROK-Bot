import flet as ft
from flet import Container, Image, Page, colors


def main(page: Page):
    svg_content = """
<svg xmlns="http://www.w3.org/2000/svg" version="1.1" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:svgjs="http://svgjs.dev/svgjs" width="350" height="560" preserveAspectRatio="none" viewBox="0 0 350 560">
    <g mask="url(&quot;#SvgjsMask1030&quot;)" fill="none">
        <rect width="350" height="560" x="0" y="0" fill="url(&quot;#SvgjsLinearGradient1031&quot;)"></rect>
        <path d="M350 0L321.91 0L350 46.25z" fill="rgba(255, 255, 255, .1)"></path>
        <path d="M321.91 0L350 46.25L350 139.82999999999998L302.87 0z" fill="rgba(255, 255, 255, .075)"></path>
        <path d="M302.87 0L350 139.82999999999998L350 384.4L300.59000000000003 0z" fill="rgba(255, 255, 255, .05)"></path>
        <path d="M300.59000000000003 0L350 384.4L350 444.67999999999995L186.48000000000002 0z" fill="rgba(255, 255, 255, .025)"></path>
        <path d="M0 560L106.44 560L0 512.69z" fill="rgba(0, 0, 0, .1)"></path>
        <path d="M0 512.69L106.44 560L218.66 560L0 264.63000000000005z" fill="rgba(0, 0, 0, .075)"></path>
        <path d="M0 264.63L218.66 560L274.79 560L0 261.96z" fill="rgba(0, 0, 0, .05)"></path>
        <path d="M0 261.96L274.79 560L285.81 560L0 208.39999999999998z" fill="rgba(0, 0, 0, .025)"></path>
    </g>
    <defs>
        <mask id="SvgjsMask1030">
            <rect width="350" height="560" fill="#ffffff"></rect>
        </mask>
        <linearGradient x1="-15%" y1="9.38%" x2="115%" y2="90.63%" gradientUnits="userSpaceOnUse" id="SvgjsLinearGradient1031">
            <stop stop-color="#0e2a47" offset="0"></stop>
            <stop stop-color="#00459e" offset="1"></stop>
        </linearGradient>
    </defs>
</svg>"""
    page.add(
        ft.Row(
            spacing=0,
            controls=[
                Container(
                    Image(src=svg_content, width=350, height=560, color="white"),
                    bgcolor=colors.DEEP_PURPLE_900,
                ),
                Container(
                    border_radius=5,
                    height=560,
                    width=350,
                    bgcolor=ft.colors.WHITE
                    ,
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        height=560,
                        alignment=ft.MainAxisAlignment.CENTER,
                        controls=[
                            ft.Text(
                                "Welcome Back",
                                color=ft.colors.DEEP_PURPLE_900,
                                width=250,
                                size=30,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Sign in to your account",
                                width=250,
                                color=ft.colors.GREY_500,

                            ),
                            ft.TextField(label="Username", width=250,focused_border_color=ft.colors.DEEP_PURPLE_900),
                            ft.TextField(label="Password", width=250),
                            ft.ElevatedButton(
                                "Login",
                                width=250,
                                bgcolor=ft.colors.DEEP_PURPLE_900,
                                color="white"

                            ),
                            ft.ElevatedButton("Renew", width=250, bgcolor=ft.colors.GREY_200, color=
                                              ft.colors.DEEP_PURPLE_900),
                        ],
                    ),
                ),
            ],
        )
    )


ft.app(target=main)
