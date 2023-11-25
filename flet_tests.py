import time

import flet as ft


class ClickableRow(ft.Row):
    def __init__(self, select, i, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.controls = [ft.Container(height=35, width=300, bgcolor="red", content=ft.ElevatedButton("Select", on_click=select, data=i))]


def main(page: ft.Page):
    lv = ft.ListView(height=400, width=300, spacing=5, expand=True)


    def select(e):
        if (len(page.controls) != 1):
            page.controls.pop()
        page.add(
            ft.Container(
                height=400, width=300, bgcolor="blue", content=ft.Text(e.control.data)
            )
        )

    for i in range(10):
        lv.controls.append(ft.Row( controls=[ClickableRow(select, i)]))
    page.add(
        lv
    )
ft.app(target=main)