import flet as ft

class Logger(ft.ListView):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.auto_scroll= True

    def add_text(self, texte:str, color="black"):
        self.controls.append(ft.Text(value=texte,weight=ft.FontWeight.W_600,color=color))
