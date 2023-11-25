import flet as ft
from flet_core import ButtonStyle, RoundedRectangleBorder


def main(page):
    page.add(
        ft.Stack(
            [
                ft.Switch(
                    label="Gem gathering",
                ),
                ft.Badge(text="New", alignment= ft.alignment.top_right)
            ],
        ),

        ft.Divider(),
        ft.Stack(
            [
                ft.Switch(
                    label="Gem gathering",
                ),
                ft.Badge(text="Updated", alignment=ft.alignment.top_right)
            ],width=200
        ),
        ft.Divider(),
        ft.Stack(
            [
                ft.OutlinedButton(
                    text="Settings",
                    icon=ft.icons.SETTINGS,
                    style=ButtonStyle(shape={
                        ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                    })
                ),
                # ft.Badge(text="Updated", alignment=ft.alignment.top_right)
            ]
        ),
        ft.OutlinedButton(
            text="Settings",
            icon=ft.icons.SETTINGS,
            style=ButtonStyle(shape={
                ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
            })
        ),


    )

ft.app(target=main)