import logging
import sys
import os
from datetime import datetime

import json
from twocaptcha import TwoCaptcha

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


def current_time():
    return datetime.now().strftime("%H:%M:%S")


def solve(path, sel):
    with open('user_settings.json') as config_file:
        data = json.load(config_file)
    # print(sel, type(sel))
    logging.basicConfig(filename=f".//logs//{data[sel]['name']}_logs.txt", level=logging.INFO,
                        format=f"%(asctime)s %(message)s",
                        datefmt="[%Y-%m-%d %H:%M:%S]", filemode="a")
    if data[sel]['API_KEY'] != "":
        api_key = os.getenv('APIKEY_2CAPTCHA', data[sel]['API_KEY'])
    else:
        api_key = os.getenv('APIKEY_2CAPTCHA', '4805a29997857b110ef26530c7f39db1')
    solver = TwoCaptcha(api_key, defaultTimeout=120, pollingInterval=5)
    # print(solver)
    try:
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] Trying to resolve the captcha")
        logging.info(f"[ {data[sel]['name']} ] Trying to resolve the captcha")
        result = solver.coordinates(path,
                                    lang='en')
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] {result = }")
        logging.info(f"[ {data[sel]['name']} ] {result = }")
        return result
    except Exception as e:
        print(f"[ {current_time()} ] [ {data[sel]['name']} ] Exception raised during the resolving of the captcha (verification.py related) :\n{e}")
        logging.info(f"[ {data[sel]['name']} ] Exception raised during the resolving of the captcha (verification.py related) :\n{e}")
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
