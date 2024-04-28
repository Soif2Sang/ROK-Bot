import flet as ft
from flet import Container, Image, Page, colors
from flet_toast.core import Position
from flet_toast.toasts_flexible import ToastsFlexible
from tiles.handler.logging_handler import Logger

toasts_history = {}


def main(page: Page):
    def generate_toast(title, description, icon=ft.icons.INFO, bgcolor_title="AMBER"):
        ToastsFlexible(
            page=page,
            icon=icon,
            title=title,
            desc=description,
            auto_close=None,
            trigger=None,
            width=360,
            set_history=toasts_history,
            position=Position.TOP_RIGHT,
            bgcolor_title=bgcolor_title,
        )

    page.generate_toast = lambda title, description, icon=ft.icons.INFO, bgcolor_title=ft.colors.ERROR_CONTAINER: generate_toast(
        title, description, icon, bgcolor_title
    )

    colors_list = [
        "primary",
        "onprimary",
        "primarycontainer",
        "onprimarycontainer",
        "secondary",
        "onsecondary",
        "secondarycontainer",
        "onsecondarycontainer",
        "tertiary",
        "ontertiary",
        "tertiarycontainer",
        "ontertiarycontainer",
        "error",
        "onerror",
        "errorcontainer",
        "onerrorcontainer",
        "outline",
        "outlinevariant",
        "background",
        "onbackground",
        "surface",
        "onsurface",
        "surfacetint",
        "surfacevariant",
        "onsurfacevariant",
        "inversesurface",
        "oninversesurface",
        "inverseprimary",
        "shadow",
        "scrim",
        "white10",
        "white12",
        "white24",
        "white30",
        "white38",
        "white54",
        "white60",
        "white70",
        "white",
        "transparent",
        "black12",
        "black26",
        "black38",
        "black45",
        "black54",
        "black87",
        "black",
        "red",
        "pink",
        "purple",
        "deeppurple",
        "indigo",
        "blue",
        "lightblue",
        "cyan",
        "teal",
        "green",
        "lightgreen",
        "lime",
        "yellow",
        "amber",
        "orange",
        "deeporange",
        "brown",
        "bluegrey",
        "redaccent",
        "pinkaccent",
        "purpleaccent",
        "deeppurpleaccent",
        "indigoaccent",
        "blueaccent",
        "lightblueaccent",
        "cyanaccent",
        "tealaccent",
        "greenaccent",
        "lightgreenaccent",
        "limeaccent",
        "yellowaccent",
        "amberaccent",
        "orangeaccent",
        "deeporangeaccent",
        "grey",
        "grey50",
        "grey100",
        "grey200",
        "grey300",
        "grey400",
        "grey500",
        "grey600",
        "grey700",
        "grey800",
        "grey900",
    ]

    # for color in colors_list:
    #     page.generate_toast("Title description", f"Une description incroyable {color}", bgcolor_title=color)
    #
    logger = Logger(page, page)

    logger.add_text("[00:12:55] Character n4", color=ft.colors.CYAN_ACCENT_700)
    logger.add_text("[00:12:55] Task 8/9", color=ft.colors.BLUE)
    logger.add_text("[00:12:55] Currently executing task", color=ft.colors.BLUE)

    # Lines with suggested colors
    logger.add_text("[00:13:58] Switching Character", color=ft.colors.PURPLE)
    logger.add_text("[00:14:22] Current character detected.", color=ft.colors.GREEN)
    # logger.add_text("[00:14:25] No more characters, going back to the first character")
    # logger.add_text("It seems the game is unable to load the characters menu..", ft.colors.RED_300)
    logger.add_text("[00:14:22] Switching to the next character", color=ft.colors.PURPLE_400)
    logger.add_text("[00:14:33] Script is paused until the game is fully loaded..", color=ft.colors.GREY)
    logger.add_text("[00:15:35] Run nb'O took 0:21:41 to complete.")
    logger.add_text("[00:14:22] script is paused for", color=ft.colors.GREY)
    logger.add_text("[00:15:35] Leaving the game..")

    # Add the logger to the page
    page.add(logger)


ft.app(target=main)
