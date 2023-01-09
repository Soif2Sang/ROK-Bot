import json
import tkinter

import customtkinter
from tktooltip import ToolTip

class GemInterface(customtkinter.CTkToplevel):
    def __init__(self, root, instance, profile):
        super().__init__(root)

        with open('user_settings.json') as config_file:
            data = json.load(config_file)

        self.instance = instance
        self.profile = profile

        self.resizable(False, False)
        self.title("Gem Interface")
        self.iconbitmap('Item_Gem.ico')

        self.label_kingdom = customtkinter.CTkLabel(self, text="Your kingdom : ")
        self.label_x = customtkinter.CTkLabel(self, text="Area location x : ")
        self.label_y = customtkinter.CTkLabel(self, text="Area location y : ")
        self.label_km = customtkinter.CTkLabel(self, text="Searching Radius(km) : ")
        self.label_duration = customtkinter.CTkLabel(self, text="Mining duration(mins): ")
        self.label_frequency = customtkinter.CTkLabel(self, text="Look for available\n troops each X (secs): ")
        self.label_seperation1 = tkinter.Label(self, text="~")
        self.label_seperation2 = tkinter.Label(self, text="~")

        ToolTip(self.label_frequency,
                msg="This settings is to configure how frequently the bot will check for an available troop\n*WARNING* Don't lower too much !",
                delay=0.3)

        self.entry_kingdom = customtkinter.CTkEntry(self, width=70)
        self.entry_x = customtkinter.CTkEntry(self, width=70)
        self.entry_y = customtkinter.CTkEntry(self, width=70)
        self.entry_km = customtkinter.CTkEntry(self, width=70)
        self.entry_duration1 = customtkinter.CTkEntry(self, width=70)
        self.entry_duration2 = customtkinter.CTkEntry(self, width=70)
        self.entry_frequency1 = customtkinter.CTkEntry(self, width=70)
        self.entry_frequency2 = customtkinter.CTkEntry(self, width=70)

        self.switch_restart = customtkinter.CTkSwitch(self,text='Sometimes restart game'
                                                      ,command=lambda: self.switch_keyword('restart_game'))
        self.switch_experimental = customtkinter.CTkSwitch(self, text='Enable experimental mode',
                                                  command=lambda: self.switch_keyword('gem_experimental'))

        self.button_submit = customtkinter.CTkButton(self, text="Save changes", command=self.submit, corner_radius=4,
                                                     fg_color="white", border_color="grey", border_width=1, text_color="black")

        self.entry_kingdom.insert(0, data[instance]['schedules'][profile]['kingdom'])
        self.entry_x.insert(0, data[instance]['schedules'][profile]['city_x'])
        self.entry_y.insert(0, data[instance]['schedules'][profile]['city_y'])
        self.entry_km.insert(0, data[instance]['schedules'][profile]['radius'])
        self.entry_duration1.insert(0, data[instance]['schedules'][profile]['gather_gem_duration1'])
        self.entry_duration2.insert(0, data[instance]['schedules'][profile]['gather_gem_duration2'])
        self.entry_frequency1.insert(0, data[instance]['schedules'][profile]['gem_check1'])
        self.entry_frequency2.insert(0, data[instance]['schedules'][profile]['gem_check2'])

        if data[instance]['schedules'][profile]['restart_game']:
            self.switch_restart.select()
        else:
            self.switch_restart.deselect()
        if data[instance]['schedules'][profile]['gem_experimental']:
            self.switch_experimental.select()
        else:
            self.switch_experimental.deselect()

        self.label_kingdom.grid(row=1, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
        self.entry_kingdom.grid(row=1, column=1, columnspan=2)
        self.label_x.grid(row=2, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
        self.entry_x.grid(row=2, column=1, columnspan=2)
        self.label_y.grid(row=3, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
        self.entry_y.grid(row=3, column=1, columnspan=2)
        self.label_km.grid(row=4, column=0, columnspan=1, pady=2, sticky='e', padx=(5, 0))
        self.entry_km.grid(row=4, column=1, columnspan=2)
        self.entry_duration1.grid(row=5, column=1)
        self.entry_duration2.grid(row=5, column=3)
        self.label_duration.grid(row=5, column=0)
        self.label_frequency.grid(row=6, column=0)
        self.label_seperation1.grid(row=5, column=2, columnspan=1, pady=2)
        self.label_seperation2.grid(row=6, column=2, columnspan=1, pady=2)
        self.entry_frequency1.grid(row=6, column=1)
        self.entry_frequency2.grid(row=6, column=3)
        self.switch_restart.grid(row=60, column=0, columnspan=4, pady=(5, 5))
        self.switch_experimental.grid(row=80, column=0, columnspan=4, pady=(5, 5))
        self.button_submit.grid(row=81, column=0, columnspan=4, pady=(5, 5))

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

    def submit(self):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        data[self.instance]['schedules'][self.profile]['kingdom'] = self.entry_kingdom.get()
        data[self.instance]['schedules'][self.profile]['city_y'] = int(self.entry_y.get())
        data[self.instance]['schedules'][self.profile]['city_x'] = int(self.entry_x.get())
        data[self.instance]['schedules'][self.profile]['radius'] = int(self.entry_km.get())
        data[self.instance]['schedules'][self.profile]['gather_gem_duration1'] = int(self.entry_duration1.get())
        data[self.instance]['schedules'][self.profile]['gather_gem_duration2'] = int(self.entry_duration2.get())
        data[self.instance]['schedules'][self.profile]['gem_check1'] = int(self.entry_frequency1.get())
        data[self.instance]['schedules'][self.profile]['gem_check2'] = int(self.entry_frequency2.get())
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))
        self.destroy()



#     def submit(self):
#         with open('user_settings.json') as config_file:
#             data = json.load(config_file)
#         data[self.instance]['schedules'][self.profile]['kingdom'] = self.entry_kingdom.get()
#         data[self.instance]['schedules'][self.profile]['city_y'] = int(self.entry_y.get())
#         data[self.instance]['schedules'][self.profile]['city_x'] = int(self.entry_x.get())
#         data[self.instance]['schedules'][self.profile]['radius'] = int(self.entry_km.get())
#         data[self.instance]['schedules'][self.profile]['gather_gem_duration1'] = int(self.entry_duration1.get())
#         data[self.instance]['schedules'][self.profile]['gather_gem_duration2'] = int(self.entry_duration2.get())
#         data[self.instance]['schedules'][self.profile]['gem_check1'] = int(self.entry_frequency1.get())
#         data[self.instance]['schedules'][self.profile]['gem_check2'] = int(self.entry_frequency2.get())
#         with open('user_settings.json', 'w') as config_file:
#             config_file.write(json.dumps(data, indent=2))
#         self.destroy()
#
# fenetre = customtkinter.CTk()
#
# app = RssInterface(fenetre,"1","1")
# app.mainloop()