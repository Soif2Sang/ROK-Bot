import flet as ft

from settings.profile.cols.Flet_col_transfer import FletColumnRss
from settings.page_base import BasePage


class PageTransfer(BasePage):
    def __init__(self, profile):
        super().__init__(profile)

        self.add(
            ft.Text(
                value="/!\ This feature require a custom ApiKey /!\ \n""/!\ This feature is on beta and may crash /!\ \n",
                size=15,
                color="red"),
            ft.Divider(),
            self.create_normal_switch('fast_rss_transfer', 'Enable faster rss transfer\nmay be riskier'),
            FletColumnRss(self.instance_index, self.profile_index),
            ft.Divider(),
            ft.OutlinedButton(icon=ft.icons.GPS_FIXED_SHARP,
                              text="Set City Position",
                              on_click=lambda _: self.initial_page.go(
                                                  f"/citylayout/{self.instance_index}/{self.profile_index}"))
        )

        self.profile.initial_page.update()
