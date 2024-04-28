import json

import flet as ft

from utils.constants import BREZILIAN, brezilian_name, brezilian_secret, global_name, global_secret, ownerid
from utils.supabase_auth import SupabaseClient
from views.login.login2 import LoginScreen

s = SupabaseClient()
s.login("maxou@gmail.com", "maxou@gmail.com")

print(s.check_hwid())
