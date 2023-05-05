import time
from random import randint

import flet as ft

from utils.Task_utils import get_data, write_data

color_bank = {
    1: "#3b8ed0",
    2: "#ba4543",
    3: "#dec433"
}


def is_valid_time(time: str):
    if len(time) != 5:
        return False
    if ":" not in time:
        return False
    hours, minutes = time.split(":")
    if not str(hours).isnumeric() or not str(minutes).isnumeric():
        return False
    if int(hours) > 24 or int(minutes) > 60:
        return False
    return True

def is_in_frametime(first,second):
    import time
    year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
    if not is_valid_time(first) or not is_valid_time(second):
        return False

    current = hour * 60 + min
    start = int(first.split(":")[0]) * 60 + int(first.split(":")[1])
    end = int(second.split(":")[0]) * 60 + int(second.split(":")[1])

    return start < current < end

def random_time_in_frametime(first,second):
    if not is_valid_time(first) or not is_valid_time(second):
        return 9_999_999
    import time
    year, month, day, hour, min = map(int, time.strftime("%Y %m %d %H %M").split())
    current = hour * 3600 + min * 60
    start = int(first.split(":")[0]) * 3600 + int(first.split(":")[1]) * 60
    end = int(second.split(":")[0]) * 3600 + int(second.split(":")[1]) * 60
    if end > current > start:
        start = current
    start = start - current
    end = end - current
    return randint(start,end)
class RowTimezone(ft.Row):
    def __init__(self,instance,profile,parent,start ="00:00",end="00:00",default=True,**kwargs):
        super().__init__(**kwargs)
        self.data = get_data()
        if start == "00:00" and end == "00:00" and default:
            self.data[str(instance)]['schedules'][str(profile)]["timing"].append(["00:00","00:00"])
        self.instance = str(instance)
        self.profile = str(profile)
        self.parent = parent
        self.start = start
        self.stop = end
        self.field_start = ft.TextField(label="Start",value=start,on_submit=lambda _:self.sub(),height=50)
        self.field_stop = ft.TextField(label="End",value=end,on_submit=lambda _:self.sub(),height=50)
        self.delete = ft.IconButton(
            icon=ft.icons.DELETE_FOREVER_ROUNDED,
            icon_color="pink600",
            icon_size=40,
            tooltip="Delete",
            on_click=lambda _: self.parent.delete(self)
        )
        self.controls.extend([self.field_start, self.field_stop, self.delete])
        write_data(self.data)

    def close_banner(self,e):
        self.page.banner.open = False
        self.page.update()

    def pop_banner(self,text):
        self.page.banner = ft.Banner(
            bgcolor=ft.colors.AMBER_100,
            leading=ft.Icon(ft.icons.WARNING_AMBER_ROUNDED, color=ft.colors.AMBER, size=40),
            content=ft.Text(
                value=text
            ),
            actions=[
                ft.TextButton("Ok", on_click=self.close_banner),
            ],
            open=True
        )
        self.page.update()
    def sub(self):
        self.data = get_data()
        i = self.data[self.instance]['schedules'][self.profile]["timing"].index([self.start,self.stop])
        print(self.data[self.instance]['schedules'][self.profile]["timing"])
        self.data[self.instance]['schedules'][self.profile]["timing"][i] = [self.field_start.value,self.field_stop.value]
        if not is_valid_time(self.field_start.value) or not is_valid_time(self.field_stop.value):

            self.pop_banner("Wrong format, please fix")
        else:
            self.start, self.stop = self.field_start.value, self.field_stop.value

            write_data(self.data)

class ManagerTimezone(ft.ListView):
    def __init__(self,instance,profile,**kwargs):
        super().__init__(**kwargs)
        self.data = get_data()
        self.instance = str(instance)
        self.profile = str(profile)
        self.spacing = 10
        print(self.data[self.instance]['schedules'][self.profile]["timing"])
        self.controls.append(ft.Text(value="You can set a frametime to a profile\n"
                                           "The only format allowed is 'hours:minutes' also, 02:00 pm -> 14:00\n"
                                           "You may want to tune your re-do tasks timings to avoid running the profile twice during the same frametime"))
        self.data = get_data()
        self.controls.append(
            ft.Row(
                controls=[
                    ft.Switch(
                        label="Enable profile frametime",
                        active_track_color=color_bank[int(self.profile)],
                        value=True if self.data[str(self.instance)]['schedules'][str(self.profile)][
                            "enable_timing"] else False,
                        on_change=lambda _: self.reverse_keyword("enable_timing")
                    ),
                    ft.ElevatedButton(text="Add new rule", on_click=lambda _: self.add_tile(),icon=ft.icons.ADD)
                ],
                spacing=50
            )

        )
        self.init()
    def reverse_keyword(self, keyword: str, index=None):
        if index is None:
            index = self.profile
        print(f"{keyword = }, {index = }, {self.instance =}")
        self.data[str(self.instance)]['schedules'][str(index)][keyword] = not \
            self.data[str(self.instance)]['schedules'][str(index)][keyword]
        write_data(self.data)
    def init(self):
        print(self.instance,self.profile)

        for tup in self.data[self.instance]['schedules'][self.profile]["timing"]:
            print(tup)
            print(tup)
            start = tup[0]
            stop = tup[1]
            self.controls.append(RowTimezone(self.instance,self.profile,self,start=start,end=stop,default=False))

    def add_tile(self,refresh=True):
        self.data = get_data()
        self.controls.append(RowTimezone(self.instance,self.profile,self))
        self.update()

    def delete(self,tile):
        self.data = get_data()
        self.data[self.instance]['schedules'][self.profile]["timing"].pop(self.data[self.instance]['schedules'][self.profile]["timing"].index([tile.start, tile.stop]))

        for i in range(len(self.controls)):
            if self.controls[i] == tile:
                self.controls.pop(i)
                break
        write_data(self.data)
        self.update()

global sel,profile

def main(page:ft.Page):
    data = get_data()
    page.window_width = 720
    page.window_height = 430

    page.add(ManagerTimezone(sel,profile))
    page.title = f"Profile n°{profile} configuration"
    page.update()

def start(sel_param="1",profile_param="1"):
    global sel,profile
    sel = sel_param
    profile = profile_param
    ft.app(target=main)

if __name__ == "__main__":
    start()
    data = get_data()
    times = data["1"]['schedules']["1"]["timing"]
    print(time.time())


    for t in times:
        print(t)
        print(is_in_frametime(t[0],t[1]))