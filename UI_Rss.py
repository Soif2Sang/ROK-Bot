import json
import tkinter

import customtkinter
from tktooltip import ToolTip



class RssInterface(customtkinter.CTkToplevel):
    def __init__(self, root, instance, profile):
        super().__init__(root)

        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        self.instance = instance
        self.profile = profile

        self.resizable(False, False)
        self.title("Rss Interface")
        self.iconbitmap('Item_Gem.ico')

        paddings = {'padx': 5, 'pady': 5}

        self.label_1 = customtkinter.CTkLabel(self, text="1st choice :")
        self.label_2 = customtkinter.CTkLabel(self, text="2nd choice :")
        self.label_3 = customtkinter.CTkLabel(self, text="3rd choice :")
        self.label_4 = customtkinter.CTkLabel(self, text="4th choice :")
        self.label_5 = customtkinter.CTkLabel(self, text="5th choice :")
        self.label_6 = customtkinter.CTkLabel(self, text="6th choice :")
        self.label_7 = customtkinter.CTkLabel(self, text="7th choice :")

        self.label_1.grid(column=0, row=0, **paddings, sticky='e')
        self.label_2.grid(column=0, row=1, **paddings, sticky='e')
        self.label_3.grid(column=0, row=2, **paddings, sticky='e')
        self.label_4.grid(column=0, row=3, **paddings, sticky='e')
        self.label_5.grid(column=0, row=4, **paddings, sticky='e')
        self.label_6.grid(column=0, row=5, **paddings, sticky='e')
        self.label_7.grid(column=0, row=6, **paddings, sticky='e')

        self.switch_custom = customtkinter.CTkSwitch(self,text='Use Yellow Preset'
                                                      ,command=lambda: self.switch_keyword('restart_game'))

        if data[self.instance]['schedules'][str(self.profile)]['rss_custom_preset']:
            # print(f" {restart_button.get() = }")
            self.switch_custom.select()
            # print(f" {restart_button.get() = }")
        else:
            self.switch_custom.deselect()

        resources = ['food node', 'wood node', 'stone node', 'gold node']

        option1_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["First"]) + " node")
        option2_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Second"]) + " node")
        option3_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Third"]) + " node")
        option4_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Fourth"]) + " node")
        option5_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Fifth"]) + " node")
        option6_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Sixth"]) + " node")
        option7_var = customtkinter.StringVar(value=str(data[self.instance]['schedules'][str(self.profile)]["Seventh"]) + " node")

        option1 = customtkinter.CTkOptionMenu(master=self, variable=option1_var, values=resources,
                                              fg_color="white", text_color="black")
        option2 = customtkinter.CTkOptionMenu(master=self, variable=option2_var, values=resources,
                                              fg_color="white", text_color="black")
        option3 = customtkinter.CTkOptionMenu(master=self, variable=option3_var, values=resources,
                                              fg_color="white", text_color="black")
        option4 = customtkinter.CTkOptionMenu(master=self, variable=option4_var, values=resources,
                                              fg_color="white", text_color="black")
        option5 = customtkinter.CTkOptionMenu(master=self, variable=option5_var, values=resources,
                                              fg_color="white", text_color="black")
        option6 = customtkinter.CTkOptionMenu(master=self, variable=option6_var, values=resources,
                                               fg_color="white", text_color="black")
        option7 = customtkinter.CTkOptionMenu(master=self, variable=option7_var, values=resources,
                                              fg_color="white", text_color="black")

        option1.configure(command=lambda _: self.choice_box("First", option1))
        option2.configure(command=lambda _: self.choice_box("Second", option2))
        option3.configure(command=lambda _: self.choice_box("Third", option3))
        option4.configure(command=lambda _: self.choice_box("Fourth", option4))
        option5.configure(command=lambda _: self.choice_box("Fifth", option5))
        option6.configure(command=lambda _: self.choice_box("Sixth", option6))
        option7.configure(command=lambda _: self.choice_box("Seventh", option7))

        option1.grid(column=1, row=0, **paddings, sticky='e')
        option2.grid(column=1, row=1, **paddings, sticky='e')
        option3.grid(column=1, row=2, **paddings, sticky='e')
        option4.grid(column=1, row=3, **paddings, sticky='e')
        option5.grid(column=1, row=4, **paddings, sticky='e')
        option6.grid(column=1, row=5, **paddings, sticky='e')
        option7.grid(column=1, row=6, **paddings, sticky='e')

        levels = ["level " + str(i) for i in range(1, 10)]

        option1_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["First_level"]))
        option2_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Second_level"]))
        option3_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Third_level"]))
        option4_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Fourth_level"]))
        option5_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Fifth_level"]))
        option6_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Sixth_level"]))
        option7_var_level = customtkinter.StringVar(value="level " + str(data[self.instance]['schedules'][str(self.profile)]["Seventh_level"]))

        option_level1 = customtkinter.CTkOptionMenu(master=self, variable=option1_var_level, values=levels,
                                              fg_color="white", text_color="black")
        option_level2 = customtkinter.CTkOptionMenu(master=self, variable=option2_var_level, values=levels,
                                              fg_color="white", text_color="black")
        option_level3 = customtkinter.CTkOptionMenu(master=self, variable=option3_var_level, values=levels,
                                              fg_color="white", text_color="black")
        option_level4 = customtkinter.CTkOptionMenu(master=self, variable=option4_var_level, values=levels,
                                              fg_color="white", text_color="black")
        option_level5 = customtkinter.CTkOptionMenu(master=self, variable=option5_var_level, values=levels,
                                              fg_color="white", text_color="black")
        option_level6 = customtkinter.CTkOptionMenu(master=self, variable=option6_var_level, values=levels,
                                               fg_color="white", text_color="black")
        option_level7 = customtkinter.CTkOptionMenu(master=self, variable=option7_var_level, values=levels,
                                              fg_color="white", text_color="black")

        option_level1.configure(command=lambda _: self.choice_box1("First_level", option_level1))
        option_level2.configure(command=lambda _: self.choice_box1("Second_level", option_level2))
        option_level3.configure(command=lambda _: self.choice_box1("Third_level", option_level3))
        option_level4.configure(command=lambda _: self.choice_box1("Fourth_level", option_level4))
        option_level5.configure(command=lambda _: self.choice_box1("Fifth_level", option_level5))
        option_level6.configure(command=lambda _: self.choice_box1("Sixth_level", option_level6))
        option_level7.configure(command=lambda _: self.choice_box1("Seventh_level", option_level7))

        option_level1.grid(column=2, row=0, **paddings, sticky='e')
        option_level2.grid(column=2, row=1, **paddings, sticky='e')
        option_level3.grid(column=2, row=2, **paddings, sticky='e')
        option_level4.grid(column=2, row=3, **paddings, sticky='e')
        option_level5.grid(column=2, row=4, **paddings, sticky='e')
        option_level6.grid(column=2, row=5, **paddings, sticky='e')
        option_level7.grid(column=2, row=6, **paddings, sticky='e')

    def switch_keyword(self, keyword):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        # print(f" {self.restart_button.get() = }")
        if self.switch_restart.get():
            data[self.instance]['schedules'][self.profile][keyword] = True
            self.switch_restart.select()
        else:
            data[self.instance]['schedules'][self.profile][keyword] = False
            self.switch_restart.deselect()
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))
        print(f"{data[self.instance]['schedules'][self.profile][keyword] = }")

    def choice_box(self, keyword, box):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        data[self.instance]['schedules'][str(self.profile)][keyword] = box.get().split(" node")[0]

        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))

    def choice_box1(self, keyword, box):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        data[self.instance]['schedules'][str(self.profile)][keyword] = int(box.get()[-1])

        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))

# fenetre = customtkinter.CTk()
#
# app = GemInterface(fenetre,"1","1")
# app.mainloop()