from bs4 import BeautifulSoup
import random
from queue import Queue
from threading import Thread
import time
import db
from models import Links
from sqlalchemy.exc import InvalidRequestError
from functions import (
    armarUrl,
    hacerGetBing,
    dormir,
    obtenerLinksDeLaBusqueda,
    obtenerSoloPacketName,
    packetNameInTable,
    obtenerEmailDePlayStore,
    obtenerEstadoEmail,
)
from newConnecTor import newConnection
from androiddeveloper import checkAccountExistsAndroidDeveloper


def workerSearchEmailInPlaystore():
    while True:
        re = searchEmailInPlayStoreQueue.get()
        email = obtenerEmailDePlayStore(re.packet_name)
        print("email: " + str(email))
        if email == "grinfotech@rediffmail.com":
            pass
        else:
            re.email = email
            searchEmailStatusQueue.put(re)


def workerSearchEmailStatus():
    while True:
        registro = searchEmailStatusQueue.get()
        if registro.email != None:
            thread = Thread(target=workerSearchEmailStatusHijo, args=(registro,))
            thread.start()
        else:
            writeInTable.put(registro)
        time.sleep(1)


def workerSearchEmailStatusHijo(r):
    try:
        print("search email status hijo thread")
        if r.email:
            status = obtenerEstadoEmail(r.email)
            r.email_isAvailable = status
        if r.email_isAvailable == True:
            r.account_in_AndroidDeveloper = checkAccountExistsAndroidDeveloper(r.email)
        writeInTable.put(r)
        print("hijo thread murio")
    except:
        print("new Connection")
        newConnection()
        searchEmailInPlayStoreQueue.put(r)


def workerWriteLinkInTable():
    while True:
        l = writeInTable.get()
        esta = db.session.query(Links).filter_by(packet_name=l.packet_name).count()
        if esta > 0:
            print("esta en la tabla")
            pass
        else:
            db.session.add(l)
            db.session.commit()


dorks = [
    'site:play.google.com inbody:"hotmail.com"',
    'site:play.google.com inbody:"aol.com"',
    'site:play.google.com inbody:"protonmail.com"',
    'site:play.google.com inbody:"rediffmail.com"',
    'site:play.google.com inbody:"outlook.com"',
]
j = 1
searchEmailInPlayStoreQueue = Queue()
searchEmailStatusQueue = Queue()
writeInTable = Queue()

d = dorks[random.randint(0, len(dorks) - 1)]
query_bing = armarUrl(d)
anterior = ""

response = hacerGetBing(query_bing, j)
soup = BeautifulSoup(response.text, "html.parser")
threadsSearchEmailInPlaystore = [
    Thread(target=workerSearchEmailInPlaystore) for _ in range(2)
]
threadsSearchEmailStatus = [Thread(target=workerSearchEmailStatus) for _ in range(1)]
threadsWriteLinkInTable = [Thread(target=workerWriteLinkInTable) for _ in range(1)]

[thread.start() for thread in threadsSearchEmailInPlaystore]
[thread.start() for thread in threadsSearchEmailStatus]
[thread.start() for thread in threadsWriteLinkInTable]

while response.status_code != 429:
    if j >= 999 or response.status_code == 404 or anterior == response.text:
        d = dorks[random.randint(0, len(dorks) - 1)]
        query_bing = armarUrl(d)
        j = 1
    else:
        links = obtenerLinksDeLaBusqueda(soup)
        for i in range(len(links)):
            packetName = obtenerSoloPacketName(links[i])
            obs = 0
            try:
                obs = db.session.query(Links).filter_by(packet_name=packetName).count()
            except InvalidRequestError:
                print("InvalidRequestError")
                time.sleep(2)
                try:
                    obs = (
                        db.session.query(Links)
                        .filter_by(packet_name=packetName)
                        .count()
                    )
                except InvalidRequestError:
                    time.sleep(1)
                    try:
                        obs = (
                            db.session.query(Links)
                            .filter_by(packet_name=packetName)
                            .count()
                        )
                    except InvalidRequestError:
                        time.sleep(1)
                        obs = (
                            db.session.query(Links)
                            .filter_by(packet_name=packetName)
                            .count()
                        )
                print("pude")
            if obs:
                pass
            else:
                registro = Links(packetName, dork=d)
                searchEmailInPlayStoreQueue.put(registro)
        j = j + 10
    anterior = response.text
    anterior = anterior + "xd"
    anterior = anterior[0:-2]
    dormir(2, 7)
    response = hacerGetBing(query_bing, j)
    soup = BeautifulSoup(response.text, "html.parser")
