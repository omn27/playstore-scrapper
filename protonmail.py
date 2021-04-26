import json
import time
import pandas as pd
import numpy as np
import urllib
from fake_useragent import UserAgent
import requests
import re
import random
import json
from newConnecTor import newConnection


def checkEmailStatusProtonmail(email):
    url = "https://mail.protonmail.com/api/users/available?Name="
    headers = {"x-pm-appversion": "Web_3.16.60"}
    onlyName = email[0 : email.find("@")]
    urlCompleta = url + onlyName
    torport = 9050
    proxies = {
        "http": "socks5h://localhost:{}".format(torport),
        "https": "socks5h://localhost:{}".format(torport),
    }
    response = requests.get(urlCompleta, headers=headers, proxies=proxies)
    jsonResponse = json.loads(response.text)
    if response.status_code == 409 or response.status_code == 200:
        if jsonResponse["Code"] == 1000:
            return True
        if (
            jsonResponse["Code"] == 12106
            and jsonResponse["Error"] == "Username already used"
        ):
            return False
    if response.status_code == 422:
        if (
            jsonResponse["Code"] == 12102
            and jsonResponse["Error"] == "Username contains invalid characters"
        ):
            return False
    raise Exception("error ip")
