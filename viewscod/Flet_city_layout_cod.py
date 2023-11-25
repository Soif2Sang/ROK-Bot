import traceback

import flet as ft

from utils.functions import FileSingleton

global sel,profile

def main(page:ft.Page):
    page.FileSingleton = FileSingleton()
    data = page.FileSingleton.get_data()
    page.window_width = 830
    page.window_height = 430
    page.current_build = None

    buttons = {
        "infantry_camp":0,
        "cavalry_camp":1,
        "archery_camp":2,
        "siege_camp":3,
        # "hospital":4,
        "scout_camp":4,
        "research_center":5
        # "city_transfer":6,
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
        data = page.FileSingleton.get_data()
        print(data[str(sel)]['schedules'][str(profile)][page.current_build])
        try:
            print(data[str(sel)]['schedules'][str(profile)])
            data[str(sel)]['schedules'][str(profile)][page.current_build] = (int(e.local_x*2), int(e.local_y*2))
            pop_banner(f"{page.current_build} successfully set")
        except Exception as e:
            traceback.print_exc()
            return
        page.FileSingleton.write_data(data)
        data = page.FileSingleton.get_data()
        print(data[str(sel)]['schedules'][str(profile)][page.current_build])

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
    # ,ft.ElevatedButton(text="Set Hospital", on_click=lambda _: setCurrentBuild("hospital"))
    , ft.ElevatedButton(text="Set Scout camp", on_click=lambda _: setCurrentBuild("scout_camp"))
    , ft.ElevatedButton(text="Set Academy", on_click=lambda _: setCurrentBuild("research_center"))

    # , ft.ElevatedButton(text="Set City to transfer", on_click=lambda _: setCurrentBuild("city_transfer"))
    ]
    )

    page.update()

def main2(sel,profile):
    global  column2, current_build

    data = FileSingleton.get_data()

    buttons = {
        "infantry_camp":0,
        "cavalry_camp":1,
        "archery_camp":2,
        "siege_camp":3,
        # "hospital":4,
        "scout_camp":4,
        "research_center":5
        # "city_transfer":6,
    }
    def setCurrentBuild(param:str):
        global current_build
        current_build = param
        for element in column2.controls:
            element.color = "blue"
        column2.controls[buttons[param]].color = "red"
        column2.page.update()

    def on_tap_update(e:ft.ControlEvent):
        print(e.local_x*2, e.local_y*2)
        try:
            print(data[str(sel)]['schedules'][str(profile)])
            data[str(sel)]['schedules'][str(profile)][current_build] = (int(e.local_x*2), int(e.local_y*2))
        except Exception as e:
            traceback.print_exc()
            return
        column2.page.FileSingleton.write_data(data)

    c = ft.Container(bgcolor=ft.colors.RED,left=0, top=0, image_src="city.png",height=720/2,width=1280/2)

    gd1 = ft.GestureDetector(
        drag_interval=10,
        top=0,
        left=0,
        on_tap_down=on_tap_update,
        content=ft.Container(width=1280/2, height=720/2),
    )
    column1 = ft.Column()
    column2 = ft.Column()
    row = ft.Row(controls=[column1,column2])
    column1.controls=[ft.Stack([c, gd1], width=1280/2, height=720/2)]


    column2.controls.extend([
        ft.ElevatedButton(text="Set Infantry camp", on_click=lambda _: setCurrentBuild("infantry_camp")),
        ft.ElevatedButton(text="Set Cavalry camp", on_click=lambda _: setCurrentBuild("cavalry_camp"))
        , ft.ElevatedButton(text="Set Archer camp", on_click=lambda _: setCurrentBuild("archery_camp"))
        , ft.ElevatedButton(text="Set Siege camp", on_click=lambda _: setCurrentBuild("siege_camp"))
        , ft.ElevatedButton(text="Set Scout camp", on_click=lambda _: setCurrentBuild("scout_camp"))
        , ft.ElevatedButton(text="Set Academy", on_click=lambda _: setCurrentBuild("research_center"))
    ]
    )

    return row

class CityPlacement(ft.Container):
    buttons = {
        "infantry_camp":0,
        "cavalry_camp":1,
        "archery_camp":2,
        "siege_camp":3,
        "scout_camp":4,
        "research_center":5
    }
    def __init__(self, instance, profile, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.profile = profile
        self.current_build =  None
        self.data = self.page.FileSingleton.get_data()

        self.main_container = ft.Container(bgcolor=ft.colors.RED, left=0, top=0, image_src="city.png", height=720 / 2, width=1280 / 2)

        self.gesture = ft.GestureDetector(
            drag_interval=10,
            top=0,
            left=0,
            on_tap_down=self.on_tap_update,
            content=ft.Container(width=1280 / 2, height=720 / 2),
        )
        self.clickable_city = ft.Column()
        self.clickable_city.controls = [ft.Stack([self.main_container, self.gesture], width=1280 / 2, height=720 / 2)]
        self.buttons = ft.Column()
        self.content = ft.Row(controls=[self.clickable_city, self.buttons])

        self.buttons.controls.extend([
            ft.ElevatedButton(text="Set Infantry camp", on_click=lambda _: self.setCurrentBuild("infantry_camp")),
            ft.ElevatedButton(text="Set Cavalry camp", on_click=lambda _: self.setCurrentBuild("cavalry_camp"))
            , ft.ElevatedButton(text="Set Archer camp", on_click=lambda _: self.setCurrentBuild("archery_camp"))
            , ft.ElevatedButton(text="Set Siege camp", on_click=lambda _: self.setCurrentBuild("siege_camp"))
            , ft.ElevatedButton(text="Set Scout camp", on_click=lambda _: self.setCurrentBuild("scout_camp"))
            , ft.ElevatedButton(text="Set City to transfer", on_click=lambda _: self.setCurrentBuild("research_center"))
        ]
        )
        for co in ["infantry_camp", "cavalry_camp", "archery_camp", "siege_camp", "scout_camp",
                   "research_center"]:
            if self.data[str(self.instance)]["schedules"][str(self.profile)][co]:
                if "✓" not in self.buttons.controls[self.button[co]].text:
                    self.buttons.controls[self.button[co]].text = self.buttons.controls[self.button[co]].text + " ✓"
    def updateButtons(self):
        for co in ["infantry_camp","cavalry_camp","archery_camp","siege_camp","scout_camp","research_center"]:
            if self.data[str(self.instance)]["schedules"][str(self.profile)][co]:
                if "✓" not in self.buttons.controls[self.button[co]].text:
                    self.buttons.controls[self.button[co]].text = self.buttons.controls[self.button[co]].text + " ✓"
        self.page.update()
    def setCurrentBuild(self,param:str):
        self.current_build = param
        for element in self.buttons.controls:
            element.color = "blue"
        self.buttons.controls[self.button[param]].color = "red"
        self.buttons.page.update()

    def on_tap_update(self,e:ft.ControlEvent):
        print(e.local_x*2, e.local_y*2)
        try:
            self.data[str(self.instance)]['schedules'][str(self.profile)][self.current_build] = (int(e.local_x*2), int(e.local_y*2))
            self.updateButtons()
        except Exception as e:
            traceback.print_exc()
            return
        for element in self.buttons.controls:
            element.color = "blue"
        self.buttons.page.update()
        self.page.FileSingleton.write_data(self.data)
def start(sel_param="1",profile_param="1"):
    global sel,profile,data
    sel = sel_param
    profile = profile_param
    ft.app(target=main)

if __name__ == "__main__":
    start()