import pandas as pd
import numpy as np
import urllib
from fake_useragent import UserAgent
import requests
import re
from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
import time
import db
from models import Links
from datetime import datetime
from sqlalchemy.sql import func
from sqlalchemy.orm import load_only
import random
from hotmail import checkEmailStatusHotmail
from protonmail import checkEmailStatusProtonmail
from aolmail import checkEmailStatusAolmail
from rediffmail import checkEmailStatusRediffmail


def armarUrl(dork, links):
    urllinks = ""
    for l in range(len(links)):
        urllinks = urllinks + " -" + links[l].url
    return dork + urllinks


def escribirInicioOFinalEnArchivo(inicio):
    if inicio:
        t = open("logs.txt", "w")
        now = datetime.now()
        t.write(str(now.time()) + "\n")
        t.close()
    else:
        f = open("logs.txt", "a")
        f.write(response.text)
        now = datetime.now()
        f.write("\n" + str(now.time()))
        f.close()


def obtenerRandomRows(dorks):
    ids = obtenerRandomIds(dorks)
    randomRows = []
    for i in range(len(ids)):
        randomRows.append(db.session.query(Links).filter(Links.id == ids[i]).all())
    return randomRows


def obtenerRandomIds(dorks):
    raw = db.session.query(Links).filter_by(dork=dorks).all()
    ids = []
    for i in range(len(raw)):
        ids.append(raw[i].id)
    if len(ids) < 125:
        return random.sample(ids, len(ids))
    return random.sample(ids, 125)


def obtenerRandomNumbers():
    cantRegistros = obtenerCantidadDeRegistrosDeTablaLinks()
    randomNumbers = random.sample(range(1, cantRegistros), 125)
    return randomNumbers


def obtenerCantidadDeRegistrosDeTablaLinks():
    return db.session.query(Links).count()


def tablaVacia(dorks):
    if (db.session.query(Links).filter_by(dork=dorks).count()) == 0:
        return True
    return False


def armarUrlConFiltro(dork):
    links = obtenerRandomRows(dork)
    urllinks = ""
    for l in range(len(links)):
        li = links[l]
        urllinks = urllinks + " -" + li[0].packet_name
    return dork + urllinks


def armarUrlSinFiltro(dork):
    return dork


def armarUrl(dork):
    url = ""
    if tablaVacia(dork):
        url = armarUrlSinFiltro(dork)
    else:
        url = armarUrlConFiltro(dork)
    return url


def hacerGetBing(query_bing, j):
    bing_url = (
        "https://www.bing.com/search?q=" + query_bing + "&start=1" + "&first=" + str(j)
    )
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    try:
        response = requests.get(bing_url, headers=headers)
        return response
    except:
        response = requests.get(bing_url, headers=headers)
        return response


def dormir(minimo, maximo):
    time.sleep((maximo - minimo) * np.random.random() + minimo)


def obtenerLinksDeLaBusqueda(soup):
    result = soup.find_all("h2")
    links = []
    for i in range(len(result)):
        for link in result[i].find_all("a", href=True):
            links.append(link["href"])
    return links


def packetNameValido(url):
    if url.find("//") == -1 and url.find(".") >= 0:
        return True
    return False


def obtenerSoloPacketName(link):
    link = urllib.parse.unquote(link, encoding="utf-8")
    txt = link
    url = txt[txt.find("id") + 3 : txt.find("&")]
    return url


def obtenerEmailDePlayStore(packetName):
    playstoreUrl = "https://play.google.com/store/apps/details?id=" + packetName
    ua = UserAgent()
    headers = {"User-Agent": ua.random}
    response = requests.get(playstoreUrl, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    if response.status_code != 404 and response.status_code != 429:
        result = soup.find_all("a", attrs={"class": "hrTbp euBY6b"})
        r = result[0]
        mail = r.contents[0]
        return mail
    else:
        return None


def obtenerEstadoEmail(email):
    statusEmail = None
    if email.find("@hotmail.com") > -1 or email.find("@outlook.com") > -1:
        statusEmail = checkEmailStatusHotmail(email)
    else:
        if email.find("@protonmail.com") > -1:
            statusEmail = checkEmailStatusProtonmail(email)
        else:
            if email.find("@rediffmail.com") > -1:
                statusEmail = checkEmailStatusRediffmail(email)
            else:
                if email.find("@aol.com") > -1:
                    statusEmail = checkEmailStatusAolmail(email)
    return statusEmail


def packetNameInTable(packetName):
    obs = db.session.query(Links).filter_by(packet_name=packetName).first()
    if obs:
        return True
    return False