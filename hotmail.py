import requests
from newConnecTor import newConnection
import json


def checkEmailStatusHotmail(email):
    if email.find(".com.") != -1:
        return None
    url = "https://signup.live.com/API/CheckAvailableSigninNames?lic=1&uaid=63cbb1cb1ca7420a952ce342aaf1d781"

    payload = (
        '{"signInName":"'
        + email
        + '","uaid":"49606c0e514a4d5dbeffa9f06822eb85","includeSuggestions":true,"uiflvr":1001,"scid":100118,"hpgid":200639}'
    )
    headers = {
        "canary": "m1QzXpnEK7uU3aLSwJtnHk+dEW4XpqGA4eUlgwFjwD7q8RDWeVVB5cArNwueOeTE1wkmFWhG9FawAx+XmVXmtmtcLR1ld+GlUIRTeYc6R7E5pQQvc986nr50OOsHZTuUMIR/kmKQ0FsvsjBUdaJW05VUWpVv3EVbijMnClDtHA0i2UysifGN6Rgjp9oiyNl0s0xtclwtryl3sGbRc4yWdyBiyyjw3ZdmAFflH4HAf0NDG/9nx0zNeMnTXgl+11cX:2:3c",
        "Content-Type": "text/plain",
        "Cookie": "amsc=ktAFkMtJk3oD7fp57aiUWp+K+jApsZXmIy6YB3XJkc0ope8sV4iREwyz4fFHHTP0sJRFaeYRwjTvp2TH8C45ZWI8jvxUCyg8A/mnqJv+FjUibMPyjmqrABfgVA28GvYBCf4gK+YnOB93r7EfScRSE7C/2qA0GcamxD/fxSpJayhq26Kx0eLXh+P0nkbE6OgTD/NZi34zzqe8kwSaF/AK1XnNGpZQrYLfnbVvmbxXn/4zKyEamuH6OhMgSPH97d+ezW8wISqm21VeQYjis9FjwEWu8flAGj7ctwMT9iQeXd3v60zS113CD7y9nbDBNAUB:2:3c; mkt=en-US; mkt1=es-AR; amcanary=0",
    }
    torport = 9050
    proxies = {
        "http": "socks5h://localhost:{}".format(torport),
        "https": "socks5h://localhost:{}".format(torport),
    }

    response = requests.request(
        "POST", url, headers=headers, data=payload, proxies=proxies
    )
    estado = None
    if response.status_code == 200:
        r = json.loads(response.text)
        try:
            estado = r["isAvailable"]
        except KeyError:
            if r["error"]["code"] == "1220" or r["error"]["code"] == "1064":
                estado = False
        if estado != True and estado != False:
            raise ("excepcion")
    else:
        print("xd")
    return estado