import flet as ft

from tile_handler_worker import TileHandlerWorker
# from views.tiles.handler.tile_handler_worker import TileHandlerWorker
from utils.supabase_auth import SupabaseClient
from utils.constants import toasts_history
from utils.flet_toast.core import Position
from utils.flet_toast.toasts_flexible import ToastAction, ToastsFlexible
from views.tile_handler import TileHandler

color_bank = {1: "#3b8ed0", 2: "#ba4543", 3: "#dec433"}


def Main(page: ft.Page, days=950):
    # page.clean()
    theme = ft.Theme()
    theme.page_transitions.windows = ft.PageTransitionTheme.CUPERTINO
    page.vertical_alignment = None
    page.horizontal_alignment = None
    page.frames = {}
    page.window_resizable = True
    page.window_width = 500
    page.window_height = 800
    page.theme = theme

    if page.UPGRADE:
        page.tile_manager = TileHandlerWorker(page)
    else:
        page.tile_manager = TileHandler(page)

    page.body = ft.Column(controls=[page.tile_manager, ft.Divider(height=0)])

    # if page.UPGRADE:
    #     page.body.controls.append(page.tile_manager.start_bar)

    page.go("/")
    page.tile_manager.refresh()


    supabaseClient = SupabaseClient()

    messages = supabaseClient.getMessages()
    for message in messages:
        if message["user_id"] is None:
            ToastsFlexible(
                page=page,
                icon=ft.icons.NOTIFICATION_IMPORTANT_OUTLINED,
                title="Announcements",
                bgcolor_title="red",
                desc=message["message"],
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
            )
        else:
            ToastsFlexible(
                page=page,
                icon=ft.icons.ANNOUNCEMENT_OUTLINED,
                title="Private Messages",
                bgcolor_title=ft.colors.BLUE_300,
                desc=message["message"],
                auto_close=None,
                trigger=None,
                set_history=toasts_history,
                position=Position.TOP_RIGHT,
                actions=[
                    ToastAction(
                        text="I have read",
                        action_style="texted",
                        on_click=lambda e: supabaseClient.readMessage(message['id'])
                    )
                ],
            )


if __name__ == "__main__":
    ft.app(target=Main, view=ft.FLET_APP)
