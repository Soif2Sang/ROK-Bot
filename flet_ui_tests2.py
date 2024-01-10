import flet as ft


class Tile(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.on_click = self.click
        self.on_hover = self.hover

        self.width = 500
        self.height = 50
        self.bgcolor = ft.colors.SURFACE

        self.content = ft.Row(controls=[ft.IconButton(icon=ft.icons.SETTINGS_SHARP), ft.Text("LDPLayyer")])

    def click(self, event):
        print("click")




def main(page: ft.Page):
    page.add(ft.ListView(height=500, expand=1, controls=[Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile(), Tile()]))


ft.app(target=main)
