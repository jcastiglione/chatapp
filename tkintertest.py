import tkinter as tk

import socket
import threading
from tkinter import *
from tkinter import font
from tkinter import ttk
import time
 
# import all functions /
#  everything from chat.py file
#from chat import *
 
# PORT = 5050
# SERVER = "192.168.0.103"
# ADDRESS = (SERVER, PORT)
# FORMAT = "utf-8"
 
# # Create a new client socket
# # and connect to the server
# client = socket.socket(socket.AF_INET,
#                        socket.SOCK_STREAM)
# client.connect(ADDRESS)
 
 
# GUI class for the chat
class GUI:
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
        self.host_or_client.configure(width=600,
                                      height=500)
        
        self.label2 = Label(self.host_or_client,
                            text = "Please select host or client ",
                            justify=CENTER,
                            font = "Helvetica 14 bold")
        self.label2.grid (column=0,row = 0, sticky = W)
        
        self.host_button = Button(self.host_or_client, text = "Host",
                                  height = 3, width = 30,
                                  command = self.host)
        
        self.host_button.grid(column=0,row=1,sticky=W)
        
        self.client_button = Button(self.host_or_client, text = "Client",
                                    height=3, width=30,
                                    command=self.server_List)
        
        self.client_button.grid(column=0, row=2,sticky=W)

        
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
                         command=lambda: self.goAhead(self.server_entry.get()))
 
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
        self.label1.grid(column=4, row = 0, sticky=W)
        
        # creating the button list 
        self.button = []
        
        # for loop to make buttons and attach them to grid 
        # then the lambda calls the login window and attaches the server name 
        for i in range(3):
            self.button.append(Button(self.server_list, text = "server name " + str(i+1),height = 3, width = 30,
                                      command=lambda i=i: self.login("servername " + str(i+1))))
            self.button[i].grid(column = 4, row = i+1, sticky=W)
 
    def login(self,servername):
        
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
                         command=lambda: self.goAhead(self.entryName.get()))
 
        self.go.place(relx=0.4,
                      rely=0.55)
    
 
    def goAhead(self, name):
        self.Login.destroy()
        self.layout(name)
 
        # the thread to receive messages
        rcv = threading.Thread(target=self.receive)
        rcv.start()
 
    # The main layout of the chat
    def layout(self, name):
 
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
        snd = threading.Thread(target=self.sendMessage)
        snd.start()
 
    # function to receive messages
    def receive(self):
        i=0
        while i < 10:  
            message = "Breadsticks: hi"
            self.textCons.config(state=NORMAL)
            self.textCons.insert(END, message+"\n\n")
            self.textCons.config(state=DISABLED)
            self.textCons.see(END)
            time.sleep(5)
            i = i + 1
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
    def sendMessage(self):
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
 
 
# create a GUI class object
g = GUI()




# root= tk.Tk()

# canvas1 = tk.Canvas(root, width=400, height=300)
# canvas1.pack()

# entry1 = tk.Entry(root)
# canvas1.create_window(200,140,window=entry1)

# def input():
#     username = entry1.get()
    
#     label1 = tk.Label(root, text=str(username))
#     canvas1.create_window(200, 230, window=label1)
    
# button1 = tk.Button(text='Enter', command=input)
# canvas1.create_window(200,180, window=button1)

# root.mainloop()