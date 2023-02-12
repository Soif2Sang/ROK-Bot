import logging
import sys
import os
from datetime import datetime, date

import json
from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def solve(path, sel):
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    # print(sel, type(sel))
    if data[sel]['API_KEY'] != "":
        api_key = os.getenv('APIKEY_2CAPTCHA', data[sel]['API_KEY'])
    else:
        api_key = os.getenv('APIKEY_2CAPTCHA', '4805a29997857b110ef26530c7f39db1')
    solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)
    # print(solver)
    try:
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] Trying to resolve the captcha")
        with open(f"{data[sel]['name']}_logs.txt", "a+", encoding="utf-8") as logger:
            logger.write(f"[ {date.today()} ] [ {current_time()} ] [ {data[sel]['name']} ] INFO : Trying to resolve the captcha\n")
        result = solver.coordinates(path,
                                    lang='en')
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] {result = }")
        with open(f"{data[sel]['name']}_logs.txt", "a+", encoding="utf-8") as logger:
            logger.write(f"[ {date.today()} ] [ {current_time()} ] [ {data[sel]['name']} ] INFO : result = {result}\n")
        return result
    except Exception as e:
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] Exception raised during the resolving of the captcha (verification.py related) :\n{e}")
        with open(f"{data[sel]['name']}_logs.txt", "a+", encoding="utf-8") as logger:
            logger.write(f"[ {date.today()} ] [ {current_time()} ] [ {data[sel]['name']} ] EXCEPTION : Exception raised during the resolving of the captcha (verification.py related) :\n{e}\n")
        return {}


def string_to_co(string):
    string = string.replace("coordinates:", "")
    string = string.replace("x=", "")
    string = string.replace("y=", "")
    tmp = string.split(';')
    boolean = True
    for i in range(len(tmp)):
        tmp[i] = tmp[i].split(",")
        tmp[i][0] = int(tmp[i][0]) + 441
        tmp[i][1] = int(tmp[i][1]) + 101
    return tmp
