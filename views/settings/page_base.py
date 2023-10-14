import flet as ft
from utils.Task_utils import FileSingleton
from flet_core import ButtonStyle, RoundedRectangleBorder


class BasePage():
    def __init__(self, profile):
        super().__init__()
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
        self.initial_page = profile.initial_page
        self.instance_index = profile.instance_index
        self.profile_index = profile.profile_index
        self.profile = profile
        self.profile.clean()
        self.add(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.profile.reset()
                    ),
                    ft.Text("Settings", size=20),
                ],
            ),
            ft.Divider(),
        )

    def add(self, *control):
        for ctrl in control:
            self.profile.add(ctrl)

    def clean(self):
        self.profile.clean()
        self.profile.update()

    def update(self):
        self.profile.update()

    def submit(self, e, keyword, method):
        self.data = self.FileSingleton.get_data()
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1", 'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
        elif keyword not in ["sleep_multiplicator", "defeat_barbarians"]:
            if e.control.value == '':
                self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(0)
            else:
                self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(
                    e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(
                e.control.value.replace("x", "").replace("level ", ""))
        self.FileSingleton.write_data(self.data)

    def reverse_keyword(self, keyword: str):
        data = self.FileSingleton.get_data()

        if keyword == "auto_scroll" or keyword == "limit_logs":
            data["interface"][keyword] = not data["interface"].get(keyword, False)
            self.FileSingleton.write_data(data)
            if keyword == 'auto_scroll':
                for frame in self.profile.initial_page.frames:
                    self.profile.initial_page.frames[frame].logger.auto_scroll = data["interface"][keyword]
                self.initial_page.update()
        elif keyword == "enabled":
            data["discord"]["enabled"] = not data["discord"].get(keyword, False)
        elif keyword == "leave_game_loop":
            data[str(self.instance_index)][keyword] = not self.data[str(self.instance_index)][keyword]
        else:
            data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = not self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword]

        self.data = data

        self.FileSingleton.write_data(data)

    def create_normal_switch(self, keyword: str, text: str):
        self.data = self.FileSingleton.get_data()
        return ft.Switch(
            label=text,

            value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                keyword] else False,
            on_change=lambda _: self.reverse_keyword(keyword)
        )

    def create_advanced_switch(self, keyword: str, text: str, function):
        self.data = self.FileSingleton.get_data()
        if keyword not in ["loop_task", "scheduler"]:
            return ft.Row(
                controls=[
                    ft.Switch(
                        label=text,

                        value=True if self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                            keyword] else False,
                        on_change=lambda _: self.reverse_keyword(keyword),

                    ),
                    ft.OutlinedButton(
                        text="Settings",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: function()
                        , style=ButtonStyle(shape={
                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                        })
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            )
        else:
            return ft.Row(
                controls=[
                    ft.Switch(
                        label=text,

                        value=True if self.data[str(self.instance_index)][keyword] else False,
                        on_change=lambda _: self.reverse_keyword(keyword),
                    ),
                    ft.OutlinedButton(
                        text="Settings",
                        icon=ft.icons.SETTINGS,
                        on_click=lambda _: function(), style=ButtonStyle(shape={
                            ft.MaterialState.DEFAULT: RoundedRectangleBorder(radius=5),
                        }, ),
                    )
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
