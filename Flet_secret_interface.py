import json
import shutil
import threading
from os.path import exists
from time import sleep

import flet as ft
import pyautogui

from Flet_Logger import Logger, LoggerUpgrade
from Flet_TileManager import TileManager, NavigationBar
from Flet_TileManager_upgrade import TileManagerUpgrade
from Task import Task
from Task_runner import TaskRunner

color_bank ={
    1:"#3b8ed0",
    2:"#ba4543",
    3:"#dec433"
}


def Main(page: ft.Page, days=950):
    page.title = f"Rok Bot - {days} Days left"
    page.frames = {}
    page.window_width = 400
    page.tile_manager = TileManagerUpgrade(page)
    page.add(page.tile_manager)
    page.add(ft.Divider())
    page.update()
    # page.tile_manager.refresh()
    page.add(page.tile_manager.start_bar)
    page.tile_manager.start_bar.tile_manager = page.tile_manager
    # print(page.logger)
    page.logger = LoggerUpgrade(page)
    page.add(page.logger)
    page.update()

if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
