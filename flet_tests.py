import flet as ft


def GenerateCard(level=None, title=None, subtitle=None, margin=None, height=None):


    if title:
        title = ft.Text(title, size=14, weight=ft.FontWeight.BOLD)

    return ft.Card(
        content=ft.Container(
            content=
                    ft.ListTile(
                        title=ft.Text("The Bot seems to be under maintenance, please wait a bit..")
                        , leading=ft.Icon(ft.icons.PORTABLE_WIFI_OFF_SHARP)
            ),
            width=400,
            padding=10,
            height=height,
        ),
        margin=margin,
        color=ft.colors.SURFACE_VARIANT
    )


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    page.add(
        GenerateCard()
    )

if __name__ == '__main__':
    ft.app(main)
