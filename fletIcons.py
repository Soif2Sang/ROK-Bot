import re

import flet as ft


class FletIcons(ft.UserControl):
    """Icons Flet to select"""

    def __init__(self, data='Erase this test'):
        super().__init__()
        self.title = data
        self.gridview = ft.GridView(
            runs_count=10,  # column's number
            run_spacing=0,  # space between widget
            padding=0,
            spacing=0,  # space widget left right
        )
        # self.DropFletIcons = ft.Container(
        #     padding=ft.padding.all(0),
        #     margin=ft.margin.all(0),
        #     alignment=ft.alignment.center,
        #     content=ft.Column(
        #         spacing=10,
        #         controls=[
        #             self.gridview
        #
        #         ], scroll=ft.ScrollMode.ALWAYS, expand=1,
        #     )
        #     # <=== NOTE COMA [NOTE]                       for x in range(1,50): widget.content.controls.append(ft.ElevatedButton("press buttom",tooltip='buttom'))
        # )  # <=== NOTE COMA

    def initialize(self):
        icons = dir(ft.icons)

        for num, x in enumerate(icons):
            if not x.startswith('_'):
                self.gridview.controls.append(ft.Icon(name=f"{x}",
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
                self.gridview.controls.append(ft.Icon(name=f"{x}",
                                                      color="green",
                                                      tooltip=f"{x}"
                                                      ),
                                              )

    def on_type(self, e):
        self.gridview.controls = []
        if e.control.value == "":
            self.initialize()
        else:
            self.search(e.control.value)
        self.update()

    def build(self):
        self.initialize()
        return [ft.Column(controls=[ft.TextField(on_submit=self.on_type), self.gridview])]


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

    page.dic = {}

    icons = dir(ft.icons)

    for num, x in enumerate(icons):
        if not x.startswith('_'):
            page.dic[f"{x}"] = x

    listview = ft.ListView()

    def initialize():
        for num, x in enumerate(page.dic.keys()):
            if num % 10 == 0:
                listview.controls.append(ft.Row())
            listview.controls[-1].controls.append(
                ft.Icon(name=f"{x}",
                        color="green",
                        tooltip=f"{x}",
                        size=55
                        ),
            )

    def search(e):
        listview.controls = []
        page.update()

        pattern = r'\b\w*{}\w*\b'.format(re.escape(e.control.value))
        i = 0
        for num, x in enumerate(page.dic.keys()):

            matches = re.findall(rf'\b\w*{e.control.value}\w*\b', x, flags=re.IGNORECASE)
            if matches:
                print(x)
                if i % 10 == 0:
                    listview.controls.append(ft.Row())

                listview.controls[-1].controls.append(
                    ft.Icon(name=f"{x}",
                            color="green",
                            tooltip=f"{x}",
                            size=55
                            ),
                )

                i += 1

        page.update()

    textfield = ft.TextField(on_submit=search)

    page.add(
        textfield,
        listview
    )  # page.add(FletIcons()) FletIcons.action()

    initialize()
    page.update()


if __name__ == '__main__':
    ft.app(
        target=main,
        # assets_dir="assets",
    )

