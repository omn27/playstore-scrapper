import requests
import xmltodict
import json
from newConnecTor import newConnection


def checkEmailStatusRediffmail(email):
    url = (
        "https://register.rediff.com/utilities/checkavailability/checkavailability.php?login="
        + email[0 : email.find("@")]
        + "&fname=&lname=&rkey=975456"
    )

    payload = {}
    headers = {
        "Connection": "keep-alive",
        "sec-ch-ua": '"Google Chrome";v="89", "Chromium";v="89", ";Not A Brand";v="99"',
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.128 Safari/537.36",
        "Accept": "*/*",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://register.rediff.com/register/register.php?FormName=user_details",
        "Accept-Language": "es-419,es;q=0.9,en;q=0.8",
        "Cookie": "_ga=GA1.2.322779123.1618073809; RuW=217a5ae0.5bfa12aad98e4; _gid=GA1.2.910053590.1618594696; Rlrd=DmdTOANpUTEANlYwUmJfb1UsVQ5TElZAAHpQMQA2B2VQOAM5UmdXYgRhADUEMg%3D%3D; ukid=DmdTOANpUTEANlYwUmJfb1UsVQ5TElZAAHpQMQA2B2VQOAM5UmdXYgRhADUEMg%3D%3D; ckey=9a83c7740e6ad99f0ecdaafa98ad6ad5",
    }
    torport = 9050
    proxies = {
        "http": "socks5h://localhost:{}".format(torport),
        "https": "socks5h://localhost:{}".format(torport),
    }
    response = requests.request(
        "GET", url, headers=headers, data=payload, proxies=proxies
    )
    r = xmltodict.parse(response.text)
    estado = r["Registration"]
    if estado["Status"] == "Success":
        return True
    else:
        if estado["Status"] == "Failure" and (
            estado["StatusMsg"] == "Rediff ID already exists"
            or estado["StatusMsg"]
            == "This ID is not allowed. Please choose another ID."
            or estado["StatusMsg"]
            == "The ID contains invalid character(s). Please choose another ID."
        ):
            return False
        else:
            if (
                estado["Status"] == "Failure"
                and estado["StatusMsg"]
                == "The system cannot process your request at this time."
            ):
                raise Exception("error de ip")

        print("xd")