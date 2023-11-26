import flet as ft
import requests

from utils.auth import selfApi
from utils.functions import getchecksum

SELLER_KEY = "85f1f39bf61d1a04394b216f3efe4215"
keyauthapp = selfApi(
    name="RokbdBR",
    ownerid="7oofxdj8uH",
    secret="6d15b7ee5e7312238105efd4b648535835dc1ce5f4250fe2dc82910db43147b6",
    version="2.0",
    hash_to_check=getchecksum(),
)


class CreateUser(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = ft.TextField(label="username")
        self.password = ft.TextField(
            label="password (only if need to create the account)"
        )
        self.days = ft.Dropdown(
            options=[
                ft.dropdown.Option(text="2 Days", key=2),
                ft.dropdown.Option(text="30 Days", key=30),
            ],
        )

        self.button = ft.FilledButton(text="Create/Extend User", on_click=self.generate)

        self.reset_button = ft.FilledButton(
            text="Reset hwid", on_click=self.delete_hwid
        )

        self.controls.extend(
            [self.username, self.password, self.days, self.button, self.reset_button]
        )

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
            print(
                self.create_user(
                    self.username.value, self.password.value, self.days.value
                )
            )

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
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=extend&user={username}&sub=default&expiry={duration}&activeOnly=0"

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


def main(page: ft.Page):
    page.user = CreateUser()
    page.add(page.user)
    page.progressbar = ft.ProgressBar(visible=False)
    page.add(page.progressbar)
    page.randomtext = ft.Text()
    page.add(page.randomtext)

    page.update()


if __name__ == "__main__":
    ft.app(target=main)
