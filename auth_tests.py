import hashlib
import sys
from datetime import datetime, date
from time import sleep
from uuid import uuid4

import requests
from Crypto.Hash import SHA256

from auth import encryption, selfApi


def getchecksum():
    md5_hash = hashlib.md5()
    file = open(''.join(sys.argv[0]), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

if __name__ == "__main__":
    keyauthapp = selfApi(
        name = "Rokbd",
        ownerid = "7oofxdj8uH",
        secret = "a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
        version = "1.0",
        hash_to_check = getchecksum()
    )


    # "f6386c16787e0eb51b24d168205267e6"
    keyauthapp.login("maxence","fe")
    print(f"""
    App data:
    Number of users: {keyauthapp.app_data.numUsers}
    Number of online users: {keyauthapp.app_data.onlineUsers}
    Number of keys: {keyauthapp.app_data.numKeys}
    Application Version: {keyauthapp.app_data.app_ver}
    Customer panel link: {keyauthapp.app_data.customer_panel}
    """)

    print(f"Current Session Validation Status: {keyauthapp.check()}")

    print("\nUser data: ")
    print("Username: " + keyauthapp.user_data.username)
    print("IP address: " + keyauthapp.user_data.ip)

    subs = keyauthapp.user_data.subscriptions  # Get all Subscription names, expiry, and timeleft
    for i in range(len(subs)):
        sub = subs[i]["subscription"]  # Subscription from every Sub
        expiry = datetime.utcfromtimestamp(int(subs[i]["expiry"])).strftime(
            '%Y-%m-%d %H:%M:%S')  # Expiry date from every Sub
        timeleft = subs[i]["timeleft"]  # Timeleft from every Sub

        print(f"[{i + 1} / {len(subs)}] | Subscription: {sub} - Expiry: {expiry} - Timeleft: {timeleft}")
    print("Created at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.createdate)).strftime('%Y-%m-%d %H:%M:%S'))
    print("Last login at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.lastlogin)).strftime('%Y-%m-%d %H:%M:%S'))
    print("Expires at: " + datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S'))
    print(f"Current Session Validation Status: {keyauthapp.check()}")

    today = date.today()
    date_brut = datetime.utcfromtimestamp(int(keyauthapp.user_data.expires)).strftime('%Y-%m-%d %H:%M:%S').split(" ")[0]
    heures = date_brut.split('-')
    future = date(int(heures[0]), int(heures[1]), int(heures[2]))
    diff = future - today
    print(diff)
    url2 = f"https://keyauth.win/api/seller/?sellerkey=f6386c16787e0eb51b24d168205267e6&type=adduser&user={'test'}&pass={'test'}&sub=default&expiry={1}"

    headers = {
        'content-type': "application/json",
        'cache-control': "no-cache"
    }
    reponse = requests.request("GET", url2, headers=headers).json()

    print(reponse)

    # while True:
    #     keyauthapp.login("maxence","fe")
    #     print(f"Current Session Validation Status: {keyauthapp.check()}")
    #     sleep(10)