import json
from tkinter import Label

import customtkinter
from tktooltip import ToolTip

import OLD_UI_Narrow
from OLD_UI_Gem import GemInterface
from OLD_UI_Rss import RssInterface


class Settings:
    def __init__(self, ui:UI_Narrow):
        self.sel = ui.sel
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
            self.data = data
        self.root = customtkinter.CTkToplevel(ui.root)
        self.root.title('RoK Bot Settings')
        self.root.resizable(False, False)
        self.root.iconbitmap('Item_Gem.ico')
    
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
    
        combobox = customtkinter.CTkSegmentedButton(master=self.root,
                                                    values=["Profile n°1", "Profile n°2", "Profile n°3"],
                                                    fg_color="#3b8ed0", text_color="white", selected_color="#266496", selected_hover_color="#266496")
        combobox.configure(command=lambda x: optionmenu_callback(combobox))
        combobox.grid(column=0, row=0, columnspan=2, pady=(0, 10))
    
        label = customtkinter.CTkLabel(self.root, text="Custom API Key : ")
        entry = customtkinter.CTkEntry(self.root)
        entry.insert(0, data[self.sel]['API_KEY'])
        label.grid(row=1, column=0)
        entry.grid(row=1, column=1, padx=(15, 0))
        dict = {}
    
        def generate_box(switch, string, i):
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
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
    
                create_button(root, "⚙", lambda: RssInterface(root, str(self.sel), str(i)), nb_switch)
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

                nb_switch = create_switch(root, "Claim Daily Quests", "claim_daily_quests", nb_switch, i)
    
                nb_switch = create_switch(root, "Claim Campaign Rewards", "claim_campaign", nb_switch, i)
    
                create_button(root, "⚙", lambda: rally_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Launch Rally", "start_fort", nb_switch, i)
    
                create_button(root, "⚙", lambda: healing_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Healing", "heal_troop", nb_switch, i)
                create_button(root, "⚙", lambda: material_config(root, i), nb_switch)
                nb_switch = create_switch(root, "Material Production", "material_production", nb_switch, i)
                nb_switch = create_switch(root, "Alliance Help", "alliance_help", nb_switch, i)
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
            dict[i] = Profile(self.sel, self.root, i).root

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
            labeld1 = customtkinter.CTkLabel(page, text="*The bigger the gap is, the safer it gets*", text_color="red",
                                             font=customtkinter.CTkFont(family='Helvetica bold', size=15))
            labeld1.grid(row=0, column=0, columnspan=4, pady=2, sticky='ew')
    
            labeld2 = customtkinter.CTkLabel(page, text="~")
            labeld2.grid(row=1, column=2, columnspan=1, pady=2)
    
            labeld1 = customtkinter.CTkLabel(page, text="Pause between two runs\nbefore the bot re-do the tasks : ")
            labeld1.grid(row=1, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
            labeld2 = Label(page, text="~")
            labeld2.grid(row=1, column=2, columnspan=1, pady=2)
    
            entryd1 = customtkinter.CTkEntry(page, width=45)
            entryd1.insert(0, data[self.sel]['time_to_wait_loop1'])
            entryd1.grid(row=1, column=1, pady=(10, 0))
    
            entryd2 = customtkinter.CTkEntry(page, width=45)
            entryd2.insert(0, data[self.sel]['time_to_wait_loop2'])
            entryd2.grid(row=1, column=3, pady=(5, 0), padx=(0, 5))

            minutes = customtkinter.CTkLabel(page, text="minutes")
            minutes.grid(row=1, column=4, columnspan=1, pady=2, sticky='e', padx=(5, 5))

            switch = customtkinter.CTkSwitch(page, text="Once the bot did all the tasks, \n"
                                                        "Close the game.\n"
                                                        "The bot will log back once the timer ends")
            switch.configure(command=lambda: generate_box2(switch, "leave_game_loop", ))
            switch.configure(progress_color="#3b8ed0", button_color="#266496", button_hover_color="#266496")

            switch.grid(row=3, column=0, sticky='w', padx=(10, 0), pady=1, columnspan=4)
            if data[self.sel]["leave_game_loop"] == True:
                switch.select()
            else:
                switch.deselect()
    
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
    
        redo_button = create_button1(self.root, "⚙", lambda: redo_config(self.root), 4)
    
        redo_switch = create_switch1(self.root, "Re-do Tasks", "loop_task", 4)
    
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

            # def generate_box1(switch, string, i):
            #     with open('user_settings.json') as config_file:
            #         data = json.load(config_file)
            #     if switch.get():
            #         data[self.sel]['schedules'][str(i)][string] = True
            #         switch.select()
            #     else:
            #         data[self.sel]['schedules'][str(i)][string] = False
            #         switch.deselect()
            #     with open('user_settings.json', 'w') as config_file:
            #         config_file.write(json.dumps(data, indent=2))
            #     print(f"{string} = {data[self.sel]['schedules'][str(i)][string]}")
    
            def create_switch_enabled(rootParam, textParam, string, rowParam, profileNb):
                switch = customtkinter.CTkSwitch(rootParam, text=textParam)
                switch.configure(command=lambda: generate_box(switch, string, profileNb))
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
    
        scheduler_button = create_button1(self.root, "⚙", lambda: scheduler_config(self.root), 5)
        scheduler_switch = customtkinter.CTkSwitch(self.root, text="Multiple Profiles")
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
            self.root.destroy()
    
        submit_button = customtkinter.CTkButton(self.root, text="Save changes", command=submit, corner_radius=4,
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
        self.root.mainloop()

