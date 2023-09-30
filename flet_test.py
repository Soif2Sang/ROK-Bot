import flet as ft
import os


def main(page: ft.Page):
    def check_text_fields(e):
        username_value = len(username.value)
        password_value = len(password.value)

        if username_value >= 3 and password_value >= 3:
            login.disabled = False
        else:
            login.disabled = True

        # Update the page after changing the login button's disabled attribute
        page.update()

    username = ft.TextField(value="")
    password = ft.TextField(value="")

    login = ft.FilledButton(disabled=True)

    # Assign the on_change callback function to the text fields
    username.on_change = check_text_fields
    password.on_change = check_text_fields

    # Add the elements to the page
    page.add(username)
    page.add(password)
    page.add(login)

    # Initial page update
    page.update()


if __name__ == "__main__":
    ft.app(main)
