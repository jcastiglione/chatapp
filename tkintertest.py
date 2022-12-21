import tkinter as tk
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
import time
import ipaddress
import select
from random import randbytes
from protocols import Mp
import netifaces as neti
import socket

 
#CONSTANTS
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

server: Mp = "None"
 
 
 
 
# GUI class for the chat
class Gui:
    # constructor method
    def __init__(self):
        
 
        # chat window which is currently hidden
        self.Window = Tk()
        self.Window.withdraw()
 
        # login window
        self.Login = Tk()
        self.Login.withdraw()
        
        #setting server list as the first window that pops up
        self.server_list = Tk()
        self.server_list.withdraw()
        
        self.Host = Tk()
        self.Host.withdraw()
        
        self.host_or_client = Toplevel()
        
        self.host_or_client.title("Chat App")
        
        self.host_or_client.resizable(False,False)
        self.host_or_client.configure(width=400,
                                      height=300)
        
        self.label2 = Label(self.host_or_client,
                            text = "Please select host or client ",
                            justify=CENTER,
                            font = "Helvetica 14 bold")
        
        self.label2.place(relx=0.5,rely=0.2,anchor=CENTER)
        
        self.host_button = Button(self.host_or_client, text = "Host",
                                  height = 3, width = 30,
                                  command = self.host)
        
        self.host_button.place(relx=0.5,rely=0.4,anchor=CENTER)
        
        self.client_button = Button(self.host_or_client, text = "Client",
                                    height=3, width=30,
                                    command=self.server_List)
        
        self.client_button.place(relx=0.5,rely=0.6,anchor=CENTER)

        
        # starts the loop for all the windows 
        self.Window.mainloop()
        
        
    def host(self):
        
        #this function isnt complete because I cant point the entry name anywhere 
        # until the integration happens we cant close this 

        self.host_or_client.destroy()
        self.Host.deiconify()
        
        self.Host.title("Host")
        
        self.Host.resizable(False,False)
        self.Host.configure(width=600,
                            height=500)
        
        # create a Label
        self.label3 = Label(self.Host,
                         text="Please select a server name",
                         justify=CENTER,
                         font="Helvetica 14 bold")
 
        self.label3.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.nameentry = Label(self.Host,
                               text="Name: ",
                               font="Helvetica 12")
 
        self.nameentry.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
 
        # create a entry box for
        # tyoing the message
        self.server_entry = Entry(self.Host,
                               font="Helvetica 14")
 
        self.server_entry.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        # set the focus of the cursor
        self.nameentry.focus()
 
        # create a Continue Button
        # along with action
        self.button_entry = Button(self.Host,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.login(self.server_entry.get()))
 
        self.button_entry.place(relx=0.4,
                      rely=0.55)
        
        
    def server_List(self):
        
        self.host_or_client.destroy()
        self.server_list.deiconify()
        #setting the title 
        self.server_list.title("Server List")
        
        #setting the size of the windows and making it not resizable 
        self.server_list.resizable(width = False,
                                   height= False)
        self.server_list.configure(width=600,
                                   height=500)
        
        # creating the label to ask the user to select a server
        self.label1 = Label(self.server_list,
                           text="please select a server to continue",
                           justify=CENTER,
                           font="Helvetica 14 bold")
        self.label1.place(relx=0.5,rely=0.1,anchor=CENTER)
        
        # creating the button list 
        self.button = []
        
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        listner = threading.Thread(target=refresh_chatrooms, daemon=True)
        listner.start() 
        broadcast()
        
        time.sleep(5)
        
        # for loop to make buttons and attach them to grid 
        # then the lambda calls the login window and attaches the server name 
        i = 0
        for key in known_chatrooms:
            self.button.append(Button(self.server_list, text = str(key), height = 3, width = 30,
                                      command=lambda key=key: self.login(key)))
            self.button[i].place(relx=0.5,rely=(0.2 + (i/10)),anchor=CENTER)
            i = i + 1
 
    def login(self,servername):
        
        server = Mp(servername)
        
        #gets rid of the server name selection window 
        self.server_list.destroy()
        
        #reveals the login screen
        self.Login.deiconify()
        
        # set the title
        self.Login.title("Login")
        self.Login.resizable(width=False,
                             height=False)
        self.Login.configure(width=400,
                             height=300)
        
        self.servername = Label(self.Login,
                                text =servername,
                                justify=CENTER,
                                font= "Helvetica 14 bold")
        self.servername.place(relheight=0.05,
                              relx=0.2,
                              rely= 0.02)
        # create a Label
        self.pls = Label(self.Login,
                         text="Please login to continue",
                         justify=CENTER,
                         font="Helvetica 14 bold")
 
        self.pls.place(relheight=0.15,
                       relx=0.2,
                       rely=0.07)
        # create a Label
        self.labelName = Label(self.Login,
                               text="Name: ",
                               font="Helvetica 12")
 
        self.labelName.place(relheight=0.2,
                             relx=0.1,
                             rely=0.2)
 
        # create a entry box for
        # tyoing the message
        self.entryName = Entry(self.Login,
                               font="Helvetica 14")
 
        self.entryName.place(relwidth=0.4,
                             relheight=0.12,
                             relx=0.35,
                             rely=0.2)
 
        # set the focus of the cursor
        self.entryName.focus()
 
        # create a Continue Button
        # along with action
        self.go = Button(self.Login,
                         text="CONTINUE",
                         font="Helvetica 14 bold",
                         command=lambda: self.goAhead(self.entryName.get(),servername))
 
        self.go.place(relx=0.4,
                      rely=0.55)
    
 
    def goAhead(self, name, servername=None):
        self.Login.destroy()
        self.Host.destroy()
        self.layout(name,servername)
 
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat
    def layout(self, name, servername=None):
        
        client = Mp(name)
        
        if servername != None:
            server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_socket.bind((self_ip, PORT))
            broadcast_thread = threading.Thread(target=recv_broadcast, args=(servername,), daemon=True)
            broadcast_thread.start()
            server_thread = threading.Thread(
                target=start_server, args=(server_socket,))
            server_thread.start()
            
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect((self_ip, PORT))
            client.join(client_socket, "HOST")
        else:
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client_socket.connect( known_chatrooms[servername], PORT)
            client.join(client_socket, "HOST")
        
        
        message = recieve_all(client_socket).decode(Mp.ENC_TYPE)
        
        head, body = message.split("\n", 1)
        mtype, code, recip, sender = body.split(" ", 3)
        
        # we still need to finish this for making a re login
        if mtype == "DECLINE":
            print("Connection Declined: " + ERRORS[code])
            quit()
            
 
        self.name = name
        # to show chat window
        self.Window.deiconify()
        self.Window.title("CHATROOM")
        self.Window.resizable(width=False,
                              height=False)
        self.Window.configure(width=470,
                              height=550,
                              bg="#17202A")
        self.labelHead = Label(self.Window,
                               bg="#17202A",
                               fg="#EAECEE",
                               text=self.name,
                               font="Helvetica 13 bold",
                               pady=5)
 
        self.labelHead.place(relwidth=1)
        self.line = Label(self.Window,
                          width=450,
                          bg="#ABB2B9")
 
        self.line.place(relwidth=1,
                        rely=0.07,
                        relheight=0.012)
 
        self.textCons = Text(self.Window,
                             width=20,
                             height=2,
                             bg="#17202A",
                             fg="#EAECEE",
                             font="Helvetica 14",
                             padx=5,
                             pady=5)
 
        self.textCons.place(relheight=0.745,
                            relwidth=1,
                            rely=0.08)
 
        self.labelBottom = Label(self.Window,
                                 bg="#ABB2B9",
                                 height=80)
 
        self.labelBottom.place(relwidth=1,
                               rely=0.825)
 
        self.entryMsg = Entry(self.labelBottom,
                              bg="#2C3E50",
                              fg="#EAECEE",
                              font="Helvetica 13")
 
        # place the given widget
        # into the gui window
        self.entryMsg.place(relwidth=0.74,
                            relheight=0.06,
                            rely=0.008,
                            relx=0.011)
 
        self.entryMsg.focus()
 
        # create a Send Button
        self.buttonMsg = Button(self.labelBottom,
                                text="Send",
                                font="Helvetica 10 bold",
                                width=20,
                                bg="#ABB2B9",
                                command=lambda: self.sendButton(self.entryMsg.get()))
 
        self.buttonMsg.place(relx=0.77,
                             rely=0.008,
                             relheight=0.06,
                             relwidth=0.22)
 
        self.textCons.config(cursor="arrow")
 
        # create a scroll bar
        scrollbar = Scrollbar(self.textCons)
 
        # place the scroll bar
        # into the gui window
        scrollbar.place(relheight=1,
                        relx=0.974)
 
        scrollbar.config(command=self.textCons.yview)
 
        self.textCons.config(state=DISABLED)
 
    # function to basically start the thread for sending messages
    def sendButton(self, msg):
        self.textCons.config(state=DISABLED)
        self.msg = msg
        self.entryMsg.delete(0, END)
        snd = threading.Thread(target=self.sendMessage())
        snd.start()
 
    # function to receive messages
    def receive(self):
        i=0
        while i<10:
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, "Breadsticks: Hi"+"\n\n")
 
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)
            i = i + 1
            time.sleep(2)  
        
        
        pass
        
        # while True:
        #     try:
        #         message = client.recv(1024).decode(FORMAT)
 
        #         # if the messages from the server is NAME send the client's name
        #         if message == 'NAME':
        #             client.send(self.name.encode(FORMAT))
        #         else:
        #             # insert messages to text box
        #             self.textCons.config(state=NORMAL)
        #             self.textCons.insert(END,
        #                                  message+"\n\n")
 
        #             self.textCons.config(state=DISABLED)
        #             self.textCons.see(END)
        #     except:
        #         # an error will be printed on the command line or console if there's an error
        #         print("An error occurred!")
        #         client.close()
        #         break
 
    # function to send messages
    def sendMessage(self,):
        
        #self.textCons.config(state=DISABLED)
        message = (f"{self.name}: {self.msg}")
        self.textCons.config(state=NORMAL)
        self.textCons.insert(END, message+"\n\n")
 
        self.textCons.config(state=DISABLED)
        self.textCons.see(END)
        
        # while True:
        #     message = (f"{self.name}: {self.msg}")
        #     client.send(message.encode(FORMAT))
        #     break
 
 
 
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

def recieve_all(conn: socket.socket) -> bytes:
    partial_message = b''
    
    while (b'\n' not in partial_message):
        # the body is constructed by reccuring recv calls
        partial_message += conn.recv(4096)
    return(partial_message)
# recieve_all()

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
 
 
self_ip = socket.gethostbyname(socket.gethostname())
network_setting = None
for inter in neti.interfaces():
    if inter is not None:
        network_setting = neti.ifaddresses(inter).get(neti.AF_INET)
        if network_setting is not None:
            if network_setting[0].get('addr') == self_ip:
                network_setting = network_setting[0]
                break
 
def start_server(socket: socket.socket) -> None:
    socket.listen(5)

    while True:
        conn, addr = socket.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        
def handle_client(conn: socket.socket, addr: str) -> None:
    init_rq = recieve_all(conn).decode(Mp.ENC_TYPE)

    head, body = init_rq.split("\n", 1)
    mtype, code, recip, sender = head.split(" ", 3)

    if mtype != "JOIN":
        server.decline(conn, sender, 400)
        conn.close()
        return

    elif sender in users:
        server.decline(conn, sender, 300)
        conn.close()
        return

    else:
        server.invite(conn, sender)
    
# handle_client()
 
# create a GUI class object
g = Gui()
