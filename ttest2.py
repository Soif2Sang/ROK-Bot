from realtime.connection import Socket
from supabase_auth import SupabaseClient
from constants import SUPABASE_ID, SUPABASE_KEY, SUPABASE_URL

supabaseClient = SupabaseClient()

response = supabaseClient.login("maxou@gmail.com","maxou@gmail.com")
WSS_URL = f"wss://{SUPABASE_ID}.supabase.co/realtimeLocal/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"


from utils.


def callback1(payload):
    print("Callback 1: ", payload)

if __name__ == "__main__":
    URL = f"wss://{SUPABASE_ID}.supabase.co/realtimeLocal/v1/websocket?apikey={SUPABASE_KEY}&vsn=1.0.0"
    s = Socket(URL)
    s.connect()

    channel_1 = s.set_channel("realtimeLocal:*")
    channel_1.join().on("UPDATE", callback1)
    s.listen()
