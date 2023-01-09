import flet as ft

def main(page: ft.Page):
    page.title = "Routes Example"

    database = \
        ft.DataTable(
            data_row_color={ft.MaterialState.HOVERED: ft.colors.GREEN, ft.MaterialState.FOCUSED: ft.colors.GREEN},
            sort_column_index=0,
            sort_ascending=True,
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Name")),
                ft.DataColumn(ft.Text("Task")),
                ft.DataColumn(ft.Text("Status")),
            ]
        )
    page_accueil = ft.View(
        controls=[
            database,
            ft.FilledButton("Refresh DataTable", icon=ft.icons.REFRESH, on_click=updateTable),
            ft.FilledButton("Add timer", icon=ft.icons.TIMER, on_click=lambda e: set_timer(e, 1, 60)),
            ft.FilledButton("Add text", icon=ft.icons.TEXT_FIELDS,
                            on_click=lambda e: set_text(e, 1, "Random text")),
        ]
    )
    def route_change(route):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Flet app"), bgcolor=ft.colors.SURFACE_VARIANT),
                    ft.ElevatedButton("Visit Store", on_click=lambda _: page.go("/store")),
                ],
            )
        )
        if page.route == "/store":
            page.views.append(
                ft.View(
                    "/store",
                    [
                        ft.AppBar(title=ft.Text("Store"), bgcolor=ft.colors.SURFACE_VARIANT),
                        ft.ElevatedButton("Go Home", on_click=lambda _: page.go("/")),
                    ],
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main)