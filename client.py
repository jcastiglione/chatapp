import netifaces as neti
import socket
import os
import threading
import ipaddress
import select
from random import randbytes
from protocols import Mp
#import tkinter as tk
from time import sleep

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

known_chatrooms = {} # {"chatroom_name" : "ip address"}
users = {}  # {"some user" : "some IP or socket or something", ...}
blacklist = []  # ["ip1", "ip2", ...]


def create_check_sum(msg: bytes) -> bytes:
    out = 0

    for b in msg:
        out += b
    # for

    return (-(out % 2**16)).to_bytes(2, byteorder='big', signed=True)
# createCheckSum


def check_sum(msg: bytes) -> bool:
    sum = 0

    for i in range(len(msg)):
        if i != 2 and i != 3:
            sum += msg[i]
        # if
        
    sum += int.from_bytes(msg[2:4], byteorder='big', signed=True)
    # for
    
    return (sum % 2**16) == 0
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
        send_all( Mp.res("DECLINE", 200, sender), room)
    # if

    if (mtype == "DECLINE"):
        print("[" + now() + "] SERVER: Message Declined - " + ERRORS[code])
    # if

    if (not is_host and mtype in ["JOIN", "DISCONNECT", "FETCH"]):
        send_all( Mp.res("DECLINE", 202, sender), room)
    # if

    if (is_host and mtype in ["INVITE", "RECIEVE", "CATCH"]):
        send_all( Mp.res("DECLINE", 203, sender), room)
    # if

    if (room.getpeername() in blacklist):
        send_all( Mp.res("DECLINE", 301, sender), room)
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
            send_all( Mp.res("DECLINE", 300, sender), room)
        # if
        pass

    elif mtype == "DISCONNECT":
        print("[" + Mp.now() + "] SERVER: Connection Closed")
        room.close()

    elif mtype == "FETCH":
        if (body in users.keys):
            send_all( Mp.res("CATCH", 100, sender, users[body]), room)
        else:
            send_all( Mp.res("DECLINE, 204, sender"), room)
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
        send_all( Mp.res("DECLINE", 400, sender), room)
    # if/else

# recieve()

def refresh_chatrooms():
    refresh_sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    refresh_sckt.bind((self_ip, PORT))
    
    inputs = [refresh_sckt]
    outputs = []
    
    while inputs:
        
        readable, writable, exceptional = select.select(inputs, outputs, inputs)
        
        for s in readable:
            if s is refresh_sckt:
                header = s.recv(2**10)
                name = header[len(header) - header[1]:]
                
                if (not check_sum(header) or header[0] == 0 
                    or name.decode(Mp.ENC_TYPE) in known_chatrooms.keys()):
                    continue
                
                name = name.decode(Mp.ENC_TYPE)
                ip = str(ipaddress.ip_address(header[8:12]))
                
                known_chatrooms[name] = ip
                print("Recieved Chatroom")
                
                
def broadcast() -> None:
    # creates a socket that is allowed to send broadcast messages
    bcst_sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bcst_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    
    first_line = b'\x00' + b'\x00'
    conn_desc = randbytes(4) + int(ipaddress.ip_address(self_ip)).to_bytes(4, byteorder='big') +\
                int(ipaddress.ip_address(network_setting['broadcast'])).to_bytes(4, byteorder='big')
    chk_sum = create_check_sum(first_line + conn_desc)
    
    bcst_sckt.sendto(first_line + chk_sum + conn_desc, (network_setting['broadcast'], PORT))
    
    
# broadcast()

def recv_broadcast(server_name: str) -> None:
    # creates a socket that is allowed to send broadcast messages
    bcst_sckt = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    bcst_sckt.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    bcst_sckt.bind((network_setting['broadcast'], PORT))
    while True:
        header = bcst_sckt.recv(16)
        name = bcst_sckt.recv(header[1])
        
        if not check_sum(header + name) or header[0] == 1:
            continue
        
        body = server_name.encode(Mp.ENC_TYPE)
        first_line = b'\x01' + len(body).to_bytes(1, byteorder='big')
        conn_desc = header[4:8] + int(ipaddress.ip_address(self_ip)).to_bytes(4, byteorder='big') +\
                    header[8:12]
        
        chk_sum = create_check_sum(first_line + conn_desc + body)
        res = first_line + chk_sum + conn_desc + body
        
        bcst_sckt.sendto(res, (str(ipaddress.ip_address(int.from_bytes(header[8:12], byteorder='big'))), PORT))
        
# recv_broadcast()


def send_typed_message(room: socket.socket, instance: Mp, msg: str) -> None:
    cmd = None
    body = msg

    if (msg.startswith("/")):
        cmd, body = msg.split(" ", 1)
    # if

    if (cmd == "/q"):

        if not is_host:
            send_all( req("DISCONNECT", room_name), room)

        else:
            pass
            # send message to all users indicating room closed
            # close all connections

        # if/else

    elif (cmd == "/w"):
        pass
        recip, body = body.split(" ", 1)
        #send_all(req(VERBS["fet"], recip))
        #send_all(req(VERBS["sen"], recip, body), )

        # send to host req("FETCH", "HOST", recip)

    elif (cmd == "/b"):

        if is_host:
            recip, body = body.split(" ", 1)
            send_all( req("SEND", recip, "BANNED BY HOST"), room)
                          
            blacklist.append(room.getpeername())
            room.close()
        else:
            print("[" + now() + "] SERVER: Insufficent Permissions")
        # if/else

    elif (cmd == "/k"):

        if is_host:
            recip, body = body.split(" ", 1)
            send_all(req("SEND", recip, "KICKED BY HOST", room))
                          
            room.close()
        else:
            print("[" + now() + "] SERVER: Insufficent Permissions")
        # if/else

    elif (cmd == None):
        send_all( (req("SEND", room_name, body), room)
        pass

    else:
        print("[" + now() + "] SERVER: Incorrect Message Formatting")

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
    #client = Mp(name)
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    listner = threading.Thread(target=refresh_chatrooms, daemon=True)
    listner.start()
    broadcast()

    while True:
        print(known_chatrooms)
        sleep(2)
        # msg = input("Enter Message: ")
        # send_typed_message(client_socket, client, msg)
    # while
# start_client()


if __name__ == "__main__":
    self_ip = socket.gethostbyname(socket.gethostname())
    network_setting = None
    for inter in neti.interfaces():
        if inter is not None:
            network_setting = neti.ifaddresses(inter).get(neti.AF_INET)
            if network_setting is not None:
                if network_setting[0].get('addr') == self_ip:
                    network_setting = network_setting[0]
                    break

    print(network_setting)

    choice = input('1 for server\n2 for client\n')
    if choice == '1':
        is_host = True
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((self_ip, PORT))
        
        chatroom_name = input("Select Chatoom Name: ")
        broadcast_thread = threading.Thread(target=recv_broadcast, args=(chatroom_name,), daemon=True)
        broadcast_thread.start()
        
        server_thread = threading.Thread(
                target=start_server, args=(server_socket,))
        server_thread.start()
    if choice == '2':
        start_client()
    # if
# main()
