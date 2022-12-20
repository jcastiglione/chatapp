import netifaces as neti
import socket
import os
import threading
from protocols import Mp
import tkinter as tk

# CONSTANTS
VERBS = {
    'sen': "SEND",
    'jn': "JOIN",
    'dis': 'DISCONNECT',
    'fet': 'FETCH',
    'inv': 'INVITE',
    'rec': 'RECIEVE',
    'cat': 'CATCH',
    'dec': 'DECLINE'
}
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
PORT = 9020

# LOCAL VARS
is_host = False
client: Mp = "NONE"
room_name = "NONE"
self_ip = "NONE"

users = {}  # {"some user" : "some IP or socket or something", ...}
blacklist = []  # ["ip1", "ip2", ...]


def create_check_sum(msg: bytes) -> bytes:
    out = 0

    for b in msg:
        out += b
    # for

    return bytes(out % 65535, Mp.ENC_TYPE)
# createCheckSum


def check_sum(msg: bytes) -> bool:
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

    if (recip != client.displayname):
        # respond with res("DECLINE", 200, sender)
        pass
    # if

    if (mtype == "DECLINE"):
        pass
        #print("[" + now() + "] SERVER: Message Declined - " + ERRORS[code])
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

    if mtype == "SEND":
        # print("[" + code + "] " + sender + ": " + body)

        for user in users:
            # send to user req("SEND", user.key?, body)
            # NEEDS A WAY TO SHOW THE ORIGINAL SENDER
            pass
        # for
        pass

    elif mtype == "JOIN":
        if (sender in users.keys):
            pass
            # respond with res("DECLINE", 300, sender)
        # if
        pass

    elif mtype == "DISCONNECT":
        print("[" + Mp.now() + "] SERVER: Connection Closed")
        room.close()

    elif mtype == "FETCH":
        if (body in users.keys):
            # respond with res("CATCH", 100, sender, users[body])
            pass
        else:
            # respond with res("DECLINE, 204, sender")
            pass
        # if/else

    elif mtype == "INVITE":
        print("[" + Mp.now() + "] SERVER: Connection Opened")

    elif mtype == "RECIEVE":
        # clear message cache maybe? Not sure if anything actually needs to happen here.
        # maybe this is when the user's message gets brought to the gui
        pass

    elif mtype == "CATCH":
        # open a connection with the ip in the body of the message
        # send whatever the user typed to that user
        pass

    else:
        # respond with res("DECLINE", 400, sender)
        pass
    # if/else

# recieve()


def broadcast() -> None:
    # broadcast to all users asking for chat rooms
    pass
# broadcast()


def send_typed_message(room: socket.socket, instance: Mp, msg: str) -> None:
    cmd = None
    body = msg

    if (msg.startswith("/")):
        cmd, body = msg.split(" ", 1)
    # if

    if (cmd == "/q"):
        pass
        #send_all(req(VERBS["dis"], 'SERVER'), room)

    elif (cmd == "/w"):
        pass
        recip, body = body.split(" ", 1)
        #send_all(req(VERBS["fet"], recip))
        #send_all(req(VERBS["sen"], recip, body), )

        # send to host req("FETCH", "HOST", recip)

    elif (cmd == "/b"):

        if is_host:
            #send_all("hello i kicked u lmao")
            blacklist.append(room.getpeername())
            room.close()
        else:
            #print("[" + now() + "] SERVER: Insufficent Permissions")
            pass
        # if/else

    elif (cmd == "/k"):

        if is_host:
            #send_all("hello i kicked u lmao")
            room.close()
        else:
            #print("[" + now() + "] SERVER: Insufficent Permissions")
            pass
        # if/else

    elif (cmd == None):
        # send to host send("SEND", "HOST", body)
        pass

    else:
        #print("[" + now() + "] SERVER: Incorrect Message Formatting")
        pass

    # if/else
# send_typed_message()


def handle_client(conn: socket.socket, addr: str) -> None:
    pass
# handle_client()


def start_server(socket: socket.socket) -> None:
    socket.listen(5)

    while True:
        conn, addr = socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
# start_server()


def start_client() -> None:
    name = input("Choose display name: ")
    client = Mp(name)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('10.103.65.12', PORT))

    while True:
        msg = input("Enter Message: ")
        send_typed_message(client_socket, client, msg)
    # while
# start_client()


if __name__ == "__main__":
    self_ip = socket.gethostbyname(socket.gethostname())
    network_setting = None
    for inter in neti.interfaces():
        if inter is not None:
            network_setting = neti.ifaddresses(inter).get(neti.AF_INET)[0]
            if network_setting['addr'] == self_ip:
                break

    print(network_setting)

    choice = input('1 for server\n2 for client\n')
    if choice == 1:
        is_host = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self_ip, PORT))
        server_thread = threading.Thread(
            target=start_server, args=(server_socket,))
        server_thread.start()
    if choice == 2:
        start_client()
# main()
