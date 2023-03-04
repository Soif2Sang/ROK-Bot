import json

import flet as ft

class FletRowRss(ft.Row):
    def __init__(self, key, instance_index, profile_index):
        super().__init__()
        with open('user_settings.json') as config_file: self.data = json.load(config_file)
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
                            ft.dropdown.Option("food"),
                            ft.dropdown.Option("wood"),
                            ft.dropdown.Option("stone"),
                            ft.dropdown.Option("gold"),
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
                            ft.dropdown.Option("7"),
                            ft.dropdown.Option("8"),
                            ft.dropdown.Option("9"),
                        ],
                        value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][
                            f"{key}_level"],
                        on_change=lambda e: self.submit(e, f"{key}_level", int)
                    ),
                ]

    def submit(self, e, keyword, method):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1",'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            print(self.data[str(self.instance_index)][keyword])
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(self.data, indent=2))
            return
        if keyword not in ["sleep_multiplicator","defeat_barbarians"]:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(e.control.value.replace("x", "").replace("level ",""))
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))