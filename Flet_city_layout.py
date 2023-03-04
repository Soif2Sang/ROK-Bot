import base64
import json
import traceback
from io import BytesIO

import flet as ft
from multiprocessing import Process

from PIL import Image

global sel,profile

def main(page:ft.Page):
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    page.window_width = 830
    page.window_height = 430
    page.current_build = None

    buttons = {
        "infantry_camp":0,
        "cavalry_camp":1,
        "archery_camp":2,
        "siege_camp":3,
        "hospital":4,
        "scout_camp":5,
        "city_transfer":6,
    }
    def setCurrentBuild(param:str):
        page.current_build = param
        for element in page.column2.controls:
            element.color = "blue"
        page.column2.controls[buttons[param]].color = "red"
        page.update()

    def close_banner(e):
        page.banner.open = False
        page.update()

    def pop_banner(text):
        page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=close_banner),
            ],
            open=True
        )
        page.update()

    def on_tap_update(e:ft.ControlEvent):
        print(e.local_x*2, e.local_y*2)

        try:
            print(data[str(sel)]['schedules'][str(profile)])
            data[str(sel)]['schedules'][str(profile)][page.current_build] = (int(e.local_x*2), int(e.local_y*2))
            pop_banner(f"{page.current_build} successfully set")
        except Exception as e:
            traceback.print_exc()
            return
        with open('user_settings.json', 'w') as config_file:
            config_file.write(json.dumps(data, indent=2))

    c = ft.Container(bgcolor=ft.colors.RED,left=0, top=0, image_src="city.png",height=720/2,width=1280/2)

    gd1 = ft.GestureDetector(
        drag_interval=10,
        top=0,
        left=0,
        on_tap_down=on_tap_update,
        content=ft.Container(width=1280/2, height=720/2),
    )
    page.column1 = ft.Column()
    page.column2 = ft.Column()
    page.row = ft.Row(controls=[page.column1,page.column2])
    page.column1.controls=[ft.Stack([c, gd1], width=1280/2, height=720/2)]
    page.add(page.row)


    page.column2.controls.extend([
        ft.ElevatedButton(text="Set Infantry camp", on_click=lambda _:setCurrentBuild("infantry_camp")),
    ft.ElevatedButton(text="Set Cavalry camp", on_click=lambda _: setCurrentBuild("cavalry_camp"))
    ,ft.ElevatedButton(text="Set Archer camp", on_click=lambda _: setCurrentBuild("archery_camp"))
    ,ft.ElevatedButton(text="Set Siege camp", on_click=lambda _: setCurrentBuild("siege_camp"))
    ,ft.ElevatedButton(text="Set Hospital", on_click=lambda _: setCurrentBuild("hospital"))
    , ft.ElevatedButton(text="Set Scout camp", on_click=lambda _: setCurrentBuild("scout_camp"))
    , ft.ElevatedButton(text="Set City to transfer", on_click=lambda _: setCurrentBuild("city_transfer"))
    ]
    )

    page.update()

def start(sel_param="1",profile_param="1"):
    global sel,profile
    sel = sel_param
    profile = profile_param
    ft.app(target=main)

if __name__ == "__main__":
    start()