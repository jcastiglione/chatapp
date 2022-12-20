import netifaces as neti
import socket
import os
from datetime import datetime as dt
import tkinter as tk

# CONSTANTS
ENC_TYPE = 'utf-8'
ERRORS = {
    100: "OK",
    200: "Wrong Recipient",
    201: "Incorrect Room Recipient",
    202: "Recipient is not Type:Host",
    203: "Recipient is not Type:User",
    204: "Desired Recipient Not Found",
    300: "DisplayName Not Available",
    301: "User has been blacklisted",
    400: "Bad Request"
}

# LOCAL VARS
is_host = False
displayname = "NONE"
room_name = "NONE"
self_ip = "NONE"

users = {}  # {"some user" : "some IP or socket or something", ...}
blacklist = []  # ["ip1", "ip2", ...]


def now() -> str:
    return dt.now().strftime("%H:%M")
# now()


def createCheckSum(msg: bytes) -> bytes:
    out = 0

    for b in msg:
        out += b
    # for

    return bytes(out % 65535, ENC_TYPE)
# createCheckSum


def checkSum(msg: bytes) -> bool:
    check = 0
    sum = 0

    for i in range(len(msg)):
        if i != 2 and i != 3:
            sum += msg[i]
        elif i == 2:
            check += msg[i] * 256
        else:
            check += msg[i]
        # if/else
    # for

    return check == sum
# checkSum()


def req(mtype: str, recip: str, body: str = None) -> str:
    return mtype + " " +\
        now() + " " +\
        recip + " " +\
        displayname + "\n" +\
        body
# req()


def res(mtype: str, code: int, recip: str, body: str = None) -> str:
    return mtype + " " +\
        code + " " +\
        recip + " " +\
        displayname + "\n" +\
        body
# res()


def send_all(message: bytes, conn: socket.socket) -> None:
    length = len(message)
    sent_bytes = 0

    while length > sent_bytes:
        sent_bytes += conn.send(message[sent_bytes:])
    # while
# send_all()


def recieve_all(conn: socket.socket, content_length: int) -> bytes:
    partial_message = b''
    while (len(partial_message) < content_length):
        # the body is constructed by reccuring recv calls
        partial_message += conn.recv(
            content_length - len(partial_message))
    else:
        message = partial_message
    # while/else
# recieve_all()


def recieve(room: socket.socket, message: str) -> None:
    head, body = message.split("\n", 1)
    mtype, code, recip, sender = body.split(" ", 3)

    if (recip != displayname):
        # respond with res("DECLINE", 200, sender)
        pass
    # if

    if (not is_host and mtype in ["JOIN", "DISCONNECT", "FETCH"]):
        # respond with res("DECLINE", 202, sender)
        pass
    # if

    if (is_host and mtype in ["INVITE", "RECIEVE", "CATCH"]):
        # respond with res("DECLINE", 203, sender)
        pass
    # if

    if (room.getpeername() in blacklist):
        # respond with res("DECLINE", 301, sender)
        pass
    # if

# recieve()


def broadcast() -> None:
    # broadcast to all users asking for chat rooms
    pass
# broadcast()


def send_message(room: socket.socket, msg: str) -> None:

    cmd = None
    body = msg

    if (msg.startswith("/")):
        cmd, body = msg.split(" ", 1)
    # if

    if (cmd == "/q"):
        room.send()
        # send to host req("DISCONNECT", "HOST")
        pass

    elif (cmd == "/w"):
        recip, body = body.split(" ", 1)

        # send to host req("FETCH", "HOST", recip)

    elif (cmd == None):
        # send to host send("SEND", "HOST", body)
        pass

    else:
        print("[" + now() + "] SERVER: Incorrect Message Formatting")

    # if/else
# send_message()


if __name__ == "__main__":
    self_ip = socket.gethostbyname(socket.gethostname())
    network_setting = None
    for inter in neti.interfaces():
        if inter is not None:
            network_setting = neti.ifaddresses(inter).get(neti.AF_INET)[0]
            if network_setting['addr'] == self_ip:
                break

    print(network_setting)
# main()
