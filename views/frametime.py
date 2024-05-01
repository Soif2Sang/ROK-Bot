from datetime import datetime, timedelta
from random import randint

import flet as ft
from schemas.emulator_schemas import AllowedTimeSlotsSchema, ProfileSchema

from utils.Components.card import GenerateCard
from utils.flet_translations import translate
from utils.functions import FileSingleton, rsetattr
from utils.singletons import ss

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


def is_valid_time(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        if 0 <= hours <= 23 and 0 <= minutes <= 59:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False


def is_slot_runnable(first, second):
    current_time = datetime.now().time()
    start_time = datetime.strptime(first, "%H:%M").time()
    end_time = datetime.strptime(second, "%H:%M").time()

    if start_time < end_time:
        return start_time <= current_time <= end_time
    else:
        now = datetime.now()
        midnight = datetime.combine(now.date(), datetime.min.time()) + timedelta(days=1)
        time_remaining = midnight - now

        # Calculate the end_time adjusted for the remaining time until the next day
        adjusted_end_time = (midnight + timedelta(seconds=time_remaining.seconds)).time()

        return start_time <= current_time <= adjusted_end_time


def random_time_in_frametime(first, second):
    if is_valid_time(first) and is_valid_time(second):
        start_time = datetime.strptime(first, "%H:%M").time()
        end_time = datetime.strptime(second, "%H:%M").time()

        if start_time < end_time:
            time_diff = (datetime.combine(datetime.min, end_time) - datetime.combine(datetime.min, start_time)).total_seconds()
        else:
            time_diff = (
                datetime.combine(datetime.min, end_time) + timedelta(days=1) - datetime.combine(datetime.min, start_time)
            ).total_seconds()

        random_seconds = randint(0, int(time_diff))

        new_time = (datetime.combine(datetime.min, start_time) + timedelta(seconds=random_seconds)).time()

        return random_seconds

    return "Invalid Time"


def is_valid_time_format(time_str):
    try:
        datetime.strptime(time_str, "%H:%M")
        return True
    except ValueError:
        return False


def is_time1_less_than_time2(time1, time2):
    if is_valid_time_format(time1) and is_valid_time_format(time2):
        return datetime.strptime(time1, "%H:%M") > datetime.strptime(time2, "%H:%M")
    else:
        return False


class RowTimezone(ft.Row):
    def __init__(
        self,
        start="00:00",
        end="00:00",
        delete_callback=None,
        update_callback=None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.update_callback = update_callback

        self.start = start
        self.stop = end

        self.field_start = ft.TextField(label="Start", value=start, on_submit=self.on_edit, height=50, width=100, data="start")

        self.field_stop = ft.TextField(label="End", value=end, on_submit=self.on_edit, height=50, width=100, data="end")

        self.delete = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            icon_size=40,
            tooltip="Delete",
            on_click=delete_callback,
        )

        self.controls.extend([self.field_start, self.field_stop, self.delete])

    def close_banner(self, e):
        self.page.banner.open = False
        self.page.update()

    def pop_banner(self, text):
        self.page.banner = ft.Banner(
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(value=text),
            actions=[
                ft.TextButton("Ok", on_click=self.close_banner),
            ],
            open=True,
        )

        self.page.update()

    def on_edit(self, e):
        if not is_valid_time_format(e.control.value):
            return self.pop_banner("Wrong time format, please fix")
        if is_time1_less_than_time2(self.field_start.value, self.field_stop.value):
            return self.pop_banner("Start time should be less than end time")

        self.start = self.field_start.value
        self.stop = self.field_stop.value

        return self.update_callback(e)


class ManagerTimezone(ft.ListView):
    def __init__(self, instance, profile, **kwargs):
        super().__init__(**kwargs)
        self.instance = str(instance)
        self.profile = str(profile)
        self.spacing = 10
        self.expand = True

        val = translate(
            "The time format should be 'hh:mm' and work on a 24-hour clock and on your computer clock.\nexemple:\n     - start : 02:00 / end : 04:00 means the script will start exclusively between 02:00 and 04:00."
        )

        self.context: ProfileSchema = ss.emulator_settings.emulators[self.instance].schedules[self.profile]

        self.controls.append(GenerateCard(subtitle=val, level="notice", height=None))
        self.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label=translate("Enable profile frametime"),
                        active_track_color=color_bank[int(self.profile)],
                        value=self.context.time_slot.enabled,
                        on_change=self.submit_with_context,
                        data={"path": "time_slot.enabled", "type": bool},
                    ),
                    ft.ElevatedButton(
                        text=translate("Add new rule"),
                        on_click=self.add_tile,
                        icon=ft.icons.ADD,
                    ),
                ],
                spacing=50,
            )
        )
        self.init()

    def init(self):
        for slot in self.context.time_slot.allowed_time_slots:
            self.controls.append(
                RowTimezone(
                    start=slot.start,
                    end=slot.end,
                    delete_callback=self.delete_callback,
                    update_callback=self.trigger_update,
                )
            )

    def add_tile(self, e):
        self.controls.append(RowTimezone(delete_callback=self.delete_callback, update_callback=self.trigger_update))
        self.update()

    def submit_with_context(self, e):
        rsetattr(self.context, e.control.data["path"], e.control.data["type"](e.control.value))
        ss.write_emulator_settings(ss.emulator_settings)

    def delete_callback(self, e):
        for control in self.controls[2:]:
            if control.delete == e.control:
                self.controls.remove(control)
                break

        self.page.update()
        self.trigger_update(e)

    def trigger_update(self, e):
        slots = []
        for control in self.controls[2:]:
            slots.append(AllowedTimeSlotsSchema(start=control.start, end=control.stop))

        ss.emulator_settings.emulators[self.instance].schedules[self.profile].time_slot.allowed_time_slots = slots
        ss.write_emulator_settings(ss.emulator_settings)


global sel, profile


def main(page: ft.Page):
    page.window_width = 720
    page.window_height = 430

    page.add(ManagerTimezone(sel, profile))
    page.title = f"Profile n°{profile} configuration"
    page.update()


def start(sel_param="1", profile_param="1"):
    global sel, profile
    sel = sel_param
    profile = profile_param
    ft.app(target=main)


if __name__ == "__main__":
    # start()
    timings = ["9:00", "23:00"]
    print(random_time_in_frametime(*timings))
