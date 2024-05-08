import base64
import traceback

import cv2
import flet as ft
import flet_route
from PIL import Image
from utils.schemas.emulator_schemas import CordsSchema

from utils.android_debug_bridge_bluestacks import AdbBluestacks
from utils.android_debug_bridge_ld_player import AdbLd
from utils.functions import FileSingleton, rgetattr, rsetattr
from utils.singletons import EmulatorSingleton, SettingsSingleton

ss = SettingsSingleton()


class cityLayoutParam(flet_route.Params):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance_index = None
        self.profile_index = None


def image_to_base64(image_byte):
    encoded_string = base64.b64encode(image_byte.read())
    return encoded_string.decode("utf-8")


def viewCityLayout(page: ft.Page, params: cityLayoutParam, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500
    emulator_choice = EmulatorSingleton().getEmulatorType()

    if emulator_choice == "bluestacks":
        adb = AdbBluestacks(str(params.instance_index))
    else:
        adb = AdbLd(str(params.instance_index))

    image_byte = image_to_base64(adb.get_curr_device_screen_img_bytesIO())

    def returnHome():
        page.window_width = 450
        page.window_height = 700
        page.go("/")

    return ft.View(
        f"/city-layout/{params.instance_index}/{params.profile_index}",
        controls=[
            ft.Container(
                bgcolor=ft.colors.SURFACE_VARIANT,
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: returnHome()),
                        ft.Text(value="Go back"),
                    ]
                ),
            ),
            ft.Text(value="Click on the building button you wanna set, then click in the center of the building."),
            CityPlacement(image_byte, params.instance_index, params.profile_index),
        ],
    )


def viewSetCenterMap(page: ft.Page, params, basket: flet_route.Basket) -> ft.View:
    page.window_width = 900
    page.window_height = 500
    emulator_choice = EmulatorSingleton().getEmulatorType()

    if emulator_choice == "bluestacks":
        adb = AdbBluestacks(str(params.instance_index))
    else:
        adb = AdbLd(str(params.instance_index))

    image = adb.get_cv2_img()
    image = image[:146, 1072:]

    cv2.imwrite("assets/map.png", image)

    def returnHome():
        page.window_width = 450
        page.window_height = 700
        page.go("/")

    return ft.View(
        f"/set-center/{params.task}/{params.instance_index}/{params.profile_index}",
        controls=[
            ft.Container(
                bgcolor=ft.colors.SURFACE_VARIANT,
                content=ft.Row(
                    controls=[
                        ft.IconButton(icon=ft.icons.ARROW_BACK, on_click=lambda _: returnHome()),
                        ft.Text(value="Go back"),
                    ]
                ),
            ),
            ft.Text(value="Click anywhere on the map to set the center of the searching area."),
            MapContainer(image, params.task, params.instance_index, params.profile_index),
        ],
    )


class CityPlacement(ft.Container):
    button = {
        "troop_training.infantry_camp": "Inf",
        "troop_training.cavalry_camp": "Cav",
        "troop_training.archery_camp": "Arch",
        "troop_training.siege_camp": "Siege",
        "troop_healing.hospital_position": "Hosp",
        "explore_fog.scout_camp_position": "Scout",
        "resources_transfer.transfer_position": "Transfer",
        "upgrade_city.city_hall_position": "CH",
        "academic_research.academy_position": "Academy",
    }

    def __init__(self, image64, instance, profile, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.profile = profile
        self.current_attribute = None

        self.main_container = ft.Stack(
            controls=[
                ft.Container(
                    image_src_base64=image64,
                    height=720 / 2,
                    width=1280 / 2,
                    on_tap_down=self.on_tap_update,
                    on_click=lambda _: 1,
                )
            ]
        )

        self.buttons = ft.ListView(height=720 / 2, expand=True, spacing=1)
        self.content = ft.Row(controls=[self.main_container, self.buttons])

        for key, item in self.button.items():
            button_text = f"Set {item.replace('_', ' ').title()}"
            button_click_handler = lambda _, name=key: self.setCurrentBuild(name)
            button = ft.ElevatedButton(text=button_text, on_click=button_click_handler)
            self.buttons.controls.append(button)

            value: CordsSchema = rgetattr(ss.emulator_settings.emulators[str(self.instance)].schedules[str(self.profile)].tasks, key)

            if value.x and value.y:
                self.main_container.controls.append(
                    ft.Chip(
                        label=ft.Text(item),
                        on_delete=self.remove_self,
                        delete_icon_tooltip="remove",
                        top=value.y / 2 - 10,
                        left=value.x / 2 - 10,
                        label_padding=0,
                        key=key,
                        opacity=0.7,
                    )
                )

    def setCurrentBuild(self, param: str):
        self.current_attribute = param

        for element in self.buttons.controls:
            element.color = "blue"

        index = -1
        for i, element in enumerate(self.button.keys()):
            if element == param:
                index = i

        self.buttons.controls[index].color = "red"
        self.buttons.page.update()

    def on_tap_update(self, e: ft.ContainerTapEvent):
        if self.current_attribute is None:
            return
        left, top = e.local_x, e.local_y

        try:
            rsetattr(
                ss.emulator_settings.emulators[str(self.instance)].schedules[str(self.profile)].tasks,
                self.current_attribute,
                CordsSchema(x=int(e.local_x * 2), y=int(e.local_y * 2)),
            )

        except Exception:
            traceback.print_exc()
            return

        for element in self.buttons.controls:
            element.color = "blue"

        for element in self.main_container.controls:
            if isinstance(element, ft.Chip):
                if element.label.value == self.button[self.current_attribute]:
                    self.main_container.controls.remove(element)

        ss.write_emulator_settings(ss.emulator_settings)

        self.main_container.controls.append(
            ft.Chip(
                label=ft.Text(self.button[self.current_attribute]),
                on_delete=self.remove_self,
                delete_icon_tooltip="remove",
                top=top - 10,
                left=left - 10,
                label_padding=0,
                key=self.current_attribute,
                opacity=0.7,
            )
        )
        self.page.update()

    def remove_self(self, e):
        self.main_container.controls.remove(e.control)
        self.page.update()

        rsetattr(ss.emulator_settings.emulators[str(self.instance)].schedules[str(self.profile)].tasks, e.control.key, CordsSchema())
        ss.write_emulator_settings(ss.emulator_settings)


class MapContainer(ft.Container):
    def __init__(self, image64, task, instance, profile, **kwargs):
        super().__init__(**kwargs)
        self.instance = instance
        self.profile = profile
        self.task = task
        self.current_build = None

        self.main_container = ft.Stack(
            controls=[
                ft.Container(
                    image_src="map.png",
                    height=146 * 2,
                    width=208 * 2,
                    image_fit=ft.ImageFit.FILL,
                    on_tap_down=self.on_tap_update,
                    on_click=lambda _: 1,
                )
            ]
        )

        self.content = ft.Row(controls=[self.main_container])

    def on_tap_update(self, e: ft.ContainerTapEvent):
        left, top = e.local_x, e.local_y

        try:
            rsetattr(
                ss.emulator_settings.emulators[str(self.instance)].schedules[str(self.profile)].tasks,
                self.task + ".map_center_pos",
                CordsSchema(x=left / 2 + 1072, y=top / 2),
            )
            ss.write_emulator_settings(ss.emulator_settings)
        except Exception:
            traceback.print_exc()
            return

        self.page.generate_toast("Success", "Center of the searching area set!", ft.icons.INFO, ft.colors.GREEN_300)
        self.page.update()
