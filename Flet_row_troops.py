import json
import flet as ft

class FletRowTraining(ft.Row):
    def __init__(self, key, instance_index, profile_index):
        super().__init__()
        with open('user_settings.json') as config_file: self.data = json.load(config_file)
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