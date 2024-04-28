from time import sleep

import flet as ft

data = {
    "workers": {
        "ld": {
            "0": {"loop_task": True, "waiting_cooldown": [90, 110], "instances": [{"instance": "0"}, {"instance": "1"}]},
            "1": {"loop_task": True, "waiting_cooldown": [90, 120], "instances": [{"instance": "2"}, {"instance": "3"}]},
            "2": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "4"}, {"instance": "5"}]},
            "3": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": []},
            "4": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": []},
            "5": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": []},
        },
        "bluestacks": {
            "0": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64"}]},
            "1": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64_10"}]},
            "2": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64_13"}]},
            "3": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64_22"}]},
            "4": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64_8"}]},
            "5": {"loop_task": True, "waiting_cooldown": [60, 90], "instances": [{"instance": "Nougat64_9"}]},
        },
    }
}

fus = {"width": 100, "height": 50, "border_radius": 5, "margin": ft.margin.symmetric(horizontal=4)}

instances = ["Instance 1", "Instance 2", "Instance 3", "Instance 4", "Instance 5"]


class SlaveDraggable(ft.Draggable):
    def __init__(self, instance, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data = instance
        self.group = "all"
        self.content = ft.Container(content=ft.Text(instance), bgcolor=ft.colors.SURFACE_VARIANT, **fus)


class SlaveDragTarget(ft.DragTarget):
    def __init__(self, instance=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.group = "all"
        if instance:
            self.content = SlaveDraggable(instance)
        else:
            self.content = ft.Container(**fus, bgcolor=ft.colors.ON_SURFACE_VARIANT)

        self.on_accept = self.accept
        # self.on_leave = self.leave

    def accept(self, e):
        print(e)
        src = e.page.get_control(e.src_id)
        e.control.content = SlaveDraggable(src.data)

        self.page.update()

    def leave(self, e):
        e.control.content = ft.Container(
            width=50,
            height=50,
            bgcolor=ft.colors.BLUE_GREY_100,
            border_radius=5,
        )
        self.page.update()


class WorkerDragtarget(ft.Container):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.width = 130
        self.height = 330
        self.content = ft.Column(
            controls=[ft.Text("Worker", size=20), ft.Divider(), ft.ListView(height=300, expand=1, spacing=5)],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment=ft.alignment.center,
        )
        self.bgcolor = ft.colors.RED
        self.alignment = ft.alignment.center
        self.border_radius = 5
        self.margin = ft.margin.all(5)

        for _ in instances:
            self.add_dragtarget()

    def add_dragtarget(self):
        self.content.controls[-1].controls.append(SlaveDragTarget())


def main(page: ft.Page):
    line = ft.Row()
    for name in instances:
        line.controls.append(SlaveDragTarget(instance=name))

    page.add(line)

    page.add(WorkerDragtarget())


ft.app(target=main)
