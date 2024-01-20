import flet as ft

from views.login.login2 import LoginScreen
from utils.constants import BREZILIAN, global_name, brezilian_name, ownerid, global_secret, brezilian_secret
import json

def main(page:ft.Page):
    page.add(LoginScreen(page))

ft.app(target=main)
