import json

import flet as ft

class Logger(ft.ListView):
    def __init__(self,frame,page,**kwargs):
        super().__init__(**kwargs)
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
        with open('user_settings.json', 'w') as f:
            json.dump(data, f, indent=2)
        self.auto_scroll= data["interface"]["auto_scroll"]
        self.parent = frame
        self.page = page

    def add_text(self, texte:str, color=None):
        if color is None:
            text = ft.Text(value=texte,weight=ft.FontWeight.W_600)
        else:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color)
        self.controls.append(text)
        if self.parent == self.page.controls[-1]:
            self.update()