from datetime import datetime
import flet as ft
import requests

from auth_tests import getchecksum
from auth import selfApi

print("creating the Api")
keyauthapp = selfApi(
    name = "Rokbd",
    ownerid = "7oofxdj8uH",
    secret = "a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
    version = "1.0",
    hash_to_check = getchecksum()
)
print("Api created")
keyauthapp.login("lordabood7","lordabood")

class Tile(ft.Row):
    def __init__(self, datas, **kwargs):
        super().__init__(**kwargs)
        self.id = datas['id']
        self.username = datas['username']
        self.password = datas['password']
        self.hwid1 = datas['HWID1']
        self.hwid2 = datas['HWID2']
        try:

            if isinstance(datas['subscriptions'],str):
                self.expiry = "0000-00-00"
            else:
                self.expiry = datetime.utcfromtimestamp(int(datas['subscriptions'][0]['expiry'])).strftime('%Y-%m-%d')
        except:
            print(datas)
        self.entry_id = ft.TextField(value=self.id,width = 100, disabled=True)
        self.entry_username = ft.TextField(value=self.username,width = 160)
        self.entry_password = ft.TextField(value=self.password,width = 300)
        self.entry_hwid1 = ft.TextField(value=self.hwid1,width = 160)
        self.entry_hwid2 = ft.TextField(value=self.hwid2, width=160)
        self.entry_expiry = ft.TextField(value=self.expiry,width = 160)
        self.controls.extend([self.entry_id,self.entry_username,self.entry_password,self.hwid1,self.hwid2,self.entry_expiry])

class TileManger(ft.ListView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.height = 600
    def add_tile(self, datas):
        self.controls.append(Tile(datas))



# url2 = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=adduser&user={'test'}&pass={'test'}&sub=default&expiry={1}"

# init_iv = SHA256.new(str(uuid4())[:8].encode()).hexdigest()
# for user in reponse['users']:
#     url2 = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=userdata&user={user['username']}"
#     print(requests.request("GET", url2, headers=headers).json())

import aiohttp
import asyncio
import time
#
start_time = time.time()


async def get_user(page,session,user2):
    url = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=getvar&user={user2['username']}&var=HWID1"
    async with session.get(url) as resp:
        resp = await resp.json(content_type=None)
        print(resp)
        user2['HWID1'] = resp.get('response',"None")
    url = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=getvar&user={user2['username']}&var=HWID2"
    async with session.get(url) as resp:
        resp = await resp.json(content_type=None)
        user2['HWID2'] = resp.get('response',"None")
    page.tile_manager.add_tile(user2)
    return user2


async def main2(page):
    url2 = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=fetchallusers"

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    reponse = requests.request("GET", url2, headers=headers).json()
    print(reponse)
    async with aiohttp.ClientSession() as session:

        tasks = []
        for user in reponse['users']:
            tasks.append(asyncio.ensure_future(get_user(page,session,user)))

        for task in tasks:
            await asyncio.gather(task)
        # await asyncio.gather(*tasks)





def main(page: ft.Page):
    page.tile_manager = TileManger()
    page.add(ft.Row(controls=[
        ft.Text(value="Id",width = 100),
        ft.Text(value="Username",width = 160),
        ft.Text(value="Password",width = 300),
        ft.Text(value="HWID1", width=160),
        ft.Text(value="HWID2", width=160),
        ft.Text(value="Expiry Date",width = 160)
    ]))
    page.add(page.tile_manager)
    asyncio.run(main2(page))
    print("--- %s seconds ---" % (time.time() - start_time))
    page.update()

if __name__ == "__main__":
    ft.app(target=main)

