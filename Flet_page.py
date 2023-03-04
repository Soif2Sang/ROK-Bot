import json

import flet as ft

class FletPage(ft.ListView):
    def __init__(self,tab,**kwargs):
        super().__init__(**kwargs)
        with open('user_settings.json') as config_file: self.data = json.load(config_file)
        self.tab = tab
        self.height = 500
        self.expend = 0
        self.instance_index = tab.instance_index
        self.profile_index = tab.profile_index
        self.color_choice = tab.color_choice


    def show(self):
        self.back()
        self.controls.append(
            ft.Row(
                controls=[
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK,
                        on_click=lambda _: self.back()
                    ),
                    ft.Text("Settings", size=20),
                ],
            )
        )
    def back(self):
        self.tab.reset()

    def reverse_keyword(self, keyword: str, index=None):
        if index is None:
            index = self.profile_index
        print(f"{keyword = }, {index = }, {self.instance_index =}")
        if keyword not in ["loop_task", "scheduler"]:
            self.data[str(self.instance_index)]['schedules'][str(index)][keyword] = not \
                self.data[str(self.instance_index)]['schedules'][str(index)][keyword]
        else:
            self.data[str(self.instance_index)][keyword] = not \
                self.data[str(self.instance_index)][keyword]
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))

    def submit(self, e, keyword, method):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        if keyword in ["time_to_wait_loop2", "time_to_wait_loop1", 'API_KEY']:
            self.data[str(self.instance_index)][keyword] = method(e.control.value)
            print(self.data[str(self.instance_index)][keyword])
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(self.data, indent=2))
            return
        if keyword not in ["sleep_multiplicator", "defeat_barbarians"]:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value)
        else:
            self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = float(
                e.control.value.replace("x", "").replace("level ", ""))
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))