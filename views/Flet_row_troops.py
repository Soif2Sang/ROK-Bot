import flet as ft

from utils.Task_utils import get_data, write_data


class FletRowTraining(ft.Row):
    def __init__(self, key, instance_index, profile_index):
        super().__init__()
        self.data = get_data()
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.content_padding = ft.padding.all(10)
        self.controls=[
                    ft.Switch(
                        label=f"Train {key}",
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][f"{key}_enable"],
                        on_change=lambda e: self.submit(e, f"{key}_enable", bool)
                    ),
                    ft.Dropdown(
                        width=140,
                        label=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][f"{key}_tier"],
                        options=[
                            ft.dropdown.Option("t1"),
                            ft.dropdown.Option("t2"),
                            ft.dropdown.Option("t3"),
                            ft.dropdown.Option("t4"),
                            ft.dropdown.Option("t5"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][f"{key}_tier"],
                        on_change=lambda e: self.submit(e, f"{key}_tier", str)
                    )
                ]

    def submit(self, e, keyword, method):
        self.data = get_data()

        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1",'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            print(self.data[str(self.instance_index)][keyword])
            write_data(self.data)
            return
        if keyword not in ["sleep_multiplicator","defeat_barbarians"]:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(e.control.value.replace("x", "").replace("level ",""))
        write_data(self.data)