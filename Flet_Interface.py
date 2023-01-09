import json
import shutil
import time
from os.path import exists
from time import sleep

import flet
import flet as ft
import pyautogui
import win32gui

import test
from Flet_Countdown import Countdown


def get_dic_instances():
    try:
        with open('path.json', encoding='utf-8') as config_file:
            path = json.load(config_file)
        string = path["bluestacks"][:-5] + ".txt"
        if exists(rf'{path["bluestacks"]}'):
            string = path["bluestacks"][:-5] + ".txt"
            shutil.copy(rf'{path["bluestacks"]}', rf'{string}')
        with open(rf'{string}', 'r', encoding='utf-8') as file:
            data_instance = file.read().split('\n')
    except:
        raise OSError(
            "The path you provided is wrong ! We are looking for something like : \n r'C:\ProgramData\BlueStacks_nxt\bluestacks.conf'")

    liste_info = []
    # for element in data_instance:
    #     if ((('bst.instance.Nougat64' in element or 'bst.instance.Nougat32' in element) and (
    #             'adb_port' in element)) and 'status' in element) or (
    #             ('bst.instance.Nougat64' in element or 'bst.instance.Nougat32' in element) and (
    #             'display_name' in element)):
    #         liste_info.append(element)
    for element in data_instance:
        if ((('bst.instance.Nougat64' in element) and (
                'adb_port' in element)) and 'status' in element) or (
                ('bst.instance.Nougat64' in element) and (
                'display_name' in element)) or ((('bst.instance.Nougat32' in element) and (
                'adb_port' in element)) and 'status' in element) or (
                ('bst.instance.Nougat32' in element) and (
                'display_name' in element)):
            liste_info.append(element)
    # for element in liste_info: print(element)
    dico_instance = {}
    for i in range(0, len(liste_info), 2):
        string = liste_info[i + 1].split('.status.adb_port=')
        # print(f"{string=} ,  {liste_info[i]=}")
        string[1] = string[1].replace('"', "")
        string[0] = string[0][13:]
        dico_instance[str(len(dico_instance))] = {}
        dico_instance[str(len(dico_instance) - 1)]['instance'] = str(string[0])
        dico_instance[str(len(dico_instance) - 1)]['port'] = string[1]

        string2 = liste_info[i].split('.display_name=')
        string2[1] = string2[1].replace('"', "")
        dico_instance[str(len(dico_instance) - 1)]['name'] = string2[1]
    return dico_instance


def get_names(data):
    names = []
    for key in data.keys():
        for element in data[key]:
            if element == 'name':
                names.append((len(names), data[key][element], "", ""))
    return names


def get_current_instances(data):
    names = get_names(data)
    # print(f"{names = }")
    # print(names)
    instances_available = []
    for win in pyautogui.getAllWindows():
        for name in names:
            if win.title == name[1]:
                instances_available.append(name)
    instances_available.sort(key=lambda x: x[0])
    return instances_available


def get_all_vms_running():
    return get_current_instances(get_dic_instances())


class Main:
    def __init__(self, page: ft.Page):
        # page.scroll = "auto"
        self.page = page
        self.page.window_height = 600
        self.page.window_width = 600
        self.page.horizontal_alignment = "center"
        self.init_view = lambda _: init_view()
        self.rows =       {}
        self.containers = {}
        self.views =      {}
        self.current_container = None

        self.database = \
            ft.DataTable(
                data_row_color={ft.MaterialState.HOVERED: ft.colors.GREEN, ft.MaterialState.FOCUSED: ft.colors.GREEN},
                sort_column_index=0,
                sort_ascending=True,
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Name")),
                    ft.DataColumn(ft.Text("Task")),
                    ft.DataColumn(ft.Text("Status")),
                ]
            )

        def select_row(e):
            for key in self.rows:
                self.rows[key].color = None
            e.control.color = ft.colors.GREEN
            print(f"row select : {e.control.cells[0].content.value}")

            self.database.rows = self.rows.values()

            if self.current_container is not None:
                try:
                    page.remove(self.current_container)
                except Exception as i:
                    pass
            self.current_container = self.containers[str(int(e.control.cells[0].content.value) - 1)]
            page.add(self.current_container)
            page.update()

        def select_row2(index):
            for key in self.rows:
                # print(key)
                self.rows[key].color = None
            # print(str(index-1))
            self.rows[str(index - 1)].color = ft.colors.GREEN
            self.database.rows = self.rows.values()
            self.current_container = self.containers[str(index - 1)]
            page.add(self.current_container)
            page.update()

        def updateTable(e):
            self.rows = {}
            for i, instance in enumerate(get_all_vms_running()):
                print(i)
                self.containers[str(i)] = \
                    ft.Column(
                        alignment=ft.MainAxisAlignment.START,
                        controls=
                        [ft.Row(controls=
                                [ft.ElevatedButton(f"Start {i + 1}", icon=ft.icons.PLAY_ARROW_OUTLINED,on_click=lambda e: add_text(e, 1, "I don't know")),
                                    ft.ElevatedButton(f"Pause {i + 1}", icon=ft.icons.PAUSE_CIRCLE),
                                    ft.ElevatedButton(f"Stop {i + 1}", icon=ft.icons.STOP_CIRCLE),],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Row(controls=
                                [ft.ElevatedButton(f"SETTINGS {i + 1}", icon=ft.icons.SETTINGS,on_click=lambda _: test.main(page, i, init_view, select_row2)),],
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                            ft.Text("Logs :"),
                            ft.ListView(height=200, width=550, expand=0, spacing=10)]
                    )
                self.rows[str(i)] = ft.DataRow \
                        (
                        on_select_changed=lambda e: select_row(e),
                        cells=[
                            ft.DataCell(ft.Text(str(instance[0]))),
                            ft.DataCell(ft.Text(str(instance[1]))),
                            ft.DataCell(ft.Text(str(instance[2]))),
                            ft.DataCell(ft.Text(str(instance[3])))
                        ],
                    )
                self.views[str(i)] = ft.View(

                )
            for y in range(50):
                add_text(e, 1, f"Line {y}")

            self.database.rows = self.rows.values()
            page.update()

        def set_timer(e, index: int, seconds: int):
            list(self.database.rows)[index].cells[3].content = Countdown(seconds)
            page.update()
            time.sleep(seconds)
            list(self.database.rows)[index].cells[3].content = ft.Text("")
            page.update()

        def set_text(e, index: int, text: str):
            print(list(self.database.rows)[index].cells[2].content)
            list(self.database.rows)[index].cells[2].content = ft.Text(text)
            page.update()

        def add_text(e, index: int, text: str):
            self.containers[str(index)].controls[-1].controls.append(ft.Text(text))
            page.update()

        self.main_page = ft.View(
                    "/",
                    [
                        self.database,
                        ft.FilledButton("Refresh DataTable", icon=ft.icons.REFRESH, on_click=updateTable),
                        ft.FilledButton("Add timer", icon=ft.icons.TIMER, on_click=lambda e: set_timer(e, 1, 60)),
                        ft.FilledButton("Add text", icon=ft.icons.TEXT_FIELDS,
                                        on_click=lambda e: set_text(e, 1, "Random text")),
                    ]
                )
        def init_view():
            page.clean()
            self.page.views.append(
                self.main_page
            )
            self.page.update()

        init_view()


ft.app(target=Main, view=ft.WEB_BROWSER)
