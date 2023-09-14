import flet as ft

from views import Flet_TileManager



class Body(ft.Column):
    def __init__(self, initial_page, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial_page = initial_page
        self.height = 640
        self.tile_manager = Flet_TileManager.TileManager(self.initial_page)
        self.initial_page.tile_manager = self.tile_manager
        self.current_frame = ft.Container()

        self.controls = [
            self.tile_manager,
            ft.Divider(),
            self.current_frame
        ]