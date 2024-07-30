from typing import Literal

DEBUG = False

VERSION_TYPE: Literal["global", "brazilian", "arabic"] = "global"

VERSION_NUMBER = "3.4.10"
TOAST_HISTORY = {}

names: dict[Literal["global", "brazilian", "arabic"], Literal["RokNet", "ROKBOT"]] = {"global": "RokNet","arabic": "RokNet", "brazilian": "ROKBOT"}

BOT_NAME: Literal["RokNet", "ROKBOT"] = names[VERSION_TYPE]

SUPABASE_ID: str = "rytpbbadrdnfozckfjde"
SUPABASE_URL: str = "https://rytpbbadrdnfozckfjde.supabase.co"
SUPABASE_KEY: str = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InJ5dHBiYmFkcmRuZm96Y2tmamRlIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDUxNDU2ODAsImV4cCI6MjAyMDcyMTY4MH0.K3da9dT4qw9e3osKrQakBEPVjeLWMDo0dEdytVLLqfY"
)

CAMPAIGN_BUTTON = 730, 675
INVENTORY_BUTTON = 830, 675
ALLIANCE_BUTTON = 930, 675
COMMANDER_BUTTON = 1030, 675
