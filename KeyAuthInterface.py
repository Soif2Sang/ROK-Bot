import flet as ft
import requests
from tiles.handler.tile_handler import TileHandler

SELLER_KEY = "f6386c16787e0eb51b24d168205267e6"


def empty(value):
    return value == "" or value is None


def main(page: ft.Page):
    page.title = "Subscription Manager 1999 Days left "
    page.window.width = 340
    page.window.height = 350
    page.UPGRADE = False
    page.add(TileHandler(page))

    def verifyUsername():
        if empty(username.value):
            username.helper_text = "Username is empty !"
            username.error_text = "Username is empty !"
            page.update()
            return False
        username.helper_text = ""
        username.error_text = ""
        page.update()
        return True

    def verifyPassword():
        if empty(password.value):
            password.helper_text = "Password is empty !"
            password.error_text = "Password is empty !"
            page.update()
            return False
        password.helper_text = ""
        password.error_text = ""
        page.update()
        return True

    def verifyDuration():
        if empty(subscription.value):
            subscription.helper_text = "Duration is empty !"
            subscription.error_text = "Duration is empty !"
            page.update()
            return False
        subscription.helper_text = ""
        subscription.error_text = ""
        page.update()
        return True

    def generate(e):
        if not verifyUsername():
            return
        if verify(username.value):
            if not verifyDuration():
                return
            print(extend_user(username.value, subscription.value))
        else:
            if not verifyDuration() or not verifyPassword():
                return
            print(create_user(username.value, password.value, subscription.value))

    def verify(username):
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=verifyuser&user={username}"

        headers = {"accept": "application/json"}

        response = requests.get(url, headers=headers)

        print(response.text)
        return response.json()["success"]

    def create_user(username, password, duration):
        url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=adduser&user={username}&sub=default&expiry={duration}&pass={password}"

        headers = {"accept": "application/json"}
        progressbar.visible = True
        randomtext.value = ""
        page.update()

        response = requests.get(url, headers=headers)

        progressbar.visible = False
        page.update()

        print(response.text)
        randomtext.value = response.json()["message"]

        if response.json()["success"]:
            randomtext.color = "green"
        else:
            randomtext.color = "red"
        page.update()
        return response.json()

    def delete_hwid(
        e,
    ):
        for i in range(1, 3):
            url = f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=deluservar&user={username.value}&var=HWID{i}"

            headers = {"accept": "application/json"}

            progressbar.visible = True
            randomtext.value = ""

            page.update()

            response = requests.get(url, headers=headers)

            progressbar.visible = False
            page.update()

            print(response.text)
            randomtext.value = response.json()["message"]

            if response.json()["success"]:
                randomtext.color = "green"
            else:
                randomtext.color = "red"
            page.update()

    def extend_user(username, duration):
        url = (
            f"https://keyauth.win/api/seller/?sellerkey={SELLER_KEY}&type=extend&user={username}&sub=default&expiry={duration}&activeOnly=0"
        )

        headers = {"accept": "application/json"}

        progressbar.visible = True
        randomtext.value = ""

        page.update()

        response = requests.get(url, headers=headers)

        progressbar.visible = False
        page.update()

        print(response.text)
        randomtext.value = response.json()["message"]

        if response.json()["success"]:
            randomtext.color = "green"
        else:
            randomtext.color = "red"
        page.update()
        return response.json()

    username = ft.TextField(label="Username")
    password = ft.TextField(label="Password")
    subscription = ft.TextField(label="Subscription")

    generate = ft.OutlinedButton(text="Generate", on_click=generate)
    reset_hwid = ft.OutlinedButton(text="Reset HWID", on_click=delete_hwid)
    randomtext = ft.Text(value="")
    progressbar = ft.ProgressBar(visible=False)

    database = ft.Column(
        controls=[
            username,
            password,
            subscription,
            ft.Row(controls=[generate, reset_hwid]),
            progressbar,
            randomtext,
        ]
    )

    channel = ft.TextField(label="Channel")
    message = ft.TextField(label="Message", multiline=True, min_lines=5)
    message_sender = ft.Column(controls=[channel, message])

    page.add(ft.Row(controls=[database]))


if __name__ == "__main__":
    ft.app(main)
