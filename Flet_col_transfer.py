import json

import flet as ft

class FletColumnRss(ft.Column):
    def __init__(self,instance_index, profile_index):
        super().__init__()
        with open('user_settings.json') as config_file: self.data = json.load(config_file)
        self.instance_index = instance_index
        self.profile_index = profile_index
        self.controls=[
            ft.TextField(label=f"Million of Food to transfer :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["transfer_food"]
                         ,on_change=lambda e: self.submit(e, f"transfer_food", int),content_padding=ft.padding.all(10),
                         ),
            ft.TextField(label=f"Million of Wood to transfer :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["transfer_wood"]
                         , on_change=lambda e: self.submit(e, f"transfer_wood", int),content_padding=ft.padding.all(10),
                         ),
            ft.TextField(label=f"Million of Stone to transfer :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["transfer_stone"]
                         , on_change=lambda e: self.submit(e, f"transfer_stone", int),content_padding=ft.padding.all(10),
                         ),

            ft.TextField(label=f"Million of Gold to transfer :",
                         value=self.data[str(self.instance_index)]['schedules'][str(self.profile_index)]["transfer_gold"]
                         , on_change=lambda e: self.submit(e, f"transfer_gold", int),content_padding=ft.padding.all(10),
                         )
            ]

    def submit(self, e, keyword, method):
        with open('user_settings.json') as config_file:
            self.data = json.load(config_file)
        self.data[str(self.instance_index)]['schedules'][str(self.profile_index)][keyword] = method(e.control.value) if e.control.value !="" else 0
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(self.data, indent=2))