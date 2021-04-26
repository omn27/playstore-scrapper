from stem import Signal
from stem.control import Controller


def newConnection():
    with Controller.from_port(port=9051) as controller:
        controller.authenticate(
            password="your password set for tor controller port in torrc"
        )
        controller.signal(Signal.NEWNYM)
        print("New Tor connection processed")
