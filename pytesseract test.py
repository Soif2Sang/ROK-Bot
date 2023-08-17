import flet as ft
from flet_route import path, Routing
from random import randint
from time import sleep
import threading


def index(page: ft.Page, params, basket):
    return ft.View("/", controls=page.controls, )


def new_page(page: ft.Page, params, basket):
    return ft.View("/newpage", controls=[
        ft.Text(
            "New Page",
        ),
        ft.TextButton(
            text="Go to new page",
            on_click=lambda e: page.go("/")
        )

    ],
                   )


def main(page: ft.Page):
    a_text_that_needs_updates = ft.Text(value=f"Unchanged")
    page.add(a_text_that_needs_updates)

    page.add(
        ft.TextButton(
            text="Go to new page",
            on_click=lambda e: page.go("/newpage")
        )
    )

    page.app_routes = [path(
        url="/",
        clear=True,
        view=index
    ), path(
        url="/newpage",
        clear=True,
        view=new_page)]

    page.routing = Routing(
        page=page,  # Here you have to pass the page. Which will be found as a parameter in all your views
        app_routes=page.app_routes,
        # Here a list has to be passed in which we have defined app routing like app_routes
    )

    def update_text():
        a_text_that_needs_updates.value = f"Updated {randint(0, 100)}"
        page.update()
        sleep(1)
        return update_text()

    threading.Thread(target=update_text).start()


if __name__ == "__main__":
    ft.app(target=main)