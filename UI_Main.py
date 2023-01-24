import ctypes
import inspect
import tkinter

from tkinter import *
from tkinter import ttk

from UI_Narrow import LowerFrame
from bot_adb import Adb
from Tasks_lib import *
import os
import pyautogui
import requests
import customtkinter
from urllib3 import Retry, PoolManager
from tktooltip import ToolTip
from pystray import MenuItem as item
import threading
import pystray

customtkinter.set_appearance_mode("light")

if not os.path.exists("user_settings.json"):
    with open('user_settings.json', 'w') as f:
        json.dump({}, f, indent=2)
        print("User settings created")

# Initialize user_settings & frames
with open('user_settings.json') as config_file: data = json.load(config_file)


def acces(date='9999-12-30'):
    for i in range(5):
        try:
            # from WorldTimeAPI import service as serv
            # myclient = serv.Client('timezone')
            # requests = {"area": "Europe", "location": "Paris"}
            # response = myclient.get(**requests)
            # tab = response.datetime.split("T")
            # url = "http://worldtimeapi.org/api/timezone/Europe/Paris"
            # response = requests.request("GET", url)
            # tab = response.json()['datetime'].split("T")
            # tmp = tab[1].split(".")
            # tab[1] = tmp[0]
            retries = Retry(connect=5, read=2, redirect=5)
            http = PoolManager(retries=retries)
            response = http.request("GET", "http://worldtimeapi.org/api/timezone/Europe/Paris",
                                    headers={'Content-Type': 'application/json'}, retries=Retry(10))
            # url = "http://worldtimeapi.org/api/timezone/Europe/Paris"
            # headers = {"Content-Type": "application/json"}
            # response = requests.request("GET", url, headers=headers,  retries=Retry(10))
            tab = json.loads(response.data.decode('utf-8'))['datetime'].split("T")
            # # print(tab)
            tmp = tab[1].split(".")
            tab[1] = tmp[0]
            if tab[0] > date:
                return False
            else:
                return True
        except Exception as e:
            print(e)
            if i == 4:
                print("Couldn't make connection, contact the admin")
            tmp = i
    return False


def request_acess(username, password):

    try:
        # print("username = ", username, password)
        import json
        url = "https://rokbot-2e6f.restdb.io/rest/auth"

        payload = json.dumps({'username': username, 'password': password})

        parameter = {"q": payload}

        headers = {
            'content-type': "application/json",
            'x-apikey': "632031befdc15b0265f17372",
            'cache-control': "no-cache"
        }

        response = requests.request("GET", url, params=parameter, headers=headers)
        # print(f" Request acces {response.status_code=}")
        data = response.json()
        # print(data)
        if data == []:
            # print("data == []")
            return False
        # print(data)
        data = data[0]
        if data['abo'] is None:
            return False
        else:
            heure = data['abo'].split("T")
            if not acces(heure[0]):
                return False
            else:
                return True
    except Exception:
        print("Could not make connection to the server")
        exit(1)

class Main:
    def __init__(self, days):
        # root = Frame(master=window)
        self.root = customtkinter.CTk()
        # self.root = Tk()
        # print(f"{self.root.cget('bg') =}")
        self.root.resizable(False, False)
        self.root.title(f'RoK Bot - {days} Days left')
        self.root.iconbitmap('Item_Gem.ico')
        self.frames = {}
        # self.root.geometry(f"{150}x{250}")
        # self.root['bg']='red'
        s = ttk.Style()

        # Set the selection background color to green.
        s.map("Custom.Treeview", background=[("selected", "#a7a7a7")])
        s.configure('Treeview', rowheight=30)
        self.tree_view = ttk.Treeview(self.root, columns=[1, 2, 3], height=8, show="headings",style="Custom.Treeview")
        self.tree_view.column(1, width=30, anchor=CENTER)
        self.tree_view.column(2, width=120, anchor=CENTER)
        self.tree_view.column(3, width=160, anchor=W)

        self.tree_view.heading(1, text="Id")
        self.tree_view.heading(2, text="Name", anchor=CENTER)
        self.tree_view.heading(3, text="Status", anchor=W)

        self.L = customtkinter.CTkLabel(self.root, text="")

        self.instance_name = customtkinter.CTkLabel(self.root, text="")
        self.instance_name.grid(row=0, column=0, sticky="e")

        self.refresh_tab = customtkinter.CTkButton(self.root, text="⟳", command=self.update_vms, fg_color="white", text_color="black",border_color="grey", border_width=1,width = 20)
        self.refresh_tab.grid(row=0, column=1, sticky="")

        self.tree_view.bind('<<TreeviewSelect>>', self.select)
        self.tree_view.grid(row=1, column=0, columnspan=2, padx=(20, 20), pady=(0, 5))
        self.tree_view.configure(height=3)

        self.tree_view.after(1000, self.update_timers)

        # scroll_bar = ttk.Scrollbar(self.root, orient="vertical", command=self.tree_view.yview)
        # scroll_bar.grid(row=1, column=1, sticky='nse', padx=(0, 0))
        # self.tree_view.configure(yscrollcommand=scroll_bar.set)

        # Frame(
        # customtkinter.CTkFrame(
        # Place frame1
        # self.root_frame1 = Frame(self.root)
        # self.root_frame1.grid(row=3, column=0, columnspan=2)
        # self.root.grid(row=0,column=0)
        # self.root.update_idletasks()
        # width = self.root.winfo_width()
        # height = self.root.winfo_height()
        # window.geometry(f"{width}x{height}")
        # def quit_window(icon, item):
        #     icon.stop()
        #     self.root.destroy()
        #
        # # Define a function to show the window again
        # def show_window(icon, item):
        #     icon.stop()
        #     self.root.after(0, self.root.deiconify())
        #
        # def hide_window():
        #     self.root.withdraw()
        #     image = Image.open("Item_Gem.ico")
        #     menu = (item(text='Open', action=show_window, default=True, visible=False),
        #             item(text='Open', action=show_window),
        #             item(text='Quit',  action=quit_window))
        #     icon = pystray.Icon("name", image, "Rise of Kingdom Bot", menu)
        #     icon.run()

        # def quit():
        #     sys.exit(1)

        self.update_vms()
        self.root.after(1000 * 3600 * 24, self.is_account_expired)
        # self.root.protocol('WM_DELETE_WINDOW', hide_window)
        # self.root.protocol('WM_DELETE_WINDOW', quit)
        self.root.mainloop()

    def update_timers(self):
        for child in self.tree_view.get_children():
            text = self.tree_view.item(child)['values']
            # print(text, child)
            if text[-1].count(":") == 2 and text[-1] != '00:00:00' and len(text[-1]) == 8:
                # print(text[-1])
                date_time_obj = datetime.strptime(text[-1], "%H:%M:%S")
                text[-1] = (date_time_obj - timedelta(seconds=1)).strftime("%H:%M:%S")
                self.tree_view.item(child, values=text)
        return self.tree_view.after(1000, self.update_timers)

    def select(self, event):
        with open('user_settings.json') as config_file:
            data = json.load(config_file)
        try:
            sel = str(self.tree_view.item(event.widget.selection())['values'][0])
            # print(sel)
            # print(self.tree_view.item(event.widget.selection()))
        except:
            self.instance_name.configure(text="")
            return
        all_instances = self.get_all_vms_running()
        dico_instance = self.get_dic_instances()
        self.instance_name.configure(text=index_of_first(all_instances, sel[0]))
        default_dic = {
            'instance': dico_instance[str(sel[0])]['instance'],
            'name': dico_instance[str(sel[0])]['name'],
            'host': '127.0.0.1',
            'port': int(dico_instance[str(sel[0])]['port']),
            'API_KEY': "",
            'loop_task': False,
            'time_to_wait_loop1': 60,
            'time_to_wait_loop2': 110,
            'leave_game_loop' : True,
            'scheduler': False,
            'schedules': {}
        }
        for i in range(1, 4):
            default_dic['schedules'][i] ={
                    'enabled': False,
                    'kingdom': 0,
                    'city_x': 0,
                    'city_y': 0,
                    'radius': 30,
                    "First": "stone",
                    "Second": "food",
                    "Third": "gold",
                    "Fourth": "wood",
                    "Fifth": "food",
                    "Sixth": "food",
                    "Seventh": "food",
                    "First_level": 6,
                    "Second_level": 6,
                    "Third_level": 6,
                    "Fourth_level": 6,
                    "Fifth_level": 6,
                    "Sixth_level": 6,
                    "Seventh_level": 6,
                    "rss_custom_preset" : False,
                    'auto_reconnect': True,
                    'auto_captcha': True,
                    'check_donation': False,
                    'use_enhanced_buff': False,
                    'gather_rss': False,
                    'buy_merchant': False,
                    'claim_daily_quests' : False,
                    'collect_ressource': False,
                    'defeat_barbarians': False,
                    'barbarians_level': 25,
                    'gather_gem': False,
                    'gem_check1': 60,
                    'gem_check2': 120,
                    'gem_experimental': False,
                    'gather_gem_duration1': 60,
                    'gather_gem_duration2': 90,
                    'restart_game': False,
                    'switch_character': False,
                    'leave_game_switch_character': False,
                    "scout_fog": False,
                    "scout_duration1": 60,
                    "scout_duration2": 90,
                    "scout_building_x": 730,
                    "scout_building_y": 410,
                    "slow_mode": False,
                    "sleep_multiplicator": 1,
                    "auto_log_back": True,
                    "log_back1": 5,
                    "log_back2": 10,
                    "claim_daily_vip": False,
                    "claim_daily_chest": False,
                    "claim_campaign" : False,
                    "start_fort": False,
                    "rally_type": 'cav',
                    "rally_time": 10,
                    "rally_radius": 20,
                    "rally_count": 2,
                    "mauraudeurs_forts": False,
                    "heal_troop": False,
                    "healing_building_x": 980,
                    "healing_building_y": 267,
                    "healing_count": 1500,
                    "material_production": False,
                    "material_choice_1": "leather",
                    "material_choice_2": "leather",
                    "material_choice_3": "leather",
                    "material_choice_4": "leather",
                    "material_choice_5": "leather"
            }
        default_dic['schedules'][1]['enabled']= True
        if str(sel[0]) not in data:
            data[str(sel[0])] = default_dic
        else:
            for key in default_dic:
                if key not in data[str(sel[0])]:
                    data[str(sel[0])][key] = default_dic[key]

            for key in default_dic['schedules'][1]:
                for i in range(1, 4):
                    if key not in data[str(sel[0])]['schedules'][str(i)]:
                        data[str(sel[0])]['schedules'][str(i)][key] = default_dic['schedules'][1][key]

        data[str(sel[0])]['name'] = dico_instance[str(sel[0])]['name']
        data[str(sel[0])]['port'] = int(dico_instance[str(sel[0])]['port'])
        data[str(sel[0])]['instance'] = dico_instance[str(sel[0])]['instance']
        with open('user_settings.json', 'w') as outfile:
            json.dump(data, outfile, indent=2)
        if sel[0] in self.frames:
            self.frames[sel[0]].bottom_frame.tkraise()
        else:
            self.frames[sel[0]] = LowerFrame(self, sel)
        self.root.update()

    def is_account_expired(self):
        # print("Checking if the account has expired")
        try:
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            if "user" in data:
                if not request_acess(data['user']["username"], data['user']["password"]):
                    self.root.destroy()
            return self.root.after(1000 * 3600 * 24, self.is_account_expired)
        except Exception:
            print("Problem in is_account_expired")
            exit(1)

    def update_label(self):
        for key in self.frames.keys():
            # print(dir(self.frames[key]))
            if self.frames[key].tasks_process.is_alive():
                # print(f"{self.frames[key].tasks_process.is_alive() = }")
                for child in self.tree_view.get_children():
                    # print(f"{self.tree_view.item(child)['values'] = }")
                    if self.tree_view.item(child)['values'][0] == int(key) and self.tree_view.item(child)['values'][
                        -1] == '':
                        # print(f"{self.tree_view.item(child)['values'][0]==int(key) and self.tree_view.item(child)['values'][-1]=='' = }")
                        text = self.tree_view.item(child)['values']
                        text[-1] = "Running.."
                        self.tree_view.item(child, values=text)
            else:
                for child in self.tree_view.get_children():
                    if self.tree_view.item(child)['values'][0] == int(key) and self.tree_view.item(child)['values'][
                        -1] != '':
                        text = self.tree_view.item(child)['values']
                        text[-1] = ""
                        self.tree_view.item(child, values=text)
        return self.tree_view.after(1000, self.update_label)


    # self.tree_view.after(1000, update_label)
    def get_dic_instances(self):
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

        def sort_by_instance(tab):
            for i in range(len(tab)):
                for y in range(len(tab) - 1):
                    if len(tab[y]['instance']) == len(tab[y + 1]['instance']):
                        if tab[y]['instance'] > tab[y + 1]['instance']:
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
                    else:
                        if len(tab[y]['instance']) > len(tab[y + 1]['instance']):
                            tab[y], tab[y + 1] = tab[y + 1], tab[y]
            dic = {}
            for i in range(len(tab)):
                dic[str(i)] = tab[i]
            return dic
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
                    'display_name' in element)):
                liste_info.append(element)
        # for element in liste_info: print(element)
        tab_instance = []
        for i in range(0, len(liste_info), 2):
            string = liste_info[i + 1].split('.status.adb_port=')
            # print(f"{string=} ,  {liste_info[i]=}")

            string[1] = string[1].replace('"', "")
            string[0] = string[0][13:]

            string2 = liste_info[i].split('.display_name=')
            string2[1] = string2[1].replace('"', "")

            dico_instance = {
                'instance': str(string[0]),
                'port': string[1],
                'name': string2[1]
            }

            tab_instance.append(dico_instance)
        dico_instance = sort_by_instance(tab_instance)
        # print(tab_instance)
        return dico_instance

    def get_names(self, data):
        names = []
        for key in data.keys():
            for element in data[key]:
                if element == 'name':
                    names.append((len(names), data[key][element]))
        return names

    def get_current_instances(self, data):
        names = self.get_names(data)
        # print(f"{names = }")
        # print(names)
        instances_available = []
        for win in pyautogui.getAllWindows():
            for name in names:
                if win.title == name[1]:
                    instances_available.append(name)
        # print(instances_available)
        instances_available.sort(key=lambda x: x[0])
        # print(instances_available)
        return instances_available

    def get_list_instances(self):
        names = self.get_names(self.get_dic_instances())
        # print(f"{names = }")
        # print(names)
        instances_available = []
        # for win in pyautogui.getAllWindows():
        #     for name in names:
        #         if win.title == name[1]:
        #             instances_available.append(name)
        for name in names:
            instances_available.append(name)

        # print(instances_available)
        instances_available.sort(key=lambda x: x[0])
        # print(instances_available)
        return instances_available

    def find_window(self):
        hwnd = win32gui.FindWindow(None, self)
        return hwnd != 0

    def get_all_vms_running(self):
        return self.get_current_instances(self.get_dic_instances())

    def search(self, comparevalue):
        children = self.tree_view.get_children('')
        for child in children:
            values = self.tree_view.item(child, 'values')
            # print(type(comparevalue[0]), int(values[0]), str(comparevalue[1]) == str(values[1]))
            if comparevalue[0] == int(values[0]) and str(comparevalue[1]) == str(values[1]):
                return True
        return False

    def clear_all(self, treeview):
        for item in treeview.get_children():
            treeview.delete(item)

    def update_vms(self):
        # print(self.get_all_vms_running())
        # print("---")
        # print(self.get_list_instances())
        instances = self.get_all_vms_running()
        self.clear_all(self.tree_view)
        if instances == []:
            for item in self.tree_view.get_children():
                self.tree_view.delete(item)
        else:
            for item in self.tree_view.get_children():
                is_here = False
                for instance in instances:
                    if self.tree_view.item(item)['values'][0] == instance[0]:
                        is_here=True
                if not is_here:
                    self.tree_view.delete(item)
            for instance in instances:
                to_add = True
                for item in self.tree_view.get_children():
                    if self.tree_view.item(item)['values'][0] == instance[0]:
                        to_add = False
                if to_add:
                    self.tree_view.insert('', END, values=(instance[0], instance[1], ""))
        # for instance in instances:
        #     self.tree_view.insert('', END, values=(instance[0], instance[1], ""))
        if len(self.tree_view.get_children()) > 3:
            self.tree_view.configure(height=len(self.tree_view.get_children()))
        else:
            self.tree_view.configure(height=3)

def index_of_first(lst, sel):
    for i, v in enumerate(lst):
        if str(v[0]) == sel:
            return lst[i][1]
    return None


def find_window(window_title):
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        return False
    else:
        return True


def acces_default():
    try:
        from WorldTimeAPI import service as serv
        myclient = serv.Client('timezone')
        requests = {"area": "Europe", "location": "Paris"}
        response = myclient.get(**requests)
        # print(response)
        tab = response.datetime.split("T")
        tab = response.datetime.split("T")
        # print(tab)
        tmp = tab[1].split(".")
        tab[1] = tmp[0]
        if tab[0] > '2022-10-15':
            return False
        else:
            return True
    except:
        print("Something is wrong with WorldTimeAPI.. Please try again !")
        return True


def start():
    # print(f"{find_window('RoK Bot') = }")
    # print("wtf?")
    if (not find_window("RoK Bot0")) or acces_default():
        app = Main(-1)
        app.root.mainloop()


if __name__ == "__main__":
    start()
