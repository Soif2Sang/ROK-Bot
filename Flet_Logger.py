import json

import flet as ft

from Task_utils import get_data


class Logger(ft.ListView):
    def __init__(self,frame,page,**kwargs):
        super().__init__(**kwargs)
        data = get_data()
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

import json


def get_date():
    pass


class LoggerUpgrade(ft.ListView):
    def __init__(self,page,**kwargs):
        super().__init__(**kwargs)
        data = get_data()
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
        with open('user_settings.json', 'w') as f:
            json.dump(data, f, indent=2)
        self.auto_scroll= True
        self.page= page

    def add_text(self, texte:str, color=None):
        if color is None:
            text = ft.Text(value=texte,weight=ft.FontWeight.W_600)
        else:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color)
        self.controls.append(text)
        if not isinstance(self.page.controls[-1],ft.Divider):
            self.update()