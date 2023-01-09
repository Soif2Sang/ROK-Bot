import ctypes
import inspect
import json
import threading

import tkinter
from datetime import datetime, timedelta
from time import sleep
from tkinter import Text
from tkinter import Label

import customtkinter
from tktooltip import ToolTip

from UI_Gem import GemInterface
from bot_adb import Adb
from tasks_lib import Tasks


class LowerFrame():
    def __init__(self, upper_frame, sel):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        # print(data[sel[0]]['port'], type(data[sel[0]]['port']))
        self.data = data
        self.upper_frame = upper_frame
        self.root = upper_frame.root
        self.sel = sel[0]
        self.adb = Adb(sel[0])
        self.device = self.adb.connect_to_device()

        # self.bot = BotInterface(sel[0])

        self.tasks = Tasks(self)
        self.tasks.set_sel(sel[0])

        self.tasks_process = threading.Thread(target=self.tasks.routine_scheduled)


        # , fg_color = "#F0F0F0"
        self.bottom_frame = customtkinter.CTkFrame(self.root)
        self.bottom_frame.grid(row=3, column=0, columnspan=2, sticky='')
        # , fg = "#424242"

        # self.write("lorem ipsoum lorem ipsoum lorem ipsoumlorem ipsoumlorem ipsoumlorem ipsoumlorem ipsoum")
        # self.textbox.after(1000, self.write)

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

        self.settings_button = customtkinter.CTkButton(self.bottom_frame, text="Settings ⚙", command=self.enter_settings, corner_radius=4,
                                                       border_color="grey", border_width=1, fg_color="white")
        self.settings_button.grid(row=4, column=0, columnspan=2, sticky='', pady=(10, 0))

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
            # self.textbox.configure(bg = "white")
        # self.upper_frame.tree_view.after(1000, self.update_timers)
        # self.root.after(1000, self.process_is_alive)
        # self.update_timers()
        # self.root.after(1000, self.update_timers)
        if self.tasks_process.is_alive():
            self.start_tasks_button.configure(state="disabled", fg_color="#d1d1d1")
            self.end_tasks_button.configure(state="normal", fg_color="white")
        else:
            # , fg_color = "white"
            self.end_tasks_button.configure(state="normal", fg_color="white")
            # , fg_color = "#d1d1d1"
            self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")

        # def switch_box(Switch, string):
        #     with open('..\\user_settings.json') as config_file:
        #         data = json.load(config_file)
        #     print(f" {Switch.get() = }")
        #     if Switch.get():
        #         data[self.sel][string] = True
        #         Switch.select()
        #     else:
        #         data[self.sel][string] = False
        #         Switch.deselect()
        #     with open('..\\user_settings.json', 'w') as config_file:
        #         config_file.write(json.dumps(data, indent=2))
        #
        # self.reconnect_switch = customtkinter.CTkSwitch(self.bottom_frame, text='Auto reconnect')
        # self.reconnect_switch.configure(command = lambda:switch_box(self.reconnect_switch,"auto_reconnect"))
        # self.reconnect_switch.grid(row=1, column=1, sticky='') #padx = (5,0)
        # if data[self.sel]['auto_reconnect']:
        #     self.reconnect_switch.select()
        # else:
        #     self.reconnect_switch.deselect()
        #
        # self.captcha_switch = customtkinter.CTkSwitch(self.bottom_frame, text='Auto captcha')
        # self.captcha_switch.configure(command = lambda:switch_box(self.captcha_switch,"auto_captcha"))
        # self.captcha_switch.grid(row=2, column=1, sticky='')
        # if data[self.sel]['auto_captcha']:
        #     self.captcha_switch.select()
        # else:
        #     self.captcha_switch.deselect()

        # self.scrollbar = Scrollbar(self.bottom_frame, orient='horizontal')
        # self.scrollbar.grid(row=6, column=0,sticky='swe')
        # self.textbox = Text(self.bottom_frame, wrap=NONE,width = 52,xscrollcommand=self.scrollbar.set)
        # self.textbox.configure(state="normal")
        # self.textbox.grid(row=6, column=0, sticky='')
        # self.textbox.insert(END,self.settings_button)
        # self.scrollbar.config(command=self.textbox.xview)
        # self.textbox.after(1000,self.update_textbox)
        #
        # self.update_textbox()
        # def check_if_process_alive(self):

    #     print(self.tasks_process.is_alive())
    #     if not self.tasks_process.is_alive():
    #         self.start_tasks_button.config(state="normal")
    #         self.end_tasks_button.config(state="disabled")
    #         return self.root.after(1000, self.check_if_process_alive)
    # def update_textbox(self):
    #     if os.path.exists(f".\\{data[self.sel]['name']}_logs.txt"):
    #         self.textbox.delete("1.0", END)
    #         with open(f".\\{data[self.sel]['name']}_logs.txt") as f:
    #             print(self.textbox.get("end-1c linestart", "end"))
    #             for lines in f.readlines():
    #                 self.textbox.insert(END,lines)
    #         self.textbox.see("end")
    #     return self.textbox.after(1000,self.update_textbox)
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

    def enter_settings(self):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
            self.data = data
        # print(data[self.sel])
        root1 = customtkinter.CTkToplevel(self.root)
        root1.title('RoK Bot Settings')
        root1.resizable(False, False)
        root1.iconbitmap('Item_Gem.ico')

        def optionmenu_callback(combobox):
            choice = combobox.get()
            # print("optionmenu dropdown clicked:", choice)
            dict[int(choice[-1])].tkraise()
            if choice[-1] == "1":
                combobox.configure(fg_color="#3b8ed0", selected_color="#266496", selected_hover_color="#266496")
                redo_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
                redo_button.configure(hover_color="#266496", fg_color="#3b8ed0")
                scheduler_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
                scheduler_button.configure(hover_color="#266496", fg_color="#3b8ed0")
                submit_button.configure(hover_color="#266496", fg_color="#3b8ed0")
            if choice[-1] == "2":
                combobox.configure(fg_color="#ba4543", selected_color="#913230", selected_hover_color="#913230")
                redo_switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
                redo_button.configure(hover_color="#913230", fg_color="#ba4543")
                scheduler_switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
                scheduler_button.configure(hover_color="#913230", fg_color="#ba4543")
                submit_button.configure(hover_color="#913230", fg_color="#ba4543")
            if choice[-1] == "3":
                combobox.configure(fg_color="#dec433", selected_color="#baa429", selected_hover_color="#baa429")
                redo_switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")
                redo_button.configure(hover_color="#baa429", fg_color="#dec433")
                scheduler_switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")
                scheduler_button.configure(hover_color="#baa429", fg_color="#dec433")
                submit_button.configure(hover_color="#baa429", fg_color="#dec433")

        combobox = customtkinter.CTkSegmentedButton(master=root1,
                                                    values=["Profile n°1", "Profile n°2", "Profile n°3"],
                                                    fg_color="#3b8ed0", text_color="white", selected_color="#266496", selected_hover_color="#266496")
        # , button_color = "#266496", button_hover_color = "#266496",
        combobox.configure(command=lambda x: optionmenu_callback(combobox))
        combobox.grid(column=0, row=0, columnspan=2, pady=(0, 10))

        label = customtkinter.CTkLabel(root1, text="Custom API Key : ")
        entry = customtkinter.CTkEntry(root1)
        entry.insert(0, data[self.sel]['API_KEY'])
        label.grid(row=1, column=0)
        entry.grid(row=1, column=1, padx=(15, 0))
        # my_scrollbar = ttk.Scrollbar(root1, orient=VERTICAL)
        # my_scrollbar.grid(column=2)
        # root= Frame(root1, yscrollcommand=my_scrollbar.set)
        # my_scrollbar.configure(command=root.yview)
        dict = {}

        def generate_box(switch, string, i):
            # print(i)
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            # print(f" {switch.get() = }")
            # print(data[self.sel]['schedules'][str(i)])
            if switch.get():
                data[self.sel]['schedules'][str(i)][string] = True
                switch.select()
            else:
                data[self.sel]['schedules'][str(i)][string] = False
                switch.deselect()
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))
            # print(data[self.sel]['schedules'][str(i)])
            print(f"{string} = {data[self.sel]['schedules'][str(i)][string]}")

        def create_switch(rootParam, textParam, string, rowParam, i):
            switch = customtkinter.CTkSwitch(rootParam, text=textParam)
            switch.configure(command=lambda: generate_box(switch, string, i))
            if i == 1:
                switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
            if i == 2:
                switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
            if i == 3:
                switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")

            switch.grid(row=rowParam, column=0, sticky='w', padx=(10, 0), pady=1)
            if data[self.sel]['schedules'][str(i)][string] == True:
                switch.select()
            else:
                switch.deselect()

            if textParam == "Switch Characters":
                ToolTip(switch,
                        msg="After the bot did all the tasks on a single account,\nbot will load the nexts characters and do the tasks",
                        delay=0.3)
            if textParam == "Re-do Tasks":
                ToolTip(switch,
                        msg="After the bot did all the tasks, the bot will wait X minutes\n according to your settings, and do the tasks again",
                        delay=0.3)
            if textParam == "Leave game at end":
                ToolTip(switch,
                        msg="After the bot did all the tasks, the bot will leave the game.\nIf 'Re-do Tasks' is enabled,the bot will launch the game after X minutes according to your settings",
                        delay=0.3)

            if textParam == "Slow mode":
                ToolTip(switch,
                        msg="If your computer is slow, you might need to enable it according to your pc specifications",
                        delay=0.3)
            if textParam == "Log back from\nother device":
                ToolTip(switch,
                        msg="If you open the game on your phone and the bot got disconnected\nThe bot will reconnect avec X minutes according to your settings",
                        delay=0.3)
            if textParam == "Multiple Profiles":
                ToolTip(switch,
                        msg="The bot will perform each profile you enabled,\nif disabled :  bot will perform the first enabled profile",
                        delay=0.3)
            return rowParam + 1

        def create_button(rootParam, textParam, commandParam, rowParam, padxp=5):
            button = customtkinter.CTkButton(rootParam, text=textParam, command=commandParam, corner_radius=4, border_color="grey", border_width=1)
            if i == 1:
                button.configure(hover_color="#266496", fg_color="#3b8ed0")
            if i == 2:
                button.configure(hover_color="#913230", fg_color="#ba4543")
            if i == 3:
                button.configure(hover_color="#baa429", fg_color="#dec433")
            button.grid(row=rowParam, column=1, padx=padxp, pady=1)

        def gem_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Gem Settings')
            page.iconbitmap('Item_Gem.ico')
            labelk = customtkinter.CTkLabel(page, text="Your kingdom : ")
            entryk = customtkinter.CTkEntry(page, width=70)
            entryk.insert(0, data[self.sel]['schedules'][str(i)]['kingdom'])
            labelk.grid(row=1, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            entryk.grid(row=1, column=1, columnspan=2)

            labelx = customtkinter.CTkLabel(page, text="Area location x : ")
            entryx = customtkinter.CTkEntry(page, width=70)
            entryx.insert(0, data[self.sel]['schedules'][str(i)]['city_x'])
            labelx.grid(row=2, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            entryx.grid(row=2, column=1, columnspan=2)

            labely = customtkinter.CTkLabel(page, text="Area location y: ")
            entryy = customtkinter.CTkEntry(page, width=70)
            entryy.insert(0, data[self.sel]['schedules'][str(i)]['city_y'])
            labely.grid(row=3, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            entryy.grid(row=3, column=1, columnspan=2)

            labelr = customtkinter.CTkLabel(page, text="Searching Radius(km) : ")
            entryr = customtkinter.CTkEntry(page, width=70)
            entryr.insert(0, data[self.sel]['schedules'][str(i)]['radius'])
            labelr.grid(row=4, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            entryr.grid(row=4, column=1, columnspan=2)

            labeld1 = customtkinter.CTkLabel(page, text="Mining duration(mins): ")
            labeld1.grid(row=5, column=0, columnspan=1, pady=2, sticky='e')
            labeld2 = tkinter.Label(page, text="~")
            labeld2.grid(row=5, column=2, columnspan=1, pady=2)

            entryd1 = customtkinter.CTkEntry(page, width=45)
            entryd1.insert(0, data[self.sel]['schedules'][str(i)]['gather_gem_duration1'])
            entryd1.grid(row=5, column=1)

            entryd2 = customtkinter.CTkEntry(page, width=45)
            entryd2.insert(0, data[self.sel]['schedules'][str(i)]['gather_gem_duration2'])
            entryd2.grid(row=5, column=3)

            labeld3 = customtkinter.CTkLabel(page, text="Look for available\n troops each X (secs): ")
            labeld3.grid(row=6, column=0, columnspan=1, pady=2, sticky='e')
            ToolTip(labeld3,
                    msg="This settings is to configure how frequently the bot will check for an available troop\n*WARNING* Don't lower too much !",
                    delay=0.3)

            labeld4 = tkinter.Label(page, text="~")
            labeld4.grid(row=6, column=2, columnspan=1, pady=2)

            entryd3 = customtkinter.CTkEntry(page, width=45)
            entryd3.insert(0, data[self.sel]['schedules'][str(i)]['gem_check1'])
            entryd3.grid(row=6, column=1)

            entryd4 = customtkinter.CTkEntry(page, width=45)
            entryd4.insert(0, data[self.sel]['schedules'][str(i)]['gem_check2'])
            entryd4.grid(row=6, column=3)

            def box_restart():
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f" {restart_button.get() = }")
                if restart_button.get():
                    data[self.sel]['schedules'][str(i)]['restart_game'] = True
                    restart_button.select()
                else:
                    data[self.sel]['schedules'][str(i)]['restart_game'] = False
                    restart_button.deselect()
                with open('user_settings.json', 'w') as config_file:
                    config_file.write(json.dumps(data, indent=2))
                print(f"{data[self.sel]['schedules'][str(i)]['restart_game'] = }")

            restart_button = customtkinter.CTkSwitch(page, text='Sometimes restart game',
                                                     command=box_restart)
            restart_button.grid(row=60, column=0, columnspan=4, pady=(5, 5))
            if data[self.sel]['schedules'][str(i)]['restart_game']:
                # print(f" {restart_button.get() = }")
                restart_button.select()
                # print(f" {restart_button.get() = }")
            else:
                restart_button.deselect()

            def box_experimental():
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f" {restart_button.get() = }")
                if experimental_button.get():
                    data[self.sel]['schedules'][str(i)]['gem_experimental'] = True
                    experimental_button.select()
                else:
                    data[self.sel]['schedules'][str(i)]['gem_experimental'] = False
                    experimental_button.deselect()
                with open('user_settings.json', 'w') as config_file:
                    config_file.write(json.dumps(data, indent=2))
                print(f"{data[self.sel]['schedules'][str(i)]['gem_experimental'] = }")

            experimental_button = customtkinter.CTkSwitch(page, text='Enable experimental mode',
                                                          command=box_experimental)
            experimental_button.grid(row=80, column=0, columnspan=4, pady=(5, 5))
            if data[self.sel]['schedules'][str(i)]['gem_experimental']:
                # print(f" {restart_button.get() = }")
                experimental_button.select()
                # print(f" {restart_button.get() = }")
            else:
                experimental_button.deselect()

            def submit():
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                data[self.sel]['schedules'][str(i)]['kingdom'] = entryk.get()
                data[self.sel]['schedules'][str(i)]['city_y'] = int(entryy.get())
                data[self.sel]['schedules'][str(i)]['city_x'] = int(entryx.get())
                data[self.sel]['schedules'][str(i)]['radius'] = int(entryr.get())
                data[self.sel]['schedules'][str(i)]['gather_gem_duration1'] = int(entryd1.get())
                data[self.sel]['schedules'][str(i)]['gather_gem_duration2'] = int(entryd2.get())
                data[self.sel]['schedules'][str(i)]['gem_check1'] = int(entryd3.get())
                data[self.sel]['schedules'][str(i)]['gem_check2'] = int(entryd4.get())
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=81, column=0, columnspan=4, pady=(5, 5))

        def rss_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            def custom_preset():
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f" {restart_button.get() = }")
                if custom_preset_button.get():
                    data[self.sel]['schedules'][str(i)]['rss_custom_preset'] = True
                    custom_preset_button.select()
                else:
                    data[self.sel]['schedules'][str(i)]['rss_custom_preset'] = False
                    custom_preset_button.deselect()
                with open('user_settings.json', 'w') as config_file:
                    config_file.write(json.dumps(data, indent=2))
                print(f"{data[self.sel]['schedules'][str(i)]['rss_custom_preset'] = }")

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Rss Settings')
            page.iconbitmap('Item_Gem.ico')

            label1 = customtkinter.CTkLabel(page, text="1st choice :")
            label1.grid(column=0, row=0, **paddings, sticky='e')

            label2 = customtkinter.CTkLabel(page, text="2nd choice :")
            label2.grid(column=0, row=1, **paddings, sticky='e')

            label3 = customtkinter.CTkLabel(page, text="3rd choice :")
            label3.grid(column=0, row=2, **paddings, sticky='e')

            label4 = customtkinter.CTkLabel(page, text="4th choice :")
            label4.grid(column=0, row=3, **paddings, sticky='e')

            label5 = customtkinter.CTkLabel(page, text="5th choice :")
            label5.grid(column=0, row=4, **paddings, sticky='e')

            label6 = customtkinter.CTkLabel(page, text="6th choice :")
            label6.grid(column=0, row=5, **paddings, sticky='e')

            label7 = customtkinter.CTkLabel(page, text="7th choice :")
            label7.grid(column=0, row=6, **paddings, sticky='e')

            custom_preset_button = customtkinter.CTkSwitch(page, text='Use Yellow Preset',
                                                           command=custom_preset)
            custom_preset_button.grid(row=80, column=0, columnspan=4, pady=(5, 5))

            if data[self.sel]['schedules'][str(i)]['rss_custom_preset']:
                # print(f" {restart_button.get() = }")
                custom_preset_button.select()
                # print(f" {restart_button.get() = }")
            else:
                custom_preset_button.deselect()

            resources = ['food node', 'wood node', 'stone node', 'gold node']

            # set up variable
            # option1_var = StringVar(page)
            # option1_var.set(data[self.sel]["First"])
            #
            # # set up variable
            # option2_var = StringVar(page)
            # option2_var.set(data[self.sel]["Second"])
            #
            # # set up variable
            # option3_var = StringVar(page)
            # option3_var.set(data[self.sel]["Third"])
            #
            # # set up variable
            # option4_var = StringVar(page)
            # option4_var.set(data[self.sel]["Fourth"])

            def first_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["First"] = option1.get().split(" node")[0]

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def second_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["Second"] = option2.get().split(" node")[0]

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def third_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["Third"] = option3.get().split(" node")[0]

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def fourth_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
                data[self.sel]['schedules'][str(i)]["Fourth"] = option4.get().split(" node")[0]
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def fifth_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
                data[self.sel]['schedules'][str(i)]["Fifth"] = option4.get().split(" node")[0]
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def sixth_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
                data[self.sel]['schedules'][str(i)]["Sixth"] = option4.get().split(" node")[0]
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def seventh_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
                data[self.sel]['schedules'][str(i)]["Seventh"] = option4.get().split(" node")[0]
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(
                    json.dumps(data, indent=2))

            option1_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["First"]) + " node")
            option2_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Second"]) + " node")
            option3_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Third"]) + " node")
            option4_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Fourth"]) + " node")
            option5_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Fifth"]) + " node")
            option6_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Sixth"]) + " node")
            option7_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["Seventh"]) + " node")

            option1 = customtkinter.CTkOptionMenu(master=page, variable=option1_var, values=resources,
                                                  command=first_choice, fg_color="white", text_color="black")
            option1.grid(column=1, row=0, **paddings, sticky='e')
            option2 = customtkinter.CTkOptionMenu(master=page, variable=option2_var, values=resources,
                                                  command=second_choice, fg_color="white", text_color="black")
            option2.grid(column=1, row=1, **paddings, sticky='e')
            option3 = customtkinter.CTkOptionMenu(master=page, variable=option3_var, values=resources,
                                                  command=third_choice, fg_color="white", text_color="black")
            option3.grid(column=1, row=2, **paddings, sticky='e')
            option4 = customtkinter.CTkOptionMenu(master=page, variable=option4_var, values=resources,
                                                  command=fourth_choice, fg_color="white", text_color="black")
            option4.grid(column=1, row=3, **paddings, sticky='e')

            option5 = customtkinter.CTkOptionMenu(master=page, variable=option5_var, values=resources,
                                                  command=fifth_choice, fg_color="white", text_color="black")
            option5.grid(column=1, row=4, **paddings, sticky='e')

            option6 = customtkinter.CTkOptionMenu(master=page, variable=option6_var, values=resources,
                                                  command=sixth_choice, fg_color="white", text_color="black")
            option6.grid(column=1, row=5, **paddings, sticky='e')

            option7 = customtkinter.CTkOptionMenu(master=page, variable=option7_var, values=resources,
                                                  command=seventh_choice, fg_color="white", text_color="black")
            option7.grid(column=1, row=6, **paddings, sticky='e')

            option_var_level1 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["First_level"]))
            option_var_level2 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Second_level"]))
            option_var_level3 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Third_level"]))
            option_var_level4 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Fourth_level"]))
            option_var_level5 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Fifth_level"]))
            option_var_level6 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Sixth_level"]))
            option_var_level7 = customtkinter.StringVar(value="level " + str(data[self.sel]['schedules'][str(i)]["Seventh_level"]))

            def first_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["First_level"] = int(option_level1.get()[-1])

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def second_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["Second_level"] = int(option_level2.get()[-1])

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def third_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["Third_level"] = int(option_level3.get()[-1])

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def fourth_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                print(f"{data[self.sel]['schedules'][str(i)]['Fourth'] = } {option_level4.get() = }")

                data[self.sel]['schedules'][str(i)]["Fourth_level"] = int(option_level4.get()[-1])

                print(f"{data[self.sel]['schedules'][str(i)]['Fourth'] = } {option_level4.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def fifth_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                print(f"{data[self.sel]['schedules'][str(i)]['Fifth'] = } {option_level5.get() = }")

                data[self.sel]['schedules'][str(i)]["Fifth_level"] = int(option_level5.get()[-1])

                print(f"{data[self.sel]['schedules'][str(i)]['Fifth'] = } {option_level5.get() = }")
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def sixth_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                print(f"{data[self.sel]['schedules'][str(i)]['Sixth'] = } {option_level6.get() = }")

                data[self.sel]['schedules'][str(i)]["Sixth_level"] = int(option_level6.get()[-1])

                print(f"{data[self.sel]['schedules'][str(i)]['Sixth'] = } {option_level6.get() = }")
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def seventh_choice_level(choice):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                print(f"{data[self.sel]['schedules'][str(i)]['Seventh'] = } {option_level7.get() = }")

                data[self.sel]['schedules'][str(i)]["Seventh_level"] = int(option_level7.get()[-1])

                print(f"{data[self.sel]['schedules'][str(i)]['Seventh'] = } {option_level7.get() = }")
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            levels = ["level " + str(i) for i in range(1, 10)]
            option_level1 = customtkinter.CTkOptionMenu(master=page, variable=option_var_level1, values=levels,
                                                        command=first_choice_level, fg_color="white", text_color="black")
            option_level1.grid(column=2, row=0, **paddings, sticky='e')
            option_level2 = customtkinter.CTkOptionMenu(page, variable=option_var_level2, values=levels,
                                                        command=second_choice_level, fg_color="white", text_color="black")
            option_level2.grid(column=2, row=1, **paddings, sticky='e')
            option_level3 = customtkinter.CTkOptionMenu(page, variable=option_var_level3, values=levels,
                                                        command=third_choice_level, fg_color="white", text_color="black")
            option_level3.grid(column=2, row=2, **paddings, sticky='e')
            option_level4 = customtkinter.CTkOptionMenu(page, variable=option_var_level4, values=levels,
                                                        command=fourth_choice_level, fg_color="white", text_color="black")
            option_level4.grid(column=2, row=3, **paddings, sticky='e')

            option_level5 = customtkinter.CTkOptionMenu(page, variable=option_var_level5, values=levels,
                                                        command=fifth_choice_level, fg_color="white", text_color="black")
            option_level5.grid(column=2, row=4, **paddings, sticky='e')

            option_level6 = customtkinter.CTkOptionMenu(page, variable=option_var_level6, values=levels,
                                                        command=sixth_choice_level, fg_color="white", text_color="black")
            option_level6.grid(column=2, row=5, **paddings, sticky='e')

            option_level7 = customtkinter.CTkOptionMenu(page, variable=option_var_level7, values=levels,
                                                        command=seventh_choice_level, fg_color="white", text_color="black")
            option_level7.grid(column=2, row=6, **paddings, sticky='e')

        def fog_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Fog Settings')
            page.iconbitmap('Item_Gem.ico')

            labelx = customtkinter.CTkLabel(page, text="Scout building placement x : ")
            entryx = customtkinter.CTkEntry(page, width=70)
            entryx.insert(0, data[self.sel]['schedules'][str(i)]['scout_building_x'])
            labelx.grid(row=2, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            entryx.grid(row=2, column=1, columnspan=2)

            labely = customtkinter.CTkLabel(page, text="Scout building placement y : ")
            entryy = customtkinter.CTkEntry(page, width=70)
            entryy.insert(0, data[self.sel]['schedules'][str(i)]['scout_building_y'])
            labely.grid(row=3, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            entryy.grid(row=3, column=1, columnspan=2)

            labeld1 = customtkinter.CTkLabel(page, text="Scouting duration(mins): ")
            labeld1.grid(row=5, column=0, columnspan=1, pady=2, sticky='e')
            labeld2 = Label(page, text="~")
            labeld2.grid(row=5, column=2, columnspan=1, pady=2)

            entryd1 = customtkinter.CTkEntry(page, width=45)
            entryd1.insert(0, data[self.sel]['schedules'][str(i)]['scout_duration1'])
            entryd1.grid(row=5, column=1)

            entryd2 = customtkinter.CTkEntry(page, width=45)
            entryd2.insert(0, data[self.sel]['schedules'][str(i)]['scout_duration2'])
            entryd2.grid(row=5, column=3)

            def submit():
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                data[self.sel]['schedules'][str(i)]['scout_building_x'] = int(entryx.get())
                data[self.sel]['schedules'][str(i)]['scout_building_y'] = int(entryy.get())
                data[self.sel]['schedules'][str(i)]['scout_duration1'] = int(entryd1.get())
                data[self.sel]['schedules'][str(i)]['scout_duration2'] = int(entryd2.get())

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        def rally_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Start Rally')
            page.iconbitmap('Item_Gem.ico')

            def first_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)]["rally_time"] = option1.get().split(" minutes")[0]

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            def second_choice(*args):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
                data[self.sel]['schedules'][str(i)]["rally_type"] = option2.get()
                # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            labelx = customtkinter.CTkLabel(page, text="Mobolisation time : ")
            labelx.grid(row=0, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))

            times = ['5 minutes', '10 minutes', '30 minutes']
            time_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["rally_time"]) + " minutes")
            option1 = customtkinter.CTkOptionMenu(master=page, variable=time_var, values=times,
                                                  command=first_choice,
                                                  fg_color="white", text_color="black")
            option1.grid(column=1, row=0, **paddings, sticky='e')

            labelx = customtkinter.CTkLabel(page, text="Rally type : ")
            labelx.grid(row=1, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            types = ['cav', 'inf', 'archers']
            type_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["rally_type"]))
            option2 = customtkinter.CTkOptionMenu(master=page, variable=type_var, values=types,
                                                  command=second_choice, fg_color="white", text_color="black")
            option2.grid(column=1, row=1, **paddings, sticky='e')

            # def checkbox_event(*args):
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
            #     data[self.sel]["mauraudeurs_forts"] = mauraudeurs_forts_box.get()
            #     # print(f"{data[self.sel]['Fourth'] = } {option4_var.get() = }")
            #     print(data[self.sel]['mauraudeurs_forts'])
            #     with open('..\\user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
            #
            # check_var = tkinter.BooleanVar(data[self.sel]["mauraudeurs_forts"])
            # mauraudeurs_forts_box = customtkinter.CTkCheckBox(master=page, text="Mauraudeurs Forts : ", command=checkbox_event,
            #                      variable=check_var, onvalue=True, offvalue=False)
            # mauraudeurs_forts_box.grid(row=2,column=0,columnspan=1,pady=2, sticky='w', padx=(5, 0))

            # if data[self.sel]["mauraudeurs_forts"]:
            #     mauraudeurs_forts_box.select()
            # else:
            #     mauraudeurs_forts_box.deselect()

            create_switch(page, "Mauraudeurs Forts", "mauraudeurs_forts", 5, i)

            def submit():
                with open('user_settings.json') as config_file: data = json.load(config_file)
                # data[self.sel]['time_to_wait_loop1'] = int(option1.get())
                # data[self.sel]['time_to_wait_loop2'] = int(option1.get())
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        def healing_config(root, i):
            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Heal config')
            page.iconbitmap('Item_Gem.ico')

            labelx = customtkinter.CTkLabel(page, text="Healing building placement x : ")
            entryx = customtkinter.CTkEntry(page, width=70)
            entryx.insert(0, data[self.sel]['schedules'][str(i)]['healing_building_x'])
            labelx.grid(row=2, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            entryx.grid(row=2, column=1, columnspan=2)

            labely = customtkinter.CTkLabel(page, text="Healing building placement y : ")
            entryy = customtkinter.CTkEntry(page, width=70)
            entryy.insert(0, data[self.sel]['schedules'][str(i)]['healing_building_y'])
            labely.grid(row=3, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            entryy.grid(row=3, column=1, columnspan=2)

            labelh = customtkinter.CTkLabel(page, text="Number of troops to heal per batch: ")
            entryh = customtkinter.CTkEntry(page, width=70)
            entryh.insert(0, data[self.sel]['schedules'][str(i)]['healing_count'])
            labelh.grid(row=4, column=0, columnspan=1, pady=2, sticky='w', padx=(5, 0))
            entryh.grid(row=4, column=1, columnspan=2)

            def submit():
                with open('user_settings.json') as config_file: data = json.load(config_file)
                data[self.sel]['schedules'][str(i)]['healing_building_x'] = int(entryx.get())
                data[self.sel]['schedules'][str(i)]['healing_building_y'] = int(entryy.get())
                data[self.sel]['schedules'][str(i)]['healing_count'] = int(entryh.get())
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        def material_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Materials Settings')
            page.iconbitmap('Item_Gem.ico')
            label1 = Label(page, text="First choice :")
            label1.grid(column=0, row=0, **paddings, sticky='e')

            label2 = Label(page, text="Second choice :")
            label2.grid(column=0, row=1, **paddings, sticky='e')

            label3 = Label(page, text="Third choice :")
            label3.grid(column=0, row=2, **paddings, sticky='e')

            label4 = Label(page, text="Fourth choice :")
            label4.grid(column=0, row=3, **paddings, sticky='e')

            label5 = Label(page, text="Fifth choice :")
            label5.grid(column=0, row=4, **paddings, sticky='e')

            materials = ['leather', 'stone', 'ebony', 'bones']

            # set up variable
            # option1_var = StringVar(page)
            # option1_var.set(data[self.sel]["First"])
            #
            # # set up variable
            # option2_var = StringVar(page)
            # option2_var.set(data[self.sel]["Second"])
            #
            # # set up variable
            # option3_var = StringVar(page)
            # option3_var.set(data[self.sel]["Third"])
            #
            # # set up variable
            # option4_var = StringVar(page)
            # option4_var.set(data[self.sel]["Fourth"])

            def mat_choice(y, option):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)

                data[self.sel]['schedules'][str(i)][f"material_choice_{y}"] = option.get()

                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

            option1_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["material_choice_1"]))
            option2_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["material_choice_2"]))
            option3_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["material_choice_3"]))
            option4_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["material_choice_4"]))
            option5_var = customtkinter.StringVar(value=str(data[self.sel]['schedules'][str(i)]["material_choice_5"]))

            option1 = customtkinter.CTkOptionMenu(master=page, variable=option1_var, values=materials,
                                                  fg_color="white", text_color="black")
            option1.configure(command=lambda x: mat_choice(1, option1))
            option1.grid(column=1, row=0, **paddings, sticky='e')

            option2 = customtkinter.CTkOptionMenu(master=page, variable=option2_var, values=materials,
                                                  fg_color="white", text_color="black")
            option2.configure(command=lambda x: mat_choice(2, option2))
            option2.grid(column=1, row=1, **paddings, sticky='e')

            option3 = customtkinter.CTkOptionMenu(master=page, variable=option3_var, values=materials,
                                                  fg_color="white", text_color="black")
            option3.configure(command=lambda x: mat_choice(3, option3))
            option3.grid(column=1, row=2, **paddings, sticky='e')

            option4 = customtkinter.CTkOptionMenu(master=page, variable=option4_var, values=materials,
                                                  fg_color="white", text_color="black")
            option4.configure(command=lambda x: mat_choice(4, option4))
            option4.grid(column=1, row=3, **paddings, sticky='e')

            option5 = customtkinter.CTkOptionMenu(master=page, variable=option5_var, values=materials,
                                                  fg_color="white", text_color="black")
            option5.configure(command=lambda x: mat_choice(5, option5))
            option5.grid(column=1, row=4, **paddings, sticky='e')

        def switch_char_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Switch Characters Settings')
            page.iconbitmap('Item_Gem.ico')

            create_switch(page, "Leave game after switching between\ncharacters, can prevent freeze",
                          "leave_game_switch_character", 1, i)

            def submit():
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        def log_back_config(root, i):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Log-back Settings')
            page.iconbitmap('Item_Gem.ico')

            labeld1 = customtkinter.CTkLabel(page,
                                             text="Time to wait before the bot log\nback from your connection(mins): ")
            labeld1.grid(row=5, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            labeld2 = Label(page, text="~")
            labeld2.grid(row=5, column=2, columnspan=1, pady=2)

            entryd1 = customtkinter.CTkEntry(page, width=45)
            entryd1.insert(0, data[self.sel]['schedules'][str(i)]['log_back1'])
            entryd1.grid(row=5, column=1, pady=(5, 0))

            entryd2 = customtkinter.CTkEntry(page, width=45)
            entryd2.insert(0, data[self.sel]['schedules'][str(i)]['log_back2'])
            entryd2.grid(row=5, column=3, pady=(5, 0), padx=(0, 5))

            def submit():
                with open('user_settings.json') as config_file: data = json.load(config_file)
                data[self.sel]['schedules'][str(i)]['log_back1'] = int(entryd1.get())
                data[self.sel]['schedules'][str(i)]['log_back2'] = int(entryd2.get())
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4
                                             , border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        class Profile():
            def __init__(self, sel, racine, profileNb):
                self.sel = sel
                self.racine = racine
                self.profileNb = profileNb
                self.root = customtkinter.CTkFrame(racine)
                root = self.root
                i = self.profileNb
                nb_switch = 0
                create_button(root, "⚙", lambda: GemInterface(root, str(self.sel), str(i)), nb_switch)
                nb_switch = create_switch(root, "Gather gems", "gather_gem", nb_switch, i)

                create_button(root, "⚙", lambda: rss_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Gather Rss", "gather_rss", nb_switch, i)

                create_button(root, "⚙", lambda: fog_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Clear fog", "scout_fog", nb_switch, i)

                nb_switch = create_switch(root, "Use enhanced buff", "use_enhanced_buff", nb_switch, i)
                nb_switch = create_switch(root, "Buy merchant", "buy_merchant", nb_switch, i)
                nb_switch = create_switch(root, "Collect city rss", "collect_ressource", nb_switch, i)

                paddings = {'padx': 5, 'pady': 1}

                levels = ["level " + str(i) for i in range(1, 56)]
                optionmenu_var = customtkinter.StringVar(value=f"level {data[self.sel]['schedules'][str(i)]['barbarians_level']}")

                def set_barbarians_level(choice, i):
                    with open('user_settings.json') as config_file:
                        data = json.load(config_file)
                    # print(f'{int(option_barbarians.get().split("level ")[1]) = }')
                    data[self.sel]['schedules'][str(i)]["barbarians_level"] = int(option_barbarians.get().split("level ")[1])

                    with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

                option_barbarians = customtkinter.CTkOptionMenu(master=root, variable=optionmenu_var, values=levels, fg_color='white')
                option_barbarians.configure(command=lambda event: set_barbarians_level(option_barbarians, i), )
                option_barbarians.grid(row=nb_switch, column=1, **paddings, sticky='')
                nb_switch = create_switch(root, "Kill barbs with AP", "defeat_barbarians", nb_switch, i)

                nb_switch = create_switch(root, "Alliance donation", "check_donation", nb_switch, i)

                nb_switch = create_switch(root, "Claim VIP Chests", "claim_daily_vip", nb_switch, i)

                nb_switch = create_switch(root, "Claim Daily Chests", "claim_daily_chest", nb_switch, i)

                nb_switch = create_switch(root, "Claim Campaign Rewards", "claim_campaign", nb_switch, i)

                create_button(root, "⚙", lambda: rally_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Launch Rally", "start_fort", nb_switch, i)

                create_button(root, "⚙", lambda: healing_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Healing", "heal_troop", nb_switch, i)
                create_button(root, "⚙", lambda: material_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Material Production", "material_production", nb_switch, i)

                label_task = customtkinter.CTkLabel(root, text="━━━━━━━━━━━━━━━━━━━━")
                label_task.grid(row=nb_switch, columnspan=2)
                nb_switch = nb_switch + 1

                nb_switch = create_switch(root, "Auto reconnection", "auto_reconnect", nb_switch, i)
                nb_switch = create_switch(root, "Resolve captchas", "auto_captcha", nb_switch, i)

                create_button(root, "⚙", lambda: switch_char_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Switch Characters", "switch_character", nb_switch, i)

                levels_slow_menu = ["1.0x", "1.25x", "1.5x", "1.75x", "2.0x", "2.25x", "2.5x", "2.75x", "3.0x"]
                slow_menu_var = customtkinter.StringVar(
                    value=str(data[self.sel]['schedules'][str(i)]["sleep_multiplicator"]) + "x")
                #
                # slow_menu_var = StringVar(
                #     value=str(data[self.sel]['schedules'][str(i)]["sleep_multiplicator"]) + "x")

                # option_barbarians = ttk.OptionMenu(root, option_level, data[self.sel]["barbarians_level"], *levels,
                #                                    command=set_barbarians_level)
                option_slow = customtkinter.CTkOptionMenu(master=root, variable=slow_menu_var, values=levels_slow_menu, fg_color="white",
                                                          text_color="black")
                # option_slow = ttk.OptionMenu(
                #     root,
                #     slow_menu_var,
                #     levels_slow_menu[0],
                #     *levels_slow_menu)
                # print(option_slow.keys())
                # print(option_slow.cget('textvariable'))
                # print(option_slow.getvar(option_slow.cget('textvariable')))
                if i == 1:
                    # pass
                    option_slow.configure(button_color="#3b8ed0", button_hover_color="#266496")
                if i == 2:
                    # pass
                    option_slow.configure(button_color="#ba4543", button_hover_color="#913230")
                if i == 3:
                    # pass
                    option_slow.configure(button_color="#dec433", button_hover_color="#baa429")

                # print(slow_menu_var.get(),i)
                # option_slow.
                def set_sleep_multiplicator(choice, i):
                    # print(choice, i)
                    with open('user_settings.json') as config_file:
                        data = json.load(config_file)

                    data[self.sel]['schedules'][str(i)]["sleep_multiplicator"] = float(choice.get()[:-1])
                    # print(choice.cget('textvariable')[:-1], type(choice.cget('textvariable')[:-1]))
                    # data[self.sel]['schedules'][str(i)]["sleep_multiplicator"] = float(option_slow.getvar(option_slow.cget('textvariable'))[:-1])
                    with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))

                # set_sleep_multiplicator(option_slow, i)
                option_slow.configure(command=lambda event: set_sleep_multiplicator(option_slow, i), )
                option_slow.grid(row=nb_switch, column=1, **paddings, sticky='')

                nb_switch = create_switch(root, "Slow mode", "slow_mode", nb_switch, i)

                create_button(root, "⚙", lambda: log_back_config(root, i), nb_switch)

                nb_switch = create_switch(root, "Log back from\nother device", "auto_log_back", nb_switch, i)

                self.root.grid(row=2, column=0, columnspan=2)

        for i in range(1, 4):
            dict[i] = Profile(self.sel, root1, i).root

            # def box_alliance_donation():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {donation_button.get() = }")
            #     if donation_button.get():
            #         data[self.sel]['check_donation'] = True
            #         donation_button.select()
            #     else:
            #         data[self.sel]['check_donation'] = False
            #         donation_button.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['check_donation'])
            #
            # def box_enhanced_buff():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {gather_rss_box.get() = }")
            #     if enhanced_buff_box.get():
            #         data[self.sel]['use_enhanced_buff'] = True
            #         enhanced_buff_box.select()
            #     else:
            #         data[self.sel]['use_enhanced_buff'] = False
            #         enhanced_buff_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['use_enhanced_buff'])
            #
            # def box_gather_rss():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {gather_rss_box.get() = }")
            #     if gather_rss_box.get():
            #         data[self.sel]['gather_rss'] = True
            #         gather_rss_box.select()
            #     else:
            #         data[self.sel]['gather_rss'] = False
            #         gather_rss_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['gather_rss'])
            #
            # def box_buy_merchant():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {buy_merchant_box.get() = }")
            #     if buy_merchant_box.get():
            #         data[self.sel]['buy_merchant'] = True
            #         buy_merchant_box.select()
            #     else:
            #         data[self.sel]['buy_merchant'] = False
            #         buy_merchant_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['buy_merchant'])
            #
            # def box_collect_ressource():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #
            #     print(f" {collect_ressourcet_box.get() = }")
            #     if collect_ressourcet_box.get():
            #         data[self.sel]['collect_ressource'] = True
            #         collect_ressourcet_box.select()
            #     else:
            #         data[self.sel]['collect_ressource'] = False
            #         collect_ressourcet_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['collect_ressource'])
            #
            # def box_defeat_barbarians():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {defeat_barbarians_box.get() = }")
            #     if defeat_barbarians_box.get():
            #         data[self.sel]['defeat_barbarians'] = True
            #         defeat_barbarians_box.select()
            #     else:
            #         data[self.sel]['defeat_barbarians'] = False
            #         defeat_barbarians_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['defeat_barbarians'])
            #
            # def box_gather_gem():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {gather_gem_box.get() = }")
            #     if gather_gem_box.get():
            #         data[self.sel]['gather_gem'] = True
            #         gather_gem_box.select()
            #     else:
            #         data[self.sel]['gather_gem'] = False
            #         gather_gem_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['gather_gem'])
            #
            # def box_switch_character():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {switch_character_box.get() = }")
            #     if switch_character_box.get():
            #         data[self.sel]['switch_character'] = True
            #         switch_character_box.select()
            #     else:
            #         data[self.sel]['switch_character'] = False
            #         switch_character_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(data[self.sel]['switch_character'])
            #
            # def box_loop_tasks():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {loop_tasks_box.get() = }")
            #     if loop_tasks_box.get() == 1:
            #         data[self.sel]['loop_task'] = True
            #         loop_tasks_box.select()
            #     else:
            #         data[self.sel]['loop_task'] = False
            #         loop_tasks_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(f"{data[self.sel]['loop_task'] = }")
            #
            # def box_leave_task():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {leave_task_box.get() = }")
            #     if leave_task_box.get():
            #         data[self.sel]['leave_game_loop'] = True
            #         leave_task_box.select()
            #     else:
            #         data[self.sel]['leave_game_loop'] = False
            #         leave_task_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(f"{data[self.sel]['leave_game_loop'] = }")
            #
            # def box_fog():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {fog_box.get() = }")
            #     if fog_box.get():
            #         data[self.sel]['scout_fog'] = True
            #         fog_box.select()
            #     else:
            #         data[self.sel]['scout_fog'] = False
            #         fog_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(f"{data[self.sel]['scout_fog'] = }")
            #
            # def box_slow_mode():
            #     with open('..\\user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     print(f" {slow_mode_box.get() = }")
            #     if slow_mode_box.get():
            #         data[self.sel]['slow_mode'] = True
            #         slow_mode_box.select()
            #     else:
            #         data[self.sel]['slow_mode'] = False
            #         slow_mode_box.deselect()
            #     with open('..\\user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(f"{data[self.sel]['slow_mode'] = }")

        def generate_box1(switch, string):
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            print(f" {switch.get() = }")
            if switch.get():
                data[self.sel]['schedules'][str(i)][string] = True
                switch.select()
            else:
                data[self.sel]['schedules'][str(i)][string] = False
                switch.deselect()
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))
            print(f"{string} = {data[self.sel]['schedules'][str(i)][string]}")

        def generate_box2(switch, string):
            # print(i)
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            # print(f" {switch.get() = }")
            if switch.get():
                data[self.sel][string] = True
                switch.select()
            else:
                data[self.sel][string] = False
                switch.deselect()
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))
            # print(data[self.sel])
            # print(f"{string} = {data[self.sel][string]}")

        def create_switch1(rootParam, textParam, string, rowParam):
            switch = customtkinter.CTkSwitch(rootParam, text=textParam)
            switch.configure(command=lambda: generate_box2(switch, string, ))
            switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")

            switch.grid(row=rowParam, column=0, sticky='w', padx=(10, 0), pady=1)
            if data[self.sel][string] == True:
                switch.select()
            else:
                switch.deselect()

            return switch

        def create_button1(rootParam, textParam, commandParam, rowParam, padxp=(13, 0)):
            button = customtkinter.CTkButton(rootParam, text=textParam, command=commandParam, corner_radius=4
                                             , border_color="grey", border_width=1)

            button.configure(hover_color="#266496")

            button.grid(row=rowParam, column=1, padx=padxp, pady=1)
            return button

        def redo_config(root):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Re-do Settings')
            page.iconbitmap('Item_Gem.ico')
            labeld1 = customtkinter.CTkLabel(page, text="*DO NOT USE CLOSE VARIABLES*", text_color="red",
                                             font=customtkinter.CTkFont(family='Helvetica bold', size=15))
            labeld1.grid(row=0, column=0, columnspan=4, pady=2, sticky='ew')

            labeld2 = customtkinter.CTkLabel(page, text="~")
            labeld2.grid(row=1, column=2, columnspan=1, pady=2)

            labeld1 = customtkinter.CTkLabel(page, text="Time to wait before\nthe bot re-do the tasks(mins): ")
            labeld1.grid(row=1, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            labeld2 = Label(page, text="~")
            labeld2.grid(row=1, column=2, columnspan=1, pady=2)

            entryd1 = customtkinter.CTkEntry(page, width=45)
            entryd1.insert(0, data[self.sel]['time_to_wait_loop1'])
            entryd1.grid(row=1, column=1, pady=(5, 0))

            entryd2 = customtkinter.CTkEntry(page, width=45)
            entryd2.insert(0, data[self.sel]['time_to_wait_loop2'])
            entryd2.grid(row=1, column=3, pady=(5, 0), padx=(0, 5))

            create_switch1(page, "Leave game at end", "leave_game_loop", 2)

            def submit():
                with open('user_settings.json') as config_file: data = json.load(config_file)
                data[self.sel]['time_to_wait_loop1'] = int(entryd1.get())
                data[self.sel]['time_to_wait_loop2'] = int(entryd2.get())
                with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", text_color=
                                             "black", border_width=1)
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5))

        redo_button = create_button1(root1, "⚙", lambda: redo_config(root1), 4)

        redo_switch = create_switch1(root1, "Re-do Tasks", "loop_task", 4)

        def scheduler_config(root):

            with open('user_settings.json') as config_file:
                data = json.load(config_file)

            paddings = {'padx': 5, 'pady': 5}
            page = customtkinter.CTkToplevel(root)
            page.resizable(False, False)
            page.title('RoK Bot Re-do Settings')
            page.iconbitmap('Item_Gem.ico')

            labeld1 = customtkinter.CTkLabel(page, text="Profiles : ")
            labeld1.grid(row=0, column=0, columnspan=2, padx=(20, 0))

            def generate_box1(switch, string, i):
                with open('user_settings.json') as config_file:
                    data = json.load(config_file)
                print(f" {switch.get() = }")
                if switch.get():
                    data[self.sel]['schedules'][str(i)][string] = True
                    switch.select()
                else:
                    data[self.sel]['schedules'][str(i)][string] = False
                    switch.deselect()
                with open('user_settings.json', 'w') as config_file:
                    config_file.write(json.dumps(data, indent=2))
                print(f"{string} = {data[self.sel]['schedules'][str(i)][string]}")

            def create_switch_enabled(rootParam, textParam, string, rowParam, profileNb):
                switch = customtkinter.CTkSwitch(rootParam, text=textParam)
                switch.configure(command=lambda: generate_box1(switch, string, profileNb))
                if i == 1:
                    switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
                if i == 2:
                    switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
                if i == 3:
                    switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")

                switch.grid(row=rowParam, column=0, sticky='we', padx=(40, 20), pady=1)
                if data[self.sel]['schedules'][str(profileNb)][string] == True:
                    switch.select()
                else:
                    switch.deselect()

            for i in range(1, 4):
                create_switch_enabled(page, f"Profile n°{i}", "enabled", i, i)

            def submit():
                page.destroy()

            button = customtkinter.CTkButton(page, text="Save changes", command=submit, corner_radius=4,
                                             fg_color="white", border_color="grey", border_width=1, text_color="black")
            button.grid(row=7, column=0, columnspan=4, pady=(5, 5), padx=(20, 20))

        scheduler_button = create_button1(root1, "⚙", lambda: scheduler_config(root1), 5)
        scheduler_switch = customtkinter.CTkSwitch(root1, text="Multiple Profiles")
        scheduler_switch.configure(command=lambda: generate_box2(scheduler_switch, "scheduler"))
        scheduler_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")

        scheduler_switch.grid(row=5, column=0, sticky='w', padx=(10, 0), pady=1)
        if data[self.sel]["scheduler"] == True:
            scheduler_switch.select()
        else:
            scheduler_switch.deselect()

        def submit():
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            data[self.sel]['API_KEY'] = entry.get()
            with open('user_settings.json', 'w') as config_file: config_file.write(json.dumps(data, indent=2))
            root1.destroy()

        submit_button = customtkinter.CTkButton(root1, text="Save changes", command=submit, corner_radius=4,
                                                border_color="grey", border_width=1, hover_color="#266496", text_color="black")
        submit_button.grid(row=10, column=0, columnspan=2, pady=(5, 5))

        # redo_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
        # redo_button.configure(hover_color="#266496")
        for profile in self.data[self.sel]['schedules']:
            if self.data[self.sel]['schedules'][str(profile)]['enabled']:
                combobox.set(f"Profile n°{profile}")
                dict[int(profile)].tkraise()
                # print(profile)
                if profile == "1":
                    combobox.configure(fg_color="#3b8ed0", selected_color="#266496", selected_hover_color="#266496")
                    redo_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
                    redo_button.configure(hover_color="#266496", fg_color="#3b8ed0")
                    scheduler_switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")
                    scheduler_button.configure(hover_color="#266496", fg_color="#3b8ed0")
                    submit_button.configure(hover_color="#266496", fg_color="#3b8ed0")
                if profile == "2":
                    combobox.configure(fg_color="#ba4543", selected_color="#913230", selected_hover_color="#913230")
                    redo_switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
                    redo_button.configure(hover_color="#913230", fg_color="#ba4543")
                    scheduler_switch.configure(progress_color="#ba4543", button_color="#913230", button_hover_color="#913230")
                    scheduler_button.configure(hover_color="#913230", fg_color="#ba4543")
                    submit_button.configure(hover_color="#913230", fg_color="#ba4543")
                if profile == "3":
                    combobox.configure(fg_color="#dec433", selected_color="#baa429", selected_hover_color="#baa429")
                    redo_switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")
                    redo_button.configure(hover_color="#baa429", fg_color="#dec433")
                    scheduler_switch.configure(progress_color="#dec433", button_color="#baa429", button_hover_color="#baa429")
                    scheduler_button.configure(hover_color="#baa429", fg_color="#dec433")
                    submit_button.configure(hover_color="#baa429", fg_color="#dec433")
                break

        # dict[1].tkraise()
        root1.mainloop()

    with open('user_settings.json') as config_file:
        data = json.load(config_file)

    def update_timers(self):
        # for key in frames.keys():
        #     print(f"{key}")
        #     # if frames[key].tasks_process.is_alive():
        #     print(f"{frames[key].tasks_process.is_alive() = }")
        # print(f"{len(self.upper_frame.tree_view.get_children())}")
        for child in self.upper_frame.tree_view.get_children():
            # print(f"{self.upper_frame.tree_view.item(child)['values'] = }")
            # for key in frames:
            #     print(f"key :{key}")
            #     print(f"child value [0] = {self.upper_frame.tree_view.item(child)['values'][0]}")
            #     print(f"{int(key)==self.upper_frame.tree_view.item(child)['values'][0]}")
            # if self.upper_frame.tree_view.item(child)['values'][0] == int(key):
            #     print(child, time())
            # print(f"{self.upper_frame.tree_view.item(child)['values'][0]==int(key) and self.upper_frame.tree_view.item(child)['values'][-1]=='' = }")
            text = self.upper_frame.tree_view.item(child)['values']
            # print(text, child)
            if text[-1].count(":") == 2 and text[-1] != '00:00:00' and len(text[-1]) == 8:
                # print(text[-1])
                date_time_obj = datetime.strptime(text[-1], "%H:%M:%S")
                text[-1] = (date_time_obj - timedelta(seconds=1)).strftime("%H:%M:%S")
                self.upper_frame.tree_view.item(child, values=text)
        # return self.upper_frame.tree_view.after(1000,self.update_timers)

    def update_label2(self, sel, string):
        # print(sel)
        # print(type(sel))
        key = sel
        if self.upper_frame.frames[key].tasks_process.is_alive():
            # print(f"{frames[key].tasks_process.is_alive() = }")
            for child in self.upper_frame.tree_view.get_children():
                # print(f"{self.upper_frame.tree_view.item(child)['values'] = }")
                if self.upper_frame.tree_view.item(child)['values'][0] == int(key):
                    # print(f"{self.upper_frame.tree_view.item(child)['values'][0]==int(key) and self.upper_frame.tree_view.item(child)['values'][-1]=='' = }")
                    text = self.upper_frame.tree_view.item(child)['values']
                    text[-1] = string
                    # print(f"{text = }")
                    self.upper_frame.tree_view.item(child, values=text)
                    # print(f"{self.upper_frame.tree_view.item(child)['values'] =}")
        else:
            for child in self.upper_frame.tree_view.get_children():
                if self.upper_frame.tree_view.item(child)['values'][0] == int(key) and \
                        self.upper_frame.tree_view.item(child)['values'][-1] != '':
                    text = self.upper_frame.tree_view.item(child)['values']
                    text[-1] = ""
                    self.upper_frame.tree_view.item(child, values=text)

    def start_tasks(self):
        self.tasks.text_update_event = self.update_label2
        if not self.tasks_process.is_alive():
            self.tasks_process = threading.Thread(target=self.tasks.routine_scheduled)
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

    def start_thread(self):
        sleep(0.5)
        return self.root.after(1000, self.process_is_alive)

    def end_tasks(self):
        # def _async_raise(tid, exctype):
        #     tid = ctypes.c_long(tid)
        #     if not inspect.isclass(exctype):
        #         exctype = type(exctype)
        #     res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
        #     if res == 0:
        #         raise ValueError("invalid thread id")
        #     elif res != 1:
        #         ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
        #         raise SystemError("PyThreadState_SetAsyncExc failed")
        # _async_raise(self.tasks_process.ident, SystemExit)
        self.stop = True
        self.update_label2(self.sel, "")
        self.start_tasks_button.configure(state="normal", fg_color="white")
        self.end_tasks_button.configure(state="disabled", fg_color="#d1d1d1")



