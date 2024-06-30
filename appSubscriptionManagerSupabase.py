import json
import logging
from datetime import datetime

logging.basicConfig(level=logging.ERROR)
import flet as ft
import requests

from utils.constants import VERSION_TYPE
from utils.supabase_auth import NoSubscriptionFound, SupabaseClient

supabaseClient = SupabaseClient()


class CreateUser(ft.Column):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.username = ft.TextField(label="email")
        self.password = ft.TextField(label="password(6 chars min) (only if need to create the account)")
        self.days = ft.Dropdown(
            options=[
                ft.dropdown.Option(text="2 Days", key=2),
                ft.dropdown.Option(text="30 Days", key=30),
            ],
            autofocus=True,
        )

        self.button = ft.FilledButton(text="Create/Extend User", on_click=self.generate)

        self.controls.append(
            ft.Container(margin=ft.margin.only(top=10), content=ft.Column([self.username, self.password, self.days, self.button]))
        )

    def submit(self, e):
        return

    def generate(self, e):
        if not self.username.value or not self.days.value:
            return

        if self.password.value and len(self.password.value) < 6:
            return

        self.page.progressbar.visible = True
        self.page.randomtext.value = ""
        self.page.update()

        try:
            supabaseClient.login("brazil@manager.com", "brazil@manager.com")
            subscriptions = supabaseClient.getSubscriptions()

            if not subscriptions:
                raise NoSubscriptionFound()
        except:
            self.page.progressbar.visible = False
            self.page.randomtext.value = "You are not authorized to use the app."
            self.page.update()

            return

        if self.username.value and not self.password.value:
            data, count = supabaseClient.client.table("users").select("*").eq("email", self.username.value).execute()
            if not data[1]:
                self.page.progressbar.visible = False
                self.page.randomtext.value = "User not found"
                self.page.update()
                return

        if self.password.value:
            supabaseClient.client.auth.sign_up(
                {"email": self.username.value.strip().lower(), "password": self.password.value.strip().lower()}
            )
            supabaseClient.client.auth.sign_out()

            supabaseClient.login("brazil@manager.com", "brazil@manager.com")

            supabaseClient.client.table("users").update({"version_type": VERSION_TYPE}).eq("email", self.username.value).execute()
            supabaseClient.client.table("log").insert({"content": f"User {self.username.value} created."}).execute()

        data, count = supabaseClient.client.table("users").select("*").eq("email", self.username.value.strip().lower()).execute()
        data = data[1]

        supabaseClient.client.rpc(
            "create_subscription", {"user_id": data[0]["user_id"], "tier": "tier1", "days": self.days.value}
        ).execute()

        supabaseClient.client.table("log").insert({"content": f"{self.username.value} got extended by {self.days.value}."}).execute()
        self.page.progressbar.visible = False
        self.page.randomtext.value = "User created/extended"

        self.page.update()


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
    page.window.height = 500
    page.window.width = 500
    page.user = CreateUser(col=4)
    page.progressbar = ft.ProgressBar(visible=False)
    page.randomtext = ft.Text()
    # version = supabaseClient.getUpdates()
    # version = version[-1]
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
                # ft.Tab(text="Update Version", content=ModifyVersion(version)),
                # ft.Tab(text="Announcement", content=ModifyMessage(message)),
                # ft.Tab(text="PM", content=SendPersonalMessage()),
            ],
            height=400,
        ),
    )
    page.add(page.progressbar)
    page.add(page.randomtext)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
