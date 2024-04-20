import flet as ft

from flet_translations import translate

import flet as ft


def main(page):
    def radiogroup_changed(e):
        t.value = f"Your favorite color is:  {e.control.value}"
        page.update()

    t = ft.Text()
    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value="red", label="Red"),
        ft.Container(
            margin=ft.margin.only(left=50),
            content=ft.TextField(label="test")
        ),
        ft.Radio(value="green", label="Green"),
        ft.Radio(value="blue", label="Blue")]), on_change=radiogroup_changed)

    page.add(ft.Text("Select your favorite color:"), cg, t)


ft.app(target=main)