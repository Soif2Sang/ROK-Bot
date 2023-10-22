import sys
import threading
from time import sleep

import flet as ft

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}


class Logger(ft.ListView):
    def __init__(self, frame, page, **kwargs):
        super().__init__(**kwargs)
        self.auto_scroll = True
        self.parent = frame
        self.initial_page = page

    def add_text(self, texte: str, color=None):
        if color is None:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, selectable=True)
        else:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color, selectable=True)
        self.controls.append(text)
        self.initial_page.update()

    def add_divider(self):
        self.controls.append(ft.Divider())
        self.initial_page.update()


class Frame(ft.Tabs):
    def __init__(self, page, number: str, **kwargs):
        super().__init__(**kwargs)
        self.number = number
        self.settings = ft.Tabs()
        self.expand = True
        self.logger = Logger(self, page)

        self.tabs.append(ft.Tab(content=self.logger, text="Logs"))

    def add_text(self, texte: str, color=None):
        self.logger.add_text(texte, color)

    def add_divider(self):
        self.logger.add_divider()


class Task:
    def __init__(self, tile):
        self.tile = tile

    def script_pause(self):
        said = False

        while self.tile.paused:
            if not said:
                self.set_text(f"Script is paused.", "orange")
                said = True

        if self.tile.stopped:
            self.set_text(f"You stopped the bot", "Red")
            self.set_divider()
            sys.exit()

        if said:
            self.set_text(f"You resumed the script.", "Green")

    def run(self):
        while 1:
            self.script_pause()
            sleep(0.001)

    def set_text(self, param, param1):
        self.tile.logs.controls.append(ft.Text(value=param, color=param1))
        self.tile.initial_page.update()

    def set_divider(self):
        self.tile.logs.controls.append(ft.Divider())
        self.tile.initial_page.update()


class Tile(ft.Row):
    def __init__(self, page, logs, **kwargs):
        super().__init__(**kwargs)
        self.initial_page = page
        self.tasks_process = None
        self.logs = logs
        self.paused = False
        self.stopped = False

        self.main_task = Task(self)

        self.tasks_process = threading.Thread(target=self.main_task.run)

        self.button_start = ft.IconButton(
            icon=ft.icons.NOT_STARTED_OUTLINED,
            on_click=self.start
        )
        self.button_stop = ft.IconButton(
            icon=ft.icons.STOP_OUTLINED,
            disabled=True,
            on_click=self.stop
        )

        self.alignment = ft.MainAxisAlignment.SPACE_BETWEEN
        self.controls.extend([
            ft.Row(
                controls=[
                    self.button_start,
                    self.button_stop
                ]
            ),
        ]
        )

    def start(self, e):
        self.button_start.icon = ft.icons.PAUSE
        self.button_stop.disabled = False

        self.paused = False
        self.stopped = False

        self.initial_page.update()
        self.start_tasks()
        self.button_start.on_click = self.pause
        self.tasks_process.join()
        self.button_start.on_click = self.start
        self.paused = False
        self.stopped = False
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.initial_page.update()

    def resume(self, e):
        self.paused = False

        self.button_start.icon = ft.icons.PAUSE
        self.initial_page.update()
        self.button_start.on_click = self.pause

    def pause(self, e):
        self.paused = True

        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.initial_page.update()
        self.button_start.on_click = self.resume

    def stop(self, e):
        self.stopped = True
        self.paused = False
        self.button_start.icon = ft.icons.NOT_STARTED_OUTLINED
        self.button_stop.disabled = True
        self.initial_page.update()

    def start_tasks(self):
        if not self.tasks_process.is_alive():
            self.tasks_process = threading.Thread(target=self.main_task.run)
            self.tasks_process.start()
        else:
            print("Task is frozen, you may need to restart the bot.")


def main(page: ft.Page):
    frame = Frame(page, '1')
    tile = Tile(page, frame.logger)

    # page.add(tile, frame)
    # page.add(
    #
    # )

def main(page: ft.Page):
    page.window_width = 450
    page.window_height = 700

    page.add(
    ft.Switch(
        label="Use normal way to upgrade the city \n(if unchecked the bot is unable to upgrade the pass but \nit is a safer way to upgrade the city)",
        width=300
    )
    )

    page.add(
        ft.ResponsiveRow(
            controls=[
                ft.Switch(col=2),
                ft.Text(col=10, value="Use normal way to upgrade the city \n(if unchecked the bot is unable to upgrade the pass but it is a safer way to upgrade the city)", text_align=ft.TextAlign.JUSTIFY)
            ],
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.MainAxisAlignment.CENTER
        )
    )
    page.update()




if __name__ == "__main__":
    ft.app(main)
