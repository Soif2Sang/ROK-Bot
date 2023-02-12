import json
import os
import subprocess
import sys
from datetime import datetime, date
from tkinter import *
import UI_Main
import requests
from getmac import get_mac_address as gma
import customtkinter
import win32gui
from pyautogui import getAllWindows
from urllib3 import Retry, PoolManager

customtkinter.set_appearance_mode("dark")
if not os.path.exists("user_settings.json"):
    with open('user_settings.json', 'w') as f:
        json.dump({}, f, indent=2)
        print("User settings created")


def find_window(window_title):
    return any(window_title in element.title for element in getAllWindows())

def get_mac_address():
    return gma()

def mac_address_exists(dict):
    keys = ['mac1', 'mac2']
    mac_address = get_mac_address()
    for key in keys:
        if dict[key] == mac_address:
            return True
    return False

def main():
    def change_mac_address(id, key):
        try:
            url = f"https://rokbot-2e6f.restdb.io/rest/auth/{id}"
            body = json.dumps({f"{key}": get_mac_address()})
            headers = {
                'content-type': "application/json",
                'x-apikey': "632031befdc15b0265f17372",
                'cache-control': "no-cache"
            }
            response = requests.patch(url, data=body, headers=headers)
        except Exception:
            print("Error occured when patching the mac adress")
        # print(f" Change mac address {response.status_code=}")

    def acces(date='9999-12-30'):
        for i in range(5):
            try:
                retries = Retry(connect=5, read=2, redirect=5)
                http = PoolManager(retries=retries)
                response = http.request("GET", "http://worldtimeapi.org/api/timezone/Europe/Paris",
                                        headers={'Content-Type': 'application/json'}, retries=Retry(10))
                tab = json.loads(response.data.decode('utf-8'))['datetime'].split("T")
                tmp = tab[1].split(".")
                tab[1] = tmp[0]
                if tab[0] > date:
                    return False
                else:
                    return True
            except Exception as e:
                if i == 4:
                    print("Couldn't make connection, contact the admin")
                tmp = i
        return False

    def request_acess(username, password):
        try:
            url = "https://rokbot-2e6f.restdb.io/rest/auth"
            payload = json.dumps({'username': username, 'password': password})
            parameter = {"q": payload}
            headers = {
                'content-type': "application/json",
                'x-apikey': "632031befdc15b0265f17372",
                'cache-control': "no-cache"
            }
            response = requests.request("GET", url, params=parameter, headers=headers)
            data = response.json()
            # print(data)
            if data == []:
                # print("data == []")
                return False

            data = data[0]
            if data['abo'] is None:
                return False
            heure = data['abo'].split("T")
            # print(heure)
            if not acces(heure[0]):
                print("Subscription expired")
                return False
            if not mac_address_exists(data):
                if data['mac1'] == '':
                    change_mac_address(data['_id'], 'mac1')
                elif data['mac2'] == '':
                    change_mac_address(data['_id'], 'mac2')
                else:
                    print("None of the mac addresses match the mac address..")
                    return False
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            data["user"] = {'username': username, 'password': password}
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))
            root.destroy()
            today = date.today()
            heures = heure[0].split('-')
            future = date(int(heures[0]),int(heures[1]) ,int(heures[2]) )
            diff = future - today
            return UI_Main.Main(diff.days)
        except Exception as e:
            # print(e)
            print("Problem occured while trying to connect")
            sys.exit(1)

    root = Tk()
    root.resizable(False, False)
    root.title('GEM 1.0')
    root.iconbitmap('./Item_Gem.ico')
    usernameL = customtkinter.CTkLabel(root, text="Username : ")
    usernameE = customtkinter.CTkEntry(root)
    usernameL.grid(row=0, column=0, sticky='ew',padx=(40, 0),pady=(20,0))
    usernameE.grid(row=0, column=1,padx=(0, 40),pady=(20,0), sticky='ew')

    passwordL = customtkinter.CTkLabel(root, text="Password : ")
    passwordE = customtkinter.CTkEntry(root)
    passwordL.grid(row=1, column=0, sticky='ew',padx=(40, 5))
    passwordE.grid(row=1, column=1, sticky='ew',padx=(0, 40))

    def test():
        request_acess(usernameE.get(), passwordE.get())

    login_button = customtkinter.CTkButton(root, text="Login", command=test, corner_radius=4, fg_color="white",
                                           border_color="grey", border_width=1, text_color="black")
    login_button.grid(row=3, column=0, sticky='nswe', padx=60, columnspan=2,pady=(5,20))

    #
    # register_button = Button(root, text="Register", command=login)
    # register_button.grid(row=3, column = 1,sticky = 'nswe', padx=5, pady=5)

    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    root.geometry(f"{width}x{height}")
    root.mainloop()


def change_mac_address(id, key):
    try:
        url = f"https://rokbot-2e6f.restdb.io/rest/auth/{id}"
        body = json.dumps({f"{key}": get_mac_address()})
        headers = {
            'content-type': "application/json",
            'x-apikey': "632031befdc15b0265f17372",
            'cache-control': "no-cache"
        }
        response = requests.patch(url, data=body, headers=headers)
    except Exception:
        print("Error occured when patching the mac adress")
    # print(f" Change mac address {response.status_code=}")


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
            # if tab[0] > date:
            #     return False
            # else:
            #     return True

            retries = Retry(connect=5, read=2, redirect=5)
            http = PoolManager(retries=retries)
            response = http.request("GET", "http://worldtimeapi.org/api/timezone/Europe/Paris",
                                    headers={'Content-Type': 'application/json'}, retries=Retry(10))
            tab = json.loads(response.data.decode('utf-8'))['datetime'].split("T")
            # # print(tab)
            tmp = tab[1].split(".")
            tab[1] = tmp[0]
            # print(tmp, tab[0])
            if tab[0] > date:
                return False
            else:
                return True
        except:
            if i == 4:
                print("Couldn't make connection with worldtimeapi, contact the admin")
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
            return main()

        data = data[0]
        heure = data['abo'].split("T")
        # print(heure)
        if not acces(heure[0]):
            return main()
        if not mac_address_exists(data):
            # print(f"{mac_address_exists(data)=}")
            if data['mac1'] == '':
                change_mac_address(data['_id'], 'mac1')
            elif data['mac2'] == '':
                change_mac_address(data['_id'], 'mac2')

        # print(f"{data=}")
        response = requests.request("GET", url, params=parameter, headers=headers)
        # print(f"{response.json()=}")
        data = response.json()[0]
        # print(f"{mac_address_exists(data) = }")

        if mac_address_exists(data):
            with open('user_settings.json') as config_file:
                data = json.load(config_file)
            data["user"] = {'username': username, 'password': password}
            with open('user_settings.json', 'w') as config_file:
                config_file.write(json.dumps(data, indent=2))
            # print(f"{data = }")
            today = date.today()
            heures = heure[0].split('-')
            future = date(int(heures[0]),int(heures[1]) ,int(heures[2]) )
            diff = future - today
            return UI_Main.Main(diff.days)
        else:
            return main()
    except Exception:
        print("Problem occured while trying to connect")
        sys.exit(1)


if __name__ == "__main__":
    # Start server
    with open('path.json') as config_file:
        path = json.load(config_file)
    cmd = f"{path['HD-Player'].replace('Player','Adb')} start-server"
    subprocess.Popen(cmd)

    print("================================================================================================")
    print("""\
       ___  ____   ____   ___   __ __      ______  __ __    ___      ____    ___   ______      __ 
      /  _]|    \ |    | /   \ |  |  |    |      ||  |  |  /  _]    |    \  /   \ |      |    |  |
     /  [_ |  _  ||__  ||     ||  |  |    |      ||  |  | /  [_     |  o  )|     ||      |    |  |
    |    _]|  |  |__|  ||  O  ||  ~  |    |_|  |_||  _  ||    _]    |     ||  O  ||_|  |_|    |__|
    |   [_ |  |  /  |  ||     ||___, |      |  |  |  |  ||   [_     |  O  ||     |  |  |       __ 
    |     ||  |  \  `  ||     ||     |      |  |  |  |  ||     |    |     ||     |  |  |      |  |
    |_____||__|__|\____| \___/ |____/       |__|  |__|__||_____|    |_____| \___/   |__|      |__|

    """)
    print("================================================================================================")
    print("Bot is starting..")
    if not os.path.exists("user_settings.json"):
        with open('user_settings.json', 'w') as f:
            json.dump({}, f, indent=2)
            print("User settings created")

    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    if not find_window("RoK Bot -"):
        if "user" in data:
            if data["user"]["username"]!="":
                request_acess(data['user']["username"], data['user']["password"])
            else:
                main()
        else:
            main()
