import flet as ft

from utils.singletons import FileSingleton, EmulatorSingleton

fs = FileSingleton()
data = fs.getCachedData()

class SlaveDraggable(ft.Draggable):
    def __init__(self, instance, *args, **kwargs):
        super().__init__( *args, **kwargs)
        self.group = "color"
        self.content = ft.Container(
            width=110,
            height=50,
            content=ft.Text(instance),
            data=self.data,
            bgcolor=ft.colors.OUTLINE_VARIANT,
            alignment=ft.alignment.center,
            border_radius=5
        )

class Worker(ft.Container):
    def __init__(self, instance, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgcolor = ft.colors.OUTLINE_VARIANT
        self.height = 300
        self.width = 150
        self.padding = ft.padding.all(5)
        self.initial_page = manager.initial_page
        self.manager = manager
        self.border_radius = 3
        self.name = ft.Text(value=f"Worker {instance}")
        self.option = ft.IconButton(icon=ft.icons.SETTINGS_SHARP, on_click=self.open_settings)
        self.slaves = ft.ListView(expand=1, height=250)
        self.content = ft.Column([ft.Row(controls=[self.name, self.option], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, vertical_alignment=ft.CrossAxisAlignment.CENTER), self.slaves])
        self.instance = instance

        for instance in data['workers'][EmulatorSingleton().getEmulator()][instance]["instances"]:
            i = instance['instance']
            self.slaves.controls.append(
                ft.Chip(
                    label=ft.Text(data[i]['name']),
                    on_delete=self.on_delete,
                    delete_icon_tooltip="remove",
                    label_padding=0,
                    width=100,
                    height=50,
                    data=i,
                    tooltip=data[i]['name']
                )
            )

            for control in self.manager.slaves.controls:
                if control.data == i:
                    self.manager.slaves.controls.remove(control)

        self.add_dragtarget()

    def open_settings(self, e):
        self.dlg_modal = ft.AlertDialog(
            content=ft.ListView(width=400, height=200, controls=[
                ft.Switch(
                    label="Re-do all the tasks until stopped",
                    value=data['workers'][EmulatorSingleton().getEmulator()][self.instance]["loop_task"],
                    on_change=lambda e: self.reverse_keyword(e, "loop_task"),
                ),
                ft.Container(
                    ft.Text(
                        "Minutes to wait until the bot do the task :",
                    ),
                    margin=ft.margin.only(left=5),
                ),
                ft.Container(
                    content=ft.ResponsiveRow(
                        controls=[
                            ft.TextField(
                                label="Minimum",
                                value=data['workers'][EmulatorSingleton().getEmulator()][self.instance]["waiting_cooldown"][0],
                                content_padding=ft.padding.all(10),
                                col=6,
                                input_filter=ft.NumbersOnlyInputFilter(),
                                on_change=lambda e: self.submit_keyword(e, "waiting_cooldown", 0)
                            ),
                            ft.TextField(
                                label="Maximum",
                                value=data['workers'][EmulatorSingleton().getEmulator()][self.instance]["waiting_cooldown"][1],
                                content_padding=ft.padding.all(10),
                                col=6,
                                input_filter=ft.NumbersOnlyInputFilter(),
                                on_change=lambda e: self.submit_keyword(e, "waiting_cooldown", 1)
                            ),
                        ],
                    ),
                    margin=ft.margin.only(left=50, top=5),
                ),
            ]),
            actions=[
                ft.TextButton("Close", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )

        self.open_dlg(e)

    def close_dlg(self, e):
        self.dlg_modal.open = False
        self.page.update()

    def open_dlg(self, e):
        self.page.dialog = self.dlg_modal
        self.dlg_modal.open = True
        self.page.update()


    def drag_leave(self, e):
        e.control.content.border = None
        e.control.update()

    def add_dragtarget(self):
        self.slaves.controls.append(
            ft.DragTarget(
                group="color",
                content=ft.Container(
                    width=50,
                    height=50,
                    bgcolor=ft.colors.BACKGROUND,
                    border_radius=5,
                    margin=ft.margin.symmetric(horizontal=10),
                    content=ft.Icon(name=ft.icons.ADD),
                    alignment=ft.alignment.center
                ),
                on_accept=self.on_accept,
                on_will_accept=self.drag_will_accept,
                on_leave=self.drag_leave
            ),
        )

        self.initial_page.update()

    def drag_will_accept(self, e):
        e.control.content.border = ft.border.all(
            2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED
        )
        e.control.update()

    def on_accept(self, e):
        data = fs.getCachedData()
        src = self.initial_page.get_control(e.src_id)

        instance = src.content.data

        for element in self.manager.slaves.controls:
            if element.data == instance:
                self.manager.slaves.controls.remove(element)

        self.slaves.controls.remove(e.control)
        self.slaves.controls.append(
            ft.Chip(
                label=ft.Text(data[instance]['name']),
                on_delete=self.on_delete,
                delete_icon_tooltip="remove",
                label_padding=0,
                width=100,
                height=50,
                data=instance
            )
        )

        data['workers'][EmulatorSingleton().getEmulator()][self.instance]["instances"] = self.get_all()

        fs.write_data(data)

        self.add_dragtarget()
        self.initial_page.update()

    def on_delete(self, e):
        data = fs.getCachedData()

        self.manager.slaves.controls.append(SlaveDraggable(data[e.control.data]['name'], data=e.control.data))
        self.slaves.controls.remove(e.control)

        data['workers'][EmulatorSingleton().getEmulator()][self.instance]["instances"] = self.get_all()
        fs.write_data(data)

        self.initial_page.update()


    def get_all(self):
        order = []
        for control in self.slaves.controls:
            if isinstance(control, ft.Chip):
                order.append(
                    {"instance": control.data}
                )

        return order

    def reverse_keyword(self, e, param):
        data = fs.getCachedData()
        data['workers'][EmulatorSingleton().getEmulator()][self.instance][param] = e.control.value
        fs.write_data(data)

    def submit_keyword(self, e, param, index):
        if not e.control.value:
            e.control.value = "0"
            self.initial_page.update()

        data = fs.getCachedData()
        data['workers'][EmulatorSingleton().getEmulator()][self.instance][param][index] = int(e.control.value)
        fs.write_data(data)

class WorkerSlaveManagement(ft.ListView):
    def __init__(self,page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_page = page
        self.expand = 1

        self.slaves = ft.Row(wrap=True)
        self.workers = ft.Row(wrap=True)

        data = FileSingleton().getCachedData()

        for key, value in data.items():
            if isinstance(value, dict) and ("instance" in value):
                self.slaves.controls.append(SlaveDraggable(value['name'], data=value['instance']))

        for worker in data["workers"][EmulatorSingleton().getEmulator()]:
            self.workers.controls.append(
                Worker(worker, self)
        )

        self.controls = [self.slaves, ft.Divider(), self.workers]


def main(page:ft.Page):
    EmulatorSingleton().setEmulator("ld")
    page.add(WorkerSlaveManagement(page))


if __name__ == "__main__":
    ft.app(target=main)
