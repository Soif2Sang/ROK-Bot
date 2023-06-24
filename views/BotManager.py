import flet as ft
import utils


# todo: output as pdf | add error dialog to handle errors

def main(page: ft.Page):
    """
    App's entry point.

    :param page: The page object
    :type page: Page
    """
    page.title = "Markdown Editor"
    # page.window_always_on_top = True
    page.theme_mode = "dark"

    # set the minimum width and height of the window.
    page.window_min_width = 478
    page.window_min_height = 389

    # set the width and height of the window.
    page.window_width = 620
    page.window_height = 720

    # set the splash (a progress bar)
    page.splash = ft.ProgressBar(visible=False, color="yellow")

    def on_error(e):
        # page.dialog = utils.error_dialog
        # page.dialog.open = True
        # page.update()
        page.show_snack_bar(
            ft.SnackBar(ft.Text("Humm, seems like an error suddenly occurred! Please try again."), open=True),
        )

    page.on_error = on_error

    def md_update(e):
        """
        Updates the markdown(preview) when the text in the Textfield changes.

        :param e: the event that triggered the function
        """
        page.md.value = page.text_field.value
        page.update()

    def change_theme(e):
        """
        When the button(to change theme) is clicked, the theme is changed, and the page is updated.

        :param e: The event that triggered the function
        """
        page.theme_mode = "light" if page.theme_mode == "dark" else "dark"
        theme_icon_button.selected = not theme_icon_button.selected
        page.update()

    # button to change theme_mode (from dark to light mode, or the reverse)
    theme_icon_button = ft.IconButton(
        icon=ft.icons.LIGHT_MODE,
        selected_icon=ft.icons.DARK_MODE,
        icon_color=ft.colors.WHITE,
        selected_icon_color=ft.colors.BLACK,
        selected=False,
        icon_size=35,
        tooltip="change theme",
        on_click=change_theme,
    )

    page.appbar = ft.AppBar(
        title=ft.Text("Markdown Editor", color=ft.colors.WHITE),
        center_title=True,
        bgcolor=ft.colors.BLUE,
        actions=[theme_icon_button],
        elevation=5,
        leading=ft.IconButton(
            icon=ft.icons.CODE,
            icon_color=ft.colors.YELLOW_ACCENT,
            on_click=lambda e: page.launch_url("https://github.com/ndonkoHenri/Flet-Samples/tree/master/Markdown%20Editor")
        )
    )

    # you can move it to a file if you wish.
    md_test_string = """# Markdown
The following provides a quick reference to the most commonly used Markdown syntax.
Gotten from https://ashki23.github.io/markdown-latex.html

## Headers

### H3

#### H4

##### H5

###### H6

*Italic* and **Bold**
~~Scratched Text~~

## Lists
- Item 1
- Item 2
    - Item 2a (2 tabs)
    - Item 2b
        - Item 2b-1 (4 tabs)
        - Item 2b-2

Link: [Github](http://www.github.com/)

Quote:
> Imagination is more important than knowledge.
>
> Albert Einstein

## Tables

1st Header|2nd Header|3rd Header
---|:---:|---: 
col 1 is|left-aligned|1
col 2 is|center-aligned|2
col 3 is|right-aligned|3
"""

    # the LHS of the editor
    page.text_field = ft.TextField(
        value=md_test_string,
        multiline=True,
        on_change=md_update,
        expand=True,
        height=page.window_height,
        keyboard_type=ft.KeyboardType.TEXT,
        border_color=ft.colors.TRANSPARENT,
        hint_text="# Heading\n\n- Use bulleted lists\n- To better clarify\n- Your points",
    )
    # the RHS of the editor
    page.md = ft.Markdown(
        value=md_test_string,
        selectable=True,
        extension_set=ft.MarkdownExtensionSet.GITHUB_WEB,
        on_tap_link=lambda e: page.launch_url(e.data),
    )

    page.add(
        ft.Divider(thickness=1, color=ft.colors.RED_ACCENT_700),
        ft.Row(
            [
                page.text_field,
                ft.VerticalDivider(color=ft.colors.BLUE,  thickness=
                                   5),
                ft.Container(
                    ft.Column(
                        [
                            page.md
                        ],
                        scroll=ft.ScrollMode.HIDDEN
                    ),
                    expand=True,
                    alignment=ft.alignment.top_left,
                    padding=ft.padding.Padding(20, 12, 0, 0),
                    bgcolor="#36393e",
                    border=ft.border.only(left=ft.border.BorderSide(7, "blue"))
                )
            ],
            expand=True,
        ),
    )


# (running the app)
if __name__ == "__main__":
    ft.app(target=main)