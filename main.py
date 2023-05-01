import hashlib
import sys
from time import sleep

from auth import api


def getchecksum():
    md5_hash = hashlib.md5()
    try:
        file = open(''.join(sys.argv), "rb")
    except:
        file = open(''.join(sys.argv[0]), "rb")
    md5_hash.update(file.read())
    digest = md5_hash.hexdigest()
    return digest

keyauthapp = api(
            name="Rokbd",
            ownerid="7oofxdj8uH",
            secret="a968396e3fdfff2a2eaf14516fb283b7b7013e19cf392c863c90e0d8c41d9be0",
            version="1.0",
            hash_to_check=getchecksum()
        )

username = input("Username ?")
password = input("Password ?")

if keyauthapp.login(username,password):
    print("You cracked the fuck out of my app")
    sleep(5)
else:
    print("Unable to crack it idiot")
    sleep(5)