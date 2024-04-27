import json
from datetime import datetime

import flet as ft
import requests

from utils.auth import selfApi
from utils.constants import brezilian_name, brezilian_secret, global_name, global_secret
from utils.functions import getchecksum

SELLER_KEY = "f6386c16787e0eb51b24d168205267e6"

keyauthapp = selfApi(name=global_name, ownerid="7oofxdj8uH", secret=global_secret, version="2.0", hash_to_check=getchecksum())


SELLER_KEY = "85f1f39bf61d1a04394b216f3efe4215"

keyauthapp = selfApi(name=brezilian_name, ownerid="7oofxdj8uH", secret=brezilian_secret, version="2.0", hash_to_check=getchecksum())


class CreateUser(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = ft.TextField(label="username")
        self.password = ft.TextField(label="password (only if need to create the account)")
        self.days = ft.Dropdown(
            options=[
                ft.dropdown.Option(text="2 Days", key=2),
                ft.dropdown.Option(text="30 Days", key=30),
            ],
            autofocus=True,
        )

        self.button = ft.FilledButton(text="Create/Extend User", on_click=self.generate)

        self.reset_button = ft.FilledButton(text="Reset hwid", on_click=self.delete_hwid)

        self.controls.extend([self.username, self.password, self.days, self.button, self.reset_button])

    def submit(self, e):
        return

    def generate(self, e):
        if not self.username.value or not self.days.value:
            return
        if self.verify(self.username.value):
            print(self.extend_user(self.username.value, self.days.value))
        else:
            if not self.password.value:
                return
            print(self.create_user(self.username.value, self.password.value, self.days.value))

    def verify(self, username):
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=verifyuser&user={username}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(response.text)
        return response.json()["success"]

    def create_user(self, username, password, duration):
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=adduser&user={username}&sub=default&expiry={duration}&pass={password}"
        headers = {"accept": "application/json"}
        self.page.progressbar.visible = True
        self.page.randomtext.value = ""
        self.page.update()

        response = requests.get(url, headers=headers)

        self.page.progressbar.visible = False
        self.page.update()

        print(response.text)
        self.page.randomtext.value = response.json()["message"]

        if response.json()["success"]:
            self.page.randomtext.color = "green"
            keyauthapp.log(f"Created {username} with {duration} day(s).")
        else:
            self.page.randomtext.color = "red"
        self.page.update()
        return response.json()

    def delete_hwid(self, e):
        for i in range(1, 3):
            url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=deluservar&user={self.username.value}&var=HWID{i}"

            headers = {"accept": "application/json"}

            self.page.progressbar.visible = True
            self.page.randomtext.value = ""

            self.page.update()

            response = requests.get(url, headers=headers)

            self.page.progressbar.visible = False
            self.page.update()

            print(response.text)
            self.page.randomtext.value = response.json()["message"]

            if response.json()["success"]:
                self.page.randomtext.color = "green"
                keyauthapp.log(f"HWID reset for {self.username.value}.")

            else:
                self.page.randomtext.color = "red"
            self.page.update()

    def extend_user(self, username, duration):
        url = (
            f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=extend&user={username}&sub=default&expiry={duration}&activeOnly=0"
        )

        headers = {"accept": "application/json"}

        self.page.progressbar.visible = True
        self.page.randomtext.value = ""

        self.page.update()

        response = requests.get(url, headers=headers)

        self.page.progressbar.visible = False
        self.page.update()

        print(response.text)
        self.page.randomtext.value = response.json()["message"]

        if response.json()["success"]:
            self.page.randomtext.color = "green"
            keyauthapp.log(f"Extended {username} for {duration} day(s).")
        else:
            self.page.randomtext.color = "red"
        self.page.update()
        return response.json()


class ModifyVersion(ft.Column):
    def __init__(self, version, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            version_json = json.loads(version)
        except:
            version_json = {"version": "0", "force": True, "download_link": ""}

        self.txt_version = ft.TextField(value=version_json["version"], text_align=ft.TextAlign.RIGHT, width=100, label="Version")
        self.chk_force = ft.Checkbox(value=version_json["force"], label="Force update")
        self.txt_download_link = ft.TextField(value=version_json["download_link"], text_align=ft.TextAlign.LEFT, width=350)

        self.submit = ft.FilledButton("Submit", on_click=self.submit_click)

        self.controls = [self.txt_version, self.chk_force, self.txt_download_link, self.submit]

    def submit_click(self, e):
        version_data = {
            "version": self.txt_version.value.strip(),
            "force": self.chk_force.value,
            "download_link": self.txt_download_link.value.strip(),
        }

        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=editvar&varid=version&data={json.dumps(version_data)}"

        headers = {"accept": "application/json"}

        self.page.progressbar.visible = True
        self.page.randomtext.value = ""

        self.page.update()

        response = requests.get(url, headers=headers)

        self.page.progressbar.visible = False
        self.page.update()

        self.page.randomtext.value = response.json()["message"]
        print((response.json()))
        if response.json()["success"]:
            self.page.randomtext.color = "green"
        else:
            self.page.randomtext.color = "red"
        self.page.update()

        return response.json()


class ModifyMessage(ft.Column):
    def __init__(self, message, *args, **kwargs):
        super().__init__(*args, **kwargs)
        try:
            message_json = json.loads(message)
        except:
            message_json = {"message": "", "start": 1, "end": 1}
        print(message_json)
        self.txt_message = ft.TextField(value=message_json["message"], text_align=ft.TextAlign.LEFT, width=600, label="Message")

        self.date_start = ft.DatePicker(
            value=datetime.fromtimestamp(message_json["start"]), help_text=f"Start Date", on_change=self.submit_start
        )
        self.date_end = ft.DatePicker(value=datetime.fromtimestamp(message_json["end"]), help_text=f"End Date", on_change=self.submit_end)

        self.submit = ft.FilledButton("Submit", on_click=self.submit_click)

        self.controls = [
            self.txt_message,
            self.date_start,
            self.date_end,
            ft.ElevatedButton(
                f"Pick Start date {datetime.fromtimestamp(message_json['start']).strftime('%d/%m/%Y')}",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_start.pick_date(),
            ),
            ft.ElevatedButton(
                f"Pick End date {datetime.fromtimestamp(message_json['end']).strftime('%d/%m/%Y')}",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_end.pick_date(),
            ),
            self.submit,
        ]

    def submit_start(self, e):
        self.controls[-3].text = f'Pick Start date {self.date_start.value.strftime("%d/%m/%Y")}'
        self.update()

    def submit_end(self, e):
        self.controls[-2].text = f'Pick Start date {self.date_end.value.strftime("%d/%m/%Y")}'
        self.update()

    def submit_click(self, e):
        print(type(self.date_start.value))

        message_data = {
            "message": self.txt_message.value.strip(),
            "start": datetime.timestamp(self.date_start.value),
            "end": datetime.timestamp(self.date_end.value),
        }

        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=editvar&varid=message&data={json.dumps(message_data)}"

        headers = {"accept": "application/json"}

        self.page.progressbar.visible = True
        self.page.randomtext.value = ""

        self.page.update()

        response = requests.get(url, headers=headers)

        self.page.progressbar.visible = False
        self.page.update()

        self.page.randomtext.value = response.json()["message"]

        if response.json()["success"]:
            self.page.randomtext.color = "green"
        else:
            self.page.randomtext.color = "red"
        self.page.update()

        return response.json()


class SendPersonalMessage(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.txt_message = ft.TextField(text_align=ft.TextAlign.LEFT, width=600, label="Message")

        self.date_start = ft.DatePicker(help_text=f"Start Date", on_change=self.submit_start)
        self.date_end = ft.DatePicker(help_text=f"End Date", on_change=self.submit_end)

        self.submit = ft.FilledButton("Submit", on_click=self.submit_click)

        usernames = self.get_all_usernames()

        self.username_choice = ft.Dropdown()
        for username in usernames:
            self.username_choice.options.append(ft.dropdown.Option(username["username"]))

        self.controls = [
            self.txt_message,
            self.username_choice,
            self.date_start,
            self.date_end,
            ft.ElevatedButton(
                f"Pick Start date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_start.pick_date(),
            ),
            ft.ElevatedButton(
                f"Pick End date",
                icon=ft.icons.CALENDAR_MONTH,
                on_click=lambda _: self.date_end.pick_date(),
            ),
            self.submit,
        ]

    def submit_start(self, e):
        self.controls[-3].text = f'Pick Start date {self.date_start.value.strftime("%d/%m/%Y")}'
        self.update()

    def submit_end(self, e):
        self.controls[-2].text = f'Pick Start date {self.date_end.value.strftime("%d/%m/%Y")}'
        self.update()

    def submit_click(self, e):
        message_data = {
            "message": self.txt_message.value.strip(),
            "start": datetime.timestamp(self.date_start.value),
            "end": datetime.timestamp(self.date_end.value),
            "read": False,
        }

        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=setvar&user={self.username_choice.value}&var=message&data={json.dumps(message_data)}"
        headers = {"accept": "application/json"}

        self.page.progressbar.visible = True
        self.page.randomtext.value = ""

        self.page.update()

        response = requests.get(url, headers=headers)

        self.page.progressbar.visible = False
        self.page.update()

        self.page.randomtext.value = response.json()["message"]

        if response.json()["success"]:
            self.page.randomtext.color = "green"
        else:
            self.page.randomtext.color = "red"
        self.page.update()

        return response.json()

    def get_all_usernames(self):
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=fetchallusernames"
        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        return response.json()["usernames"]


def main(page: ft.Page):
    keyauthapp.login("maxence", "fe")
    version = keyauthapp.var("version")
    message = keyauthapp.var("message")
    page.window_height = 500
    page.window_width = 500
    page.user = CreateUser(col=4)
    page.progressbar = ft.ProgressBar(visible=False)
    page.randomtext = ft.Text()

    # page.add(ft.ResponsiveRow(
    #     controls=[
    #         page.user,
    #         ModifyVersion(version, col=4),
    #         ModifyMessage(message, col=4)
    #     ],
    #     spacing=10,
    #     expand=True,
    # ))

    page.add(
        ft.Tabs(
            tabs=[
                ft.Tab(text="Create User", content=page.user),
                ft.Tab(text="Update Version", content=ModifyVersion(version)),
                ft.Tab(text="Announcement", content=ModifyMessage(message)),
                ft.Tab(text="PM", content=SendPersonalMessage()),
            ],
            height=400,
        ),
    )
    page.add(page.progressbar)
    page.add(page.randomtext)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
