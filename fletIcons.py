import re

import flet as ft


class FletIcons(ft.UserControl):
    """Icons Flet to select"""

    def __init__(self, data='Erase this test'):
        super().__init__()
        self.title = data
        self.DropFletIcons = ft.Container(
            ##################### PROPERTY ROW
            ink=False,  # click effect ripple
            padding=ft.padding.all(0),
            # inside box                        # padding.only(left=8, top=8, right=8, bottom=8),
            margin=ft.margin.all(0),
            # outside box                       # margin.only (left=8, top=8, right=8, bottom=8),
            alignment=ft.alignment.center,
            # top_left,top_center,top_right,center_left,center,center_right,bottom_left,bottom_center,bottom_right
            content=ft.Column(
                spacing=10,
                controls=[
                    ft.TextField(on_change=self.on_type),
                    # ft.Divider(),

                    ft.GridView(
                        ##################### PROPERTY GRIDVIEW
                        runs_count=10,  # column's number
                        run_spacing=0,  # space between widget
                        padding=0,
                        spacing=0,  # space widget left right

                        ##################### WIDGETS
                    ),
                ], scroll=ft.ScrollMode.ALWAYS,expand=1,
            )
            # <=== NOTE COMA [NOTE]                       for x in range(1,50): widget.content.controls.append(ft.ElevatedButton("press buttom",tooltip='buttom'))
        )  # <=== NOTE COMA

    def initialize(self):
        icons = dir(ft.icons)

        for num, x in enumerate(icons):
            if not x.startswith('_'):
                self.DropFletIcons.content.controls[1].controls.append(ft.Icon(name=f"{x}",
                                                              color="green",
                                                              tooltip=f"{x}"
                                                              ),
                                                      )
    def search(self, word):
        icons = dir(ft.icons)
        pattern = r'\b\w*{}\w*\b'.format(re.escape(word))

        for num, x in enumerate(icons):
            matches = re.finditer(pattern, x)
            if not x.startswith('_') and matches:
                self.DropFletIcons.content.controls[1].controls.append(ft.Icon(name=f"{x}",
                                                              color="green",
                                                              tooltip=f"{x}"
                                                              ),
                                                      )
        self.update()

    def on_type(self, e):
        self.controls[0].content.controls[1].controls = []
        print(e)
        print(e.control.value)
        if e.control.value == "":
            return
            self.initialize()
        else:
            return
            self.search(e.control.value)
        print(self.controls)
        self.DropFletIcons.update()

    def build(self):


            # if num == 200:
            #      break
        self.initialize()
        return self.DropFletIcons


def configuration(self):
    ###################### CONFIGURATION
    self.title = "Icons pack"
    self.scroll = True
    self.vertical_alignment = ft.MainAxisAlignment.CENTER
    self.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    ######################  COLOR
    self.theme_mode = ft.ThemeMode.DARK  # ft.ThemeMode.LIGHT
    ###################### POSITION OF SC
    # self.window_left = 900
    # self.window_top = 8
    self.window_center()
    ###################### SIZE
    self.window_width = 640
    self.window_height = 640
    self.padding = 0
    self.spacing = 0
    self.expand = True


def main(page):
    configuration(page)
    page.add(FletIcons('hello world'))  # page.add(FletIcons()) FletIcons.action()


if __name__ == '__main__':
    ft.app(
        target=main,
        # assets_dir="assets",
    )
