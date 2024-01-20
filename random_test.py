import os
from supabase import create_client, Client

from supabase_auth import SupabaseClient
from views.login.login2 import LoginScreen
import flet as ft

url: str = "https://rytpbbadrdnfozckfjde.supabase.co"
key: str = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dHBiYmFkcmRuZm96Y2tmamRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUxNDU2ODAsImV4cCI6MjAyMDcyMTY4MH0.K3da9dT4qw9e3osKrQakBEPVjeLWMDo0dEdytVLLqfY"
# supabase: Client = create_client(url, key)

# print(supabase.auth.sign_in_with_password({'email': "maxou@gmail.com", "password": "maxou@gmail.com"}))

# print(supabase.table("keys").select("*").eq('name', '2captcha').execute())

# print(supabase.table("subscriptions").select("*").execute())

# from utils.supabase_auth import SupabaseClient
# from ttest import test
#
# s = SupabaseClient()
# s.login("maxou@gmail.com", "maxou@gmail.com")
#
# print(s.getApiKey('2captcha'))

# s.client.auth.sign_out()


s = SupabaseClient()
s.login("maxou@gmail.com", "maxou@gmail.com")
messages = s.getMessages()
for message in messages:
    print(message)
