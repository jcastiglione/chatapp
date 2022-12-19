import netifaces as neti
import socket
import os
from datetime import datetime as dt
import tkinter as tk

#CONSTANTS
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

#LOCAL VARS
ishost = False
displayname = "NONE"
roomname = "NONE"
users = {
    "some user", "some IP or socket or something"
}
blacklist = ["ip1", "ip2"]

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

def recieve(message: str) -> None:
    head, body = message.split("\n", 1)
    mtype, code, recip, sender = body.split(" ", 3)

    if (recip != displayName):
        # respond with res("DECLINE", 200, sender)
        return 4
    # if

    if (not ishost and mtype in ["JOIN", "DISCONNECT", "FETCH"]):
        # respond with res("DECLINE", 202, sender)
        return 4
    # if

    if (ishost and mtype in ["INVITE", "RECIEVE", "CATCH"]):
        # respond with res("DECLINE", 203, sender)
        return 4
    #if

    # BLACKLIST CATCHING GOES HERE

    # MORE STUFF

# recieve()

def broadcast() -> None:
    #broadcast to all users asking for chat rooms
    return 4
# broadcast()

def send_message(msg: str) -> None:

    cmd = None
    body = msg
    
    if (msg.startswith("/")):
        cmd, body = msg.split(" ", 1)
    # if

    if (cmd == "/q"):
        #send to host send("DISCONNECT", "HOST")
        return 4

    elif (cmd == "/w"):
        recip, body = body.split(" ", 1)

        #send to host send("SEND", recip, body)

    elif (cmd == None):
        #send to host send("SEND", "HOST", body)
        return 4

    else:
        print(timestamp + "[SERVER]: Incorrect Message Formatting")

    # if/else
# send_message()


if __name__ == "__main__":
    print(4)
# main()
