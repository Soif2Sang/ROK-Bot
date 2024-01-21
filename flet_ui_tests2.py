import flet as ft

from utils.supabase_auth import SupabaseClient
from views.login.login2 import LoginScreen
from utils.constants import BREZILIAN, global_name, brezilian_name, ownerid, global_secret, brezilian_secret
import json

s = SupabaseClient()
s.login("maxou@gmail.com", "maxou@gmail.com")

print(s.check_hwid())