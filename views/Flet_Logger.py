import flet as ft

from utils.Task_utils import FileSingleton


class Logger(ft.ListView):
    def __init__(self,frame,page,**kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
        self.FileSingleton.write_data(data)
        self.auto_scroll= data["interface"]["auto_scroll"]
        self.parent = frame
        self.page = page

    def add_text(self, texte:str, color=None):
        if color is None:
            text = ft.Text(value=texte,weight=ft.FontWeight.W_600)
        else:
            text = ft.Text(value=texte, weight=ft.FontWeight.W_600, color=color)
        self.controls.append(text)
        if self.parent == self.page.controls[-1] :
            self.update()


def get_date():
    pass


class LoggerUpgrade(ft.ListView):
    def __init__(self,page,**kwargs):
        super().__init__(**kwargs)
        data = get_data()
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
        write_data(data)
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