import flet as ft
import os

def main(page: ft.Page):
    pass

if __name__ == "__main__":
    for name, value in os.environ.items():
        print("{0}: {1}".format(name, value))
    ft.app(main)

    for name, value in os.environ.items():
        print("{0}: {1}".format(name, value))