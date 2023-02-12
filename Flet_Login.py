import asyncio
import json
import os
import subprocess
import threading
from datetime import date
from time import sleep

import flet as ft
import requests
from pyautogui import getAllWindows
from getmac import get_mac_address as gma
from urllib3 import Retry, PoolManager

import Flet_main_interface


def update_user_info(password, username):
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    data["user"] = {'username': username, 'password': password}
    with open('user_settings.json', 'w') as config_file:
        config_file.write(json.dumps(data, indent=2))


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


def is_date_valid(date='9999-12-30'):
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
    return False


class LoginButton(ft.FilledButton):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def is_str_valid(self, username, password):
        for element in ['#', "$", "&", "|", "\0",
                        "\n",
                        "\r",
                        '\'',
                        "'",
                        '"',
                        "\Z"]:
            if element in username or element in password:
                return False
        return True

    def login_schedule(self, username, password):
        print("Login schedule...")
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            exit(1)
            main(self.page)
            return False
        try:
            data = self.login_to_bd(password, username)
            # print(data)
            heure = self.is_data_valid(data)
            if heure == 0:
                self.page.clean()
                main(self.page)
                return False
            else:
                sleep(10)
                return self.login_schedule(username, password)
        except Exception as e:
            # print(e)
            self.pop_banner("Problem occurred, please try again")
            print("Problem occured while trying to connect")
            self.page.clean()
            main(self.page)
            exit(1)

    def login(self, e, username=None, password=None):
        print("Trying to login...")
        if username is None and password is None:
            username = self.page.controls[0].value
            password = self.page.controls[1].value
        if not self.is_str_valid(username, password):
            self.pop_banner("Illegal characters..")
            return False
        try:
            data = self.login_to_bd(password, username)
            # print(data)
            heure = self.is_data_valid(data)
            if heure == 0:
                return False
            update_user_info(password, username)
            today = date.today()
            heures = heure[0].split('-')
            future = date(int(heures[0]), int(heures[1]), int(heures[2]))
            diff = future - today
            print("Login successful")
            self.page.clean()
            self.page.window_width = 400
            self.page.window_height = 700
            Flet_main_interface.Main(self.page)
            threading.Thread(self.login_schedule(username, password))
        except Exception as e:
            # print(e)
            self.pop_banner("Problem occurred, please try again")
            print("Problem occured while trying to connect")
            self.page.window_close()
            exit(1)

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def pop_banner(self, text):
        self.page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=self.close_banner),
            ],
            open=True
        )
        self.page.update()

    def is_data_valid(self, data):
        if data == {}:
            return 0
        if data['abo'] is None:
            return 0
        heure = data['abo'].split("T")
        if not is_date_valid(heure[0]):
            self.pop_banner("Subscription expired")
            print("Subscription expired")
            return 0
        if not mac_address_exists(data):
            if data['mac1'] == '':
                change_mac_address(data['_id'], 'mac1')
            elif data['mac2'] == '':
                change_mac_address(data['_id'], 'mac2')
            else:
                self.pop_banner("The account seems to be connected on too much machines, contact the administrator")
                print("None of the mac addresses match the mac address..")
                return 0
        return heure

    def login_to_bd(self, password, username):
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
            return data[0]
        except:
            return {}


def main(page: ft.Page):
    if not os.path.exists("user_settings.json"):
        with open('user_settings.json', 'w') as f:
            json.dump({}, f, indent=2)
            print("User settings created")
    with open('user_settings.json') as config_file:
        data = json.load(config_file)

    page.window_width = 330
    page.window_height = 330
    page.add(ft.TextField(label="Username", width=300, value=data.get("user",{}).get("username","")))
    page.add(ft.TextField(label="Password", password=True, can_reveal_password=True, width=300,value=data.get("user",{}).get("password","")))
    login_button = LoginButton(text="Login", width=100)
    login_button.on_click = login_button.login
    page.add(login_button)
    page.update()
    with open('path.json') as config_file:
        path = json.load(config_file)
    cmd = f"{path['HD-Player'].replace('Player', 'Adb')} start-server"
    subprocess.Popen(cmd)
    print("Bot is starting..")
    if not find_window("RoK Bot -"):
        if "user" in data:
            if data["user"]["username"] != "":
                login_button.login(None, data['user']["username"], data['user']["password"])


if __name__ == "__main__":
    ft.app(target=main)
