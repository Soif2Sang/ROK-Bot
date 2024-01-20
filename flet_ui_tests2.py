import flet as ft


def main(page: ft.Page):
    page.spacing = 0
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = ft.padding.only(top=0)

    def handle_expansion_tile_change(e):
        page.show_snack_bar(
            ft.SnackBar(ft.Text(f"ExpansionTile was {'expanded' if e.data=='true' else 'collapsed'}"), duration=1000)
        )
        if e.control.trailing:
            e.control.trailing.name = (
                ft.icons.ARROW_DROP_DOWN
                if e.control.trailing.name == ft.icons.ARROW_DROP_DOWN_CIRCLE
                else ft.icons.ARROW_DROP_DOWN_CIRCLE
            )
            page.update()

    page.add(
        ft.ExpansionTile(
            title=ft.Row([ft.Checkbox(),ft.IconButton(icon=ft.icons.SETTINGS),ft.Text("Worker 1")]),
            affinity=ft.TileAffinity.PLATFORM,
            maintain_state=True,
            collapsed_text_color=ft.colors.RED,
            text_color=ft.colors.RED,
            controls=[ft.ListTile(title=ft.Text("This is sub-tile number 1"))],
        ),
    )


ft.app(target=main)