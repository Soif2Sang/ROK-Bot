import ctypes
import inspect
import json
import threading

import tkinter
from datetime import datetime, timedelta
from time import sleep
from tkinter import Text
import customtkinter

from Task import Task
from UI_Settings import Settings
from bot_adb import Adb
from Task_runner import TaskRunner



class LowerFrame():
    def __init__(self, upper_frame, sel):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        # print(data[sel[0]]['port'], type(data[sel[0]]['port']))
        self.data = data
        self.upper_frame = upper_frame
        self.root = upper_frame.root
        self.sel = sel[0]
        # self.adb = Adb(sel[0])
        # self.device = self.adb.connect_to_device()

        self.bottom_frame = customtkinter.CTkFrame(self.root)
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky='')

        self.start_tasks_button = customtkinter.CTkButton(self.bottom_frame, text="Start ▶", command=self.start_tasks, corner_radius=4,
                                                          fg_color="white")
        self.start_tasks_button.grid(row=1, column=0, columnspan=2, sticky='', pady=(10, 0))
        # , fg_color = "white

        self.pause = False
        self.stop = False
        self.pr_tasks_button = customtkinter.CTkButton(self.bottom_frame, text="⏸/▶", command=self.pause_tasks, corner_radius=4, fg_color="white",
                                                       text_color="black")
        self.pr_tasks_button.grid(row=2, column=0, columnspan=2, sticky='')

        self.end_tasks_button = customtkinter.CTkButton(self.bottom_frame, text="Stop ■", command=self.end_tasks, corner_radius=4, fg_color="white")
        self.end_tasks_button.grid(row=3, column=0, columnspan=2, sticky='')

        self.settings_button = customtkinter.CTkButton(self.bottom_frame, text="Settings ⚙", command=lambda: Settings(self), corner_radius=4,
                                                       border_color="grey", border_width=1, fg_color="white")
        self.settings_button.grid(row=4, column=0, columnspan=2, sticky='', pady=(10, 0))


        # self.main_task = Task(self)
        # self.main_task.set_sel(sel[0])
        # self.tasks = TaskRunner(self.main_tasks, self)
        # self.tasks = Task(self)
        # self.tasks.set_sel(sel[0])

        self.main_task = Task(self)
        # self.main_task.set_sel(sel[0])
        self.runner = TaskRunner(self.main_task,self)
        self.tasks_process = threading.Thread(target=self.runner.upgrade_all_accounts)



        def change_status(param):
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            data[self.sel]['schedules'][param]["enabled"] = not data[self.sel]['schedules'][param]["enabled"]
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))


        self.checkbox_p1 = customtkinter.CTkCheckBox(self.bottom_frame, text="Profile n°1", command=lambda : change_status("1"), hover_color="#266496", fg_color="#3b8ed0")
        if data[self.sel]['schedules']["1"]["enabled"]:
            self.checkbox_p1.select()
        self.checkbox_p2 = customtkinter.CTkCheckBox(self.bottom_frame, text="Profile n°2", command=lambda : change_status("2"), hover_color="#913230", fg_color="#ba4543")
        if data[self.sel]['schedules']["2"]["enabled"]:
            self.checkbox_p2.select()
        self.checkbox_p3 = customtkinter.CTkCheckBox(self.bottom_frame, text="Profile n°3", command=lambda: change_status("3"), hover_color="#baa429",  fg_color="#dec433")
        if data[self.sel]['schedules']["3"]["enabled"]:
            self.checkbox_p3.select()

        self.checkbox_p1.grid(row=1, column=1, sticky='e', pady=(10, 0), padx=(0,30))
        self.checkbox_p2.grid(row=2, column=1, sticky='e', padx=(0,30))
        self.checkbox_p3.grid(row=3, column=1, sticky='e', padx=(0,30))

        font1 = customtkinter.CTkFont(family='Helvetica bold underline', size=15)
        self.console_label = customtkinter.CTkLabel(self.bottom_frame, text="       Logs :", font=font1).grid(column=0, row=5, sticky="w")
        # self.textbox = customtkinter.CTkTextbox(self.bottom_frame, height = 150, width =400,font=('Helvetica', 15))
        self.textbox = Text(self.bottom_frame, height=6, width=50, font=('Helvetica', 12))
        self.textbox.insert("0.0", "                                     ")
        self.textbox.configure(state="disabled")
        self.textbox.grid(row=6, column=0, columnspan=2, sticky='we')

        if customtkinter.get_appearance_mode() == "Dark":
            self.start_tasks_button.configure(text_color="white")
            self.end_tasks_button.configure(text_color="white")
            self.settings_button.configure(text_color="white")
            self.textbox.configure(bg="#2b2b2b")
        else:
            self.start_tasks_button.configure(text_color="black")
            self.end_tasks_button.configure(text_color="black")
            self.settings_button.configure(text_color="black")
        if self.tasks_process.is_alive():
            self.start_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
            self.end_tasks_button.configure(state="normal", fg_color="white")
        else:
            # , fg_color = "white"
            self.end_tasks_button.configure(state="normal", fg_color="white")
            # , fg_color = "#d1d1d1"
            self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")

    def start_tasks(self):
        # try:
        #     self.runner.upgrade_all_accounts()
        # except:
        #     traceback.print_exc()
        # pass
        # self.tasks.text_update_event = self.update_label2
        # print("Tryiing to start tasks")
        if not self.tasks_process.is_alive():
            # print("Task is not running")
            self.tasks_process = threading.Thread(target=self.runner.upgrade_all_accounts)
            self.tasks_process.daemon = False
            self.tasks_process.start()
            # print("Starting")
            if self.tasks_process.is_alive():
                self.start_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
                self.end_tasks_button.configure(state="normal", fg_color="white")
            else:
                self.end_tasks_button.configure(state="normal", fg_color="white")
                self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
            #         self.start_tasks_button.configure(state="normal", fg_color="white")
            #         self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
            return threading.Thread(target=self.start_thread).start()
        else:
            print("Task is running")
            def _async_raise(tid, exctype):
                tid = ctypes.c_long(tid)
                if not inspect.isclass(exctype):
                    exctype = type(exctype)
                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
                if res == 0:
                    raise ValueError("invalid thread id")
                elif res != 1:
                    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                    raise SystemError("PyThreadState_SetAsyncExc failed")
            _async_raise(self.tasks_process.ident, SystemExit)

    def start_thread(self):
        sleep(0.5)
        return self.root.after(1000, self.process_is_alive)

    def end_tasks(self):
        self.stop = True
        self.update_label2(self.sel, "")
        self.start_tasks_button.configure(state="normal", fg_color="white")
        self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")

    def pause_tasks(self):
        self.pause = not self.pause
        if self.pause:
            self.pr_tasks_button.configure(fg_color="#266496")
        else:
            self.pr_tasks_button.configure(fg_color="white")

    def write(self, text, type="normal", color="red_fg"):
        self.textbox.configure(state="normal")  # make field editable
        self.textbox.insert(tkinter.END, "\n" + text)  # write text to textbox
        self.textbox.see(tkinter.END)  # scroll to end
        self.textbox.configure(state="disabled")  # make field readonly

    def process_is_alive(self):
        if not self.tasks_process.is_alive():
            self.start_tasks_button.configure(state="normal", fg_color="white")
            self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
            return self.update_label2(self.sel, "")
        return self.root.after(1000, self.process_is_alive)

    def update_timers(self):
        for child in self.upper_frame.tree_view.get_children():
            text = self.upper_frame.tree_view.item(child)['values']
            if text[-1].count(":") == 2 and text[-1] != '00:00:00' and len(text[-1]) == 8:
                date_time_obj = datetime.strptime(text[-1], "%H:%M:%S")
                text[-1] = (date_time_obj - timedelta(seconds=1)).strftime("%H:%M:%S")
                self.upper_frame.tree_view.item(child, values=text)

    def update_label2(self, sel, string):
        key = sel
        if self.upper_frame.frames[key].tasks_process.is_alive():
            for child in self.upper_frame.tree_view.get_children():
                if self.upper_frame.tree_view.item(child)['values'][0] == int(key):
                    text = self.upper_frame.tree_view.item(child)['values']
                    text[-1] = string
                    self.upper_frame.tree_view.item(child, values=text)
        else:
            for child in self.upper_frame.tree_view.get_children():
                if self.upper_frame.tree_view.item(child)['values'][0] == int(key) and \
                        self.upper_frame.tree_view.item(child)['values'][-1] != '':
                    text = self.upper_frame.tree_view.item(child)['values']
                    text[-1] = ""
                    self.upper_frame.tree_view.item(child, values=text)




