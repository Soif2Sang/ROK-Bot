from utils.Task_utils import FileSingleton
import flet as ft

class InterfaceSettings(ft.Tab):
    def __init__(self, page, **kwargs):
        super().__init__(**kwargs)
        self.FileSingleton = FileSingleton()
        data = self.FileSingleton.get_data()
        if "interface" not in data:
            data["interface"] = {'auto_scroll' : True, 'auto_refresh' : True}
            self.FileSingleton.write_data(data)
        self.content = ft.Column(
            controls=[
                ft.Row(controls=[ft.Switch(label="Logger autoscroll",value=data["interface"]["auto_scroll"],on_change=lambda _: self.reverse_keyword("auto_scroll"))]),
                ft.Row(controls=[ft.Switch(label="Limit Logs to 300 (reduce lags)", value=data["interface"].get("limit_logs",False),
                                           on_change=lambda _: self.reverse_keyword("limit_logs"))]),
                ft.Row(controls=[ft.Switch(label="Enable Discord Notifications", value=data["discord"]["enabled"],on_change=lambda _: self.reverse_keyword("enabled"))]),
                ft.Row(controls=[ft.TextField(label="Your discord ID", value=data["discord"]["user_id"],on_change=self.submit)])
            ]
        )
        self.text="General Settings"


    def reverse_keyword(self, keyword:str):
        if keyword == "auto_scroll" or keyword == "limit_logs":
            data = self.FileSingleton.get_data()
            data["interface"][keyword] = not data["interface"].get(keyword, False)
            self.FileSingleton.write_data(data)
            if keyword == 'auto_scroll':
                for frame in self.page.frames:
                    self.page.frames[frame].logger.auto_scroll = data["interface"][keyword]
                self.update()
        if keyword == "enabled":
            data = self.FileSingleton.get_data()
            data["discord"]["enabled"] = not data["discord"].get(keyword, False)
            self.FileSingleton.write_data(data)

    def submit(self,e):
        data = self.FileSingleton.get_data()
        data["discord"]["user_id"] = e.control.value
        self.FileSingleton.write_data(data)