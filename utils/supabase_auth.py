import datetime
import os
import platform
import subprocess

from packaging.version import Version
from supabase import create_client

from utils.constants import SUPABASE_KEY, SUPABASE_URL, VERSION_NUMBER, VERSION_TYPE


class HwidAlreadyLinked(Exception):
    pass


class NoSubscriptionFound(Exception):
    pass


class others:
    @staticmethod
    def get_hwid():
        if platform.system() == "Linux":
            with open("/etc/machine-id") as f:
                hwid = f.read()
                return hwid
        elif platform.system() == "Windows":
            import win32security

            winuser = os.getlogin()
            sid = win32security.LookupAccountName(None, winuser)[
                0
            ]  # You can also use WMIC (better than SID, some users had problems with WMIC)
            hwid = win32security.ConvertSidToStringSid(sid)
            return hwid
        elif platform.system() == "Darwin":
            output = subprocess.Popen("ioreg -l | grep IOPlatformSerialNumber", stdout=subprocess.PIPE, shell=True).communicate()[0]
            serial = output.decode().split("=", 1)[1].replace(" ", "")
            hwid = serial[1:-2]
            return hwid


class SupabaseClient:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance.client = create_client(SUPABASE_URL, SUPABASE_KEY)
        return cls._instance

    def login(self, email, password):
        self.client.auth.sign_in_with_password({"email": email, "password": password})

    def check_hwid(self):
        hwid = others.get_hwid()

        data, count = self.client.table("hwid").select("*").execute()

        s = self.client.auth.get_session()

        if len(data[1]) == 0:
            self.client.table("hwid").insert({"hwid": hwid, "user_id": s.user.id}).execute()
            return True

        row = data[1][0]

        if hwid not in row["hwid"]:
            raise HwidAlreadyLinked()
        return True

    def refresh_session(self):
        self.client.auth.refresh_session()

    def getSubscriptions(self):
        self.refresh_session()
        data, count = self.client.table("subscriptions").select("*").eq("paused", False).order("start_at").execute()

        filtered = []
        for row in data[1]:
            if row["user_id"] == self.client.auth.get_session().user.id:
                filtered.append(row)

        return filtered

    def getMessages(self):
        self.refresh_session()
        data, count = (
            self.client.table("messages")
            .select("*")
            .lte("start_at", datetime.datetime.now())
            .gte("end_at", datetime.datetime.now())
            .eq("read", False)
            .execute()
        )
        return data[1]

    def getApiKey(self, name):
        self.refresh_session()
        data, count = self.client.table("keys").select("*").eq("name", name).single().execute()
        return data[1]

    def getUpdates(self):
        data, count = (
            self.client.table("updates")
            .select("*")
            .eq("version_type", VERSION_TYPE)
            .execute()
        )

        return data[1]

    def increamentCaptchaCount(self):
        self.refresh_session()
        data, count = self.client.rpc("increase_captcha_request", {}).execute()
        return int(data[1])

    def readMessage(self, id):
        self.client.table("messages").update({"read": True}).eq("id", id).execute()
