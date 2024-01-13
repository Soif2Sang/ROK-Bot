import flet as ft

from utils.functions import get_dic_instances_ld, get_dic_instances
from utils.singletons import FileSingleton, EmulatorSingleton


class EmulatorGroup(ft.Row):
    def __init__(self, instance, instances, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance = instance[0]
        self.controls.append(ft.Text(f"Emulator n°{instance[0]}"))
        data = FileSingleton().get_data()

        if data[self.instance].get("group", -1) == -1:
            data[self.instance]["group"] = self.instance[0]
            FileSingleton().write_data(data)

        options = []

        for instance in instances:
            options.append(ft.dropdown.Option(text=f"Worker n°{instance[0]}", key=instance[0]))

        self.controls.append(ft.Dropdown(options=options, on_change=self.on_change, value=data[self.instance]["group"]))

    def on_change(self, e):
        data = FileSingleton().get_data()

        data[self.instance]["group"] = e.control.value

        FileSingleton().write_data(data)
