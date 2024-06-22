import flet as ft


from utils.schemas.discord_schemas import DiscordWorkerSchema, DiscordWorkerListSingleton


class DiscordWorkerRow(ft.Row):
    def __init__(self, worker: DiscordWorkerSchema, on_click, text):
        self.worker = worker
        self.label_worker = ft.TextField(data="worker", value=worker.worker, label="Worker", disabled=text=="delete", on_change=self.on_change)
        self.label_discord_id = ft.TextField(data="discord_id", value=worker.discord_id, label="Discord ID", disabled=text=="delete",on_change=self.on_change)
        self.label_channel_id = ft.TextField(data="channel_id", value=worker.channel_id, label="Channel ID", disabled=text=="delete", on_change=self.on_change)

        self.button = ft.OutlinedButton(text=text, on_click=on_click)

        super().__init__(controls=[self.label_worker, self.label_discord_id, self.label_channel_id, self.button])

    def on_change(self, e):
        if e.control.data == "worker":
            self.worker.worker = e.control.value
        elif e.control.data == "discord_id":
            self.worker.discord_id = e.control.value
        elif e.control.data == "channel_id":
            self.worker.channel_id = e.control.value

def main(page: ft.Page):

    discord_settings = DiscordWorkerListSingleton()
    listview = ft.ListView(expand=1)
    page.add(listview)

    def delete_row(e):
        discord_settings.worker_list.workers.remove(e.control.parent.worker)
        discord_settings.write_worker_list(discord_settings.worker_list)
        refresh_page()
    def add_row(e):
        discord_settings.worker_list.workers.append(e.control.parent.worker)
        discord_settings.write_worker_list(discord_settings.worker_list)
        refresh_page()

    def refresh_page():
        print("here")
        listview.controls = []
        listview.controls.append(DiscordWorkerRow(DiscordWorkerSchema("", "", ""), add_row, "save"))
        for workers in discord_settings.read_worker_list().workers:
            listview.controls.append(DiscordWorkerRow(workers, delete_row, "delete"))

        listview.update()
        print(listview.controls)

    refresh_page()

if __name__ == "__main__":
    ft.app(main)