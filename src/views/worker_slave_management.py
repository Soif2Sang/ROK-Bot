from typing import List

import flet as ft
from src.utils.schemas.worker_schemas import InstanceSchema

from src.utils.flet_translations import translate
from src.utils.singletons import EmulatorSingleton, FileSingleton, SettingsSingleton

fs = FileSingleton()
ss = SettingsSingleton()


class SlaveDraggable(ft.Draggable):
    def __init__(self, instance, *args, **kwargs):
        kwargs['content'] = ft.Container(
            width=110,
            height=50,
            content=ft.Text(instance),
            data=kwargs['data'],
            bgcolor=ft.colors.OUTLINE_VARIANT,
            alignment=ft.alignment.center,
            border_radius=5,
            border=ft.border.all(2, ft.colors.ON_SURFACE_VARIANT),
            padding=ft.padding.all(3),
        )
        kwargs['group'] = "color"

        super().__init__(*args, **kwargs)


class Worker(ft.Container):
    def __init__(self, instance, manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bgcolor = ft.colors.OUTLINE_VARIANT
        self.height = 300
        self.width = 150
        self.padding = ft.padding.all(5)
        self.manager = manager
        self.border_radius = 3
        self.name = ft.Text(value=translate(f"Worker") + f" {instance}")
        self.option = ft.IconButton(icon=ft.icons.SETTINGS_SHARP, on_click=self.open_settings)
        self.slaves = ft.ListView(expand=1, height=250)
        self.content = ft.Column(
            [
                ft.Row(
                    controls=[self.name, self.option],
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                self.slaves,
            ]
        )
        self.instance = instance
        self.emulator_settings = ss.emulator_settings
        self.worker_settings = ss.worker_settings

        self.emulator_type = EmulatorSingleton().getEmulatorType()

        for instanceSchema in self.worker_settings.worker_type[self.emulator_type].workers[instance].instances:
            name = self.emulator_settings.emulators[instanceSchema.instance].name
            self.slaves.controls.append(
                ft.Chip(
                    label=ft.Text(name),
                    on_delete=self.on_delete,
                    delete_icon_tooltip="remove",
                    label_padding=0,
                    width=100,
                    height=50,
                    data=instanceSchema.instance,
                    tooltip=name,
                )
            )

            for control in self.manager.slaves.controls:
                if control.data == instanceSchema.instance:
                    self.manager.slaves.controls.remove(control)

        self.add_dragtarget()

    def open_settings(self, e):
        self.dlg_modal = ft.AlertDialog(
            content=ft.ListView(
                width=400,
                height=200,
                controls=[
                    ft.Switch(
                        label=translate("Re-do all the tasks until stopped"),
                        value=self.worker_settings.worker_type[self.emulator_type].workers[self.instance].loop_task,
                        on_change=lambda e: self.submit_with_context(
                            e, self.worker_settings.worker_type[self.emulator_type].workers[self.instance], "loop_task", bool
                        ),
                    ),
                    ft.Container(
                        ft.Text(
                            translate("Minutes to wait until the bot do the task :"),
                        ),
                        margin=ft.margin.only(left=5),
                    ),
                    ft.Container(
                        content=ft.ResponsiveRow(
                            controls=[
                                ft.TextField(
                                    label="Minimum",
                                    value=str(
                                        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].waiting_cooldown.min
                                    ),
                                    content_padding=ft.padding.all(10),
                                    col=6,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    on_change=lambda e: self.submit_with_context(
                                        e,
                                        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].waiting_cooldown,
                                        "min",
                                        int,
                                    ),
                                ),
                                ft.TextField(
                                    label="Maximum",
                                    value=str(
                                        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].waiting_cooldown.max
                                    ),
                                    content_padding=ft.padding.all(10),
                                    col=6,
                                    input_filter=ft.NumbersOnlyInputFilter(),
                                    on_change=lambda e: self.submit_with_context(
                                        e,
                                        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].waiting_cooldown,
                                        "max",
                                        int,
                                    ),
                                ),
                            ],
                        ),
                        margin=ft.margin.only(left=50, top=5),
                    ),
                    ft.Switch(
                        label=translate("Close the Emulator once all the task are completed."),
                        value=self.worker_settings.worker_type[self.emulator_type].workers[self.instance].close_emulator,
                        on_change=lambda e: self.submit_with_context(
                            e, self.worker_settings.worker_type[self.emulator_type].workers[self.instance], "close_emulator", bool
                        ),
                    ),
                ],
            ),
            actions=[
                ft.TextButton("Close", on_click=self.close_dlg),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
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
                    alignment=ft.alignment.center,
                ),
                on_accept=self.on_accept,
                on_will_accept=self.drag_will_accept,
                on_leave=self.drag_leave,
            ),
        )

        ss.page.update()

    def drag_will_accept(self, e):
        e.control.content.border = ft.border.all(2, ft.colors.BLACK45 if e.data == "true" else ft.colors.RED)
        e.control.update()

    def on_accept(self, e):
        emulator_settings = ss.emulator_settings
        src = ss.page.get_control(e.src_id)

        instance = src.content.data

        for element in self.manager.slaves.controls:
            if element.data == instance:
                self.manager.slaves.controls.remove(element)

        self.slaves.controls.remove(e.control)
        self.slaves.controls.append(
            ft.Chip(
                label=ft.Text(emulator_settings.emulators[instance].name),
                on_delete=self.on_delete,
                delete_icon_tooltip="remove",
                label_padding=0,
                width=100,
                height=50,
                data=instance,
            )
        )

        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].instances = self.get_all()
        ss.write_worker_settings(self.worker_settings)

        self.add_dragtarget()
        ss.page.update()

    def on_delete(self, e):
        emulator_settings = ss.emulator_settings

        self.manager.slaves.controls.append(SlaveDraggable(emulator_settings.emulators[e.control.data].name, data=e.control.data))
        self.slaves.controls.remove(e.control)

        self.worker_settings.worker_type[self.emulator_type].workers[self.instance].instances = self.get_all()
        ss.write_worker_settings(self.worker_settings)

        ss.page.update()

    def get_all(self):
        order: List[InstanceSchema] = []
        for control in self.slaves.controls:
            if isinstance(control, ft.Chip):
                order.append(InstanceSchema(instance=control.data))
        return order

    def submit_with_context(self, e, context, keyword, method):
        setattr(context, keyword, method(e.control.value))
        ss.write_worker_settings(self.worker_settings)


class WorkerSlaveManagement(ft.ListView):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.expand = 1

        self.slaves = ft.Row(wrap=True)
        self.workers = ft.Row(wrap=True)
        self.emulator_type = EmulatorSingleton().getEmulatorType()

        # for key, value in data.items():
        #     if isinstance(value, dict) and ("instance" in value) and value.get("emulator") == self.emulator_type:
        #         self.slaves.controls.append(SlaveDraggable(value["name"], data=value["instance"]))

        emulator_settings = ss.emulator_settings
        worker_settings = ss.worker_settings

        for emulatorSchema in emulator_settings.emulators.values():
            if emulatorSchema.emulator != self.emulator_type:
                continue
            self.slaves.controls.append(SlaveDraggable(emulatorSchema.name, data=emulatorSchema.instance))

        for workerKey in worker_settings.worker_type[self.emulator_type].workers.keys():
            self.workers.controls.append(Worker(workerKey, self))

        # for worker in data["workers"][self.emulator_type]:
        #     self.workers.controls.append(Worker(worker, self))

        self.controls = [self.slaves, ft.Divider(), self.workers]


def main(page: ft.Page):
    EmulatorSingleton().setEmulator("ld")
    page.add(WorkerSlaveManagement())


if __name__ == "__main__":
    ft.app(target=main)
