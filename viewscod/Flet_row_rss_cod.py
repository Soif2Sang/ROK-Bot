import flet as ft

from utils.Task_utils import FileSingleton


class FletRowRss(ft.Row):
    def __init__(self, key, instance_index, profile_index):
        super().__init__()
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.controls=[
                    ft.Container(
                        width=100,
                        content=ft.Text(f"{key} choice :"),
                        alignment=ft.alignment.center_right
                    ),

                    ft.Dropdown(
                        width=140,
                        height=70,
                        label="Node Type",
                        options=[
                            ft.dropdown.Option("gold"),
                            ft.dropdown.Option("wood"),
                            ft.dropdown.Option("stone"),
                            ft.dropdown.Option("mana"),
                            ft.dropdown.Option('nothing')
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][f"{key}"],
                        on_change=lambda e: self.submit(e, f"{key}", str)
                    ),

                    ft.Dropdown(
                        width=140,
                        height=70,
                        label="Node Level",
                        options=[
                            ft.dropdown.Option("1"),
                            ft.dropdown.Option("2"),
                            ft.dropdown.Option("3"),
                            ft.dropdown.Option("4"),
                            ft.dropdown.Option("5"),
                            ft.dropdown.Option("6"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                            f"{key}_level"],
                        on_change=lambda e: self.submit(e, f"{key}_level", int)
                    ),
                ]

    def submit(self, e, keyword, method):
        self.data = self.FileSingleton.get_data()
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1",'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            print(self.data[str(self.instance_index)][keyword])
            self.FileSingleton.write_data(self.data)
            return
        if keyword not in ["sleep_multiplicator","defeat_barbarians"]:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(e.control.value.replace("x", "").replace("level ",""))
        self.FileSingleton.write_data(self.data)