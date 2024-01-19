import datetime

from supabase import Client, create_client
from utils.constants import url, key, VERSION
import unittest

class SupabaseClient():
    client: Client or None = None
    def __init__(self):
        if not self.client:
            self.client = create_client(url, key)

    def login(self, email, password):
        self.client.auth.sign_in_with_password({'email': email, "password": password})

    def getSubscriptions(self):
        self.client.auth.refresh_session()
        data, count = self.client.table("subscriptions").select("*").lte('start_at', datetime.datetime.now()).gte('end_at', datetime.datetime.now()).eq("paused", False).order('tier').execute()
        return data[1]

    def getMessages(self):
        self.client.auth.refresh_session()
        data, count = self.client.table("messages").select("*").lte('start_at', datetime.datetime.now()).gte('end_at', datetime.datetime.now()).execute()
        return data[1]

    def getApiKey(self, name):
        self.client.auth.refresh_session()
        data, count = self.client.table("keys").select("*").eq('name', name).single().execute()
        return data[1]

    def getUpdates(self):
        self.client.auth.refresh_session()
        data, count = self.client.table("updates").select("*").gte('version', VERSION).execute()
        return data[1]

    def increamentCaptchaCount(self):
        self.client.auth.refresh_session()
        data, count = self.client.rpc('increase_captcha_request', {}).execute()
        return int(data[1])

class TestSupabaseClient(unittest.TestCase):

    supabase_client = None

    def setUp(self):
        self.supabase_client = SupabaseClient()
        email = "maxou@gmail.com"
        password = "maxou@gmail.com"
        self.supabase_client.login(email, password)

    def test_login(self):
        self.assertTrue(self.supabase_client.client.auth.get_session())

    def test_get_subscriptions(self):
        data = self.supabase_client.getSubscriptions()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_messages(self):
        data = self.supabase_client.getMessages()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)

    def test_get_api_key(self):
        key_name = "2captcha"
        data = self.supabase_client.getApiKey(key_name)
        self.assertIsInstance(data, dict)
        self.assertTrue(data['name'], key_name)

    def test_get_updates(self):
        data = self.supabase_client.getUpdates()
        self.assertIsInstance(data, list)

    def test_increment_captcha(self):
        value = self.supabase_client.increamentCaptchaCount()
        new_value = self.supabase_client.increamentCaptchaCount()
        self.assertTrue((value + 1) == new_value)

    def test_cannot_increment_captcha(self):
        try:
            self.supabase_client.client.table("captcha_request_count").update({'captcha_requests_count': 0}).eq('id', 1).execute()
            self.fail()
        except:
            self.assertTrue(True)
    def tearDown(self):
        self.supabase_client: SupabaseClient
        self.supabase_client.client.auth.sign_out()

if __name__ == '__main__':
    unittest.main()
