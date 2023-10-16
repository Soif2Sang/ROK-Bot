import base64
import traceback

import flet as ft
import flet_route

from utils.Task_utils import FileSingleton


class cityLayoutParam(flet_route.Params):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_index = None
        self.profile_index = None

def image_to_base64(image_byte):
    encoded_string = base64.b64encode(image_byte.read())
    return encoded_string.decode('utf-8')

def viewCityLayout(page: ft.Page, params: cityLayoutParam, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500
    image_byte = image_to_base64(
        page.tile_manager.tiles[str(params.instance_index)].runner.adb.get_curr_device_screen_img_bytesIO())

    def returnHome():
        page.window_width = 450
        page.window_height = 700
        page.go("/")

    return ft.View(
        f"/citylayout/{params.instance_index}/{params.profile_index}",
        controls=[
            ft.Container(
                bgcolor=ft.colors.SURFACE_VARIANT,
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: returnHome()),
                        ft.Text(value="Go back")
                    ]
                    )
            ),
            ft.Text(value="Click on the building button you wanna set, then click in the center of the building."),
            CityPlacement(image_byte, params.instance_index, params.profile_index)
        ]
    )


class CityPlacement(ft.Container):
    button = {
        "infantry_camp": 0,
        "cavalry_camp": 1,
        "archery_camp": 2,
        "siege_camp": 3,
        "hospital": 4,
        "scout_camp": 5,
        "city_transfer": 6,
        "city_hall_position": 7
    }

    def __init__(self, image64, instance, profile, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.profile = profile
        self.current_build = None
        self.FileSingleton = FileSingleton()
        self.data = self.FileSingleton.get_data()

        self.main_container = ft.Container(
            image_src_base64=image64,
            height=720 / 2,
            width=1280 / 2,
            on_click=self.on_tap_update
        )

        self.gesture = ft.GestureDetector(
            drag_interval=10,
            top=0,
            left=0,
            on_tap_down=self.on_tap_update,
            content=ft.Container(width=1280 / 2, height=720 / 2),
        )

        self.buttons = ft.ListView(height=720 / 2, expand=True, spacing=1)
        self.content = ft.Row(controls=[self.main_container, self.buttons])

        self.buttons.controls.extend([
            ft.ElevatedButton(text="Set Infantry camp", on_click=lambda _: self.setCurrentBuild("infantry_camp")),
            ft.ElevatedButton(text="Set Cavalry camp", on_click=lambda _: self.setCurrentBuild("cavalry_camp"))
            , ft.ElevatedButton(text="Set Archer camp", on_click=lambda _: self.setCurrentBuild("archery_camp"))
            , ft.ElevatedButton(text="Set Siege camp", on_click=lambda _: self.setCurrentBuild("siege_camp"))
            , ft.ElevatedButton(text="Set Hospital", on_click=lambda _: self.setCurrentBuild("hospital"))
            , ft.ElevatedButton(text="Set Scout camp", on_click=lambda _: self.setCurrentBuild("scout_camp"))
            , ft.ElevatedButton(text="Set City to transfer", on_click=lambda _: self.setCurrentBuild("city_transfer"))
            , ft.ElevatedButton(text="Set City Hall", on_click=lambda _: self.setCurrentBuild("city_hall_position"))
        ]
        )
        for co in ["infantry_camp", "cavalry_camp", "archery_camp", "siege_camp", "hospital", "scout_camp",
                   "city_transfer", "city_hall_position"]:
            if self.data[str(self.instance)]["schedules"][str(self.profile)][co]:
                if "✓" not in self.buttons.controls[self.button[co]].text:
                    self.buttons.controls[self.button[co]].text = self.buttons.controls[self.button[co]].text + " ✓"

    def updateButtons(self):
        for co in ["infantry_camp", "cavalry_camp", "archery_camp", "siege_camp", "hospital", "scout_camp",
                   "city_transfer", "city_hall_position"]:
            if self.data[str(self.instance)]["schedules"][str(self.profile)][co]:
                if "✓" not in self.buttons.controls[self.button[co]].text:
                    self.buttons.controls[self.button[co]].text = self.buttons.controls[self.button[co]].text + " ✓"
        self.update()

    def setCurrentBuild(self, param: str):
        self.current_build = param
        for element in self.buttons.controls:
            element.color = "blue"
        self.buttons.controls[self.button[param]].color = "red"
        self.buttons.page.update()

    def on_tap_update(self, e: ft.ControlEvent):
        if self.current_build == None:
            return
        print(e.local_x * 2, e.local_y * 2)
        try:
            self.data = self.FileSingleton.get_data()
            print(f"{self.instance =  } {self.profile =}")
            print(self.data[str(self.instance)]['schedules'][str(self.profile)][self.current_build])
            self.data[str(self.instance)]['schedules'][str(self.profile)][self.current_build] = (
                int(e.local_x * 2), int(e.local_y * 2))
            self.FileSingleton.write_data(self.data)
            self.data = self.FileSingleton.get_data()
            print(self.data[str(self.instance)]['schedules'][str(self.profile)][self.current_build])
            self.updateButtons()
        except Exception as e:
            traceback.print_exc()
            return
        for element in self.buttons.controls:
            element.color = "blue"
        self.buttons.page.update()
        self.FileSingleton.write_data(self.data)
