import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.update()

ft.app(target=main)