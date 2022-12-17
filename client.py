import socket
import os
from datetime import datetime as dt

#CONSTANTS
ERRORS = {
    100: "Recipeint Mismatch",
    101: "Recipeint is not a Host",
    102: "Incorrect Room Name",
    103: "Recipient Not Found",
    200: "Display Name not Available"
    999: "Bad Request"
}

#LOCAL VARS
ishost = false
displayname = "NONE"
roomname = "NONE"
users = {
    "some user", "some IP or socket or something"
}

def send(mtype: str, recip: str, body: str = None) -> str:
    return mtype + " " +\
        displayname + " " +\
        dt.now().strftime("%H:%M") + " " +\
        recip + "/n" +\
        body
# send()

def recieve(message: str) -> None:
    head, body = message.split("\n", 1)
    mtype, sender, timestamp, recip = head.split(" ", 3)

    if (mtype == "SEARCH"):

        if not ishost:
            # reply with ("DECLINE", "ALL", 101)

        else:
            # reply with ("REVEAL", "ALL", roomname)
        # if/else

    elif (mtype == "REVEAL"):

        if ishost:
            # reply with ("DECLINE", sender, 100)

        else:
            print("Room found: " + body)
            # do something
        # if/else

    elif (mtype == "INVITE"):
        # join the chat room
        roomname = body

    elif (mtype == "SEND"):

        if (recip.upper() == "HOST"):
            if not ishost:
                # reply with ("DECLINE", sender, 101)

            else:
                print(timeStamp + "[" + sender + "]: " + body)
    
                for (user in users.key):
                    if (user.key != displayname):
                        # send to user send("SHOW, user, body)
                    # if
                # for
            # if/else
            
        elif (recip not in users.keys):
            # reply with send("DECLINE", sender, 103)

        else:
            # send to recip send("SHOW", user, body)

        # if/else
    
    elif (mtype == "SHOW"):

        if (recip != displayname):
            # reply with send("DECLINE", sender, 102)

        else:
            print(timeStamp + "[" + sender + "]: " + body)
            # do something

        # if/esle
    
    elif (mtype == "JOIN"):
        
        if not ishost:
            # reply with send("DECLINE", sender, 101)
            
        else :
            
            if (sender in users.keys):
                # reply with send("DECLINE", sender, 200)

            else if (recip != roomname):
                # reply with send("DECLINE", sender, 102)

            else:
                # reply with send("INVITE", sender)
            # if/else
        # if/else

    elif (mtype == "DECLINE"):
        print("[DECLINED]: " + Errors[body])
        # do something

    elif (mtype == "DISCONNECT"):

        if not ishost:
            # reply with send("DECLINE", sender, 101)
            
        elif (sender not in users):
            # reply with send("DECLINE", sender, 100)

        else:
            # reply with ("END", sender)
            # close connection with sender

    elif (mtype == "END"):

        if (body != roomname):
            # reply with send("DECLINE", sender, 102)

        else:
            print(timestamp + "[SERVER]: Connection Closed")
            # close connection with server
            # return to main menu?
        # if/else
        
    else:
        # reply with send("DECLINE", sender, 999)
    # if/else
# recieve()

def broadcast() -> None:
    #broadcast to all users asking for chat rooms
    #message is send("SEARCH", "ALL")
# broadcast()

def send_message(msg: str) -> None:

    cmd = None
    body = msg
    
    if (msg.startswith("/"):
        cmd, body = msg.split(" ", 1)
    # if

    if (cmd == "/q"):
        #send to host send("DISCONNECT", "HOST")

    elif (cmd == "/w"):
        recip, body = body.split(" ", 1)

        #send to host send("SEND", recip, body)

    elif (cmd == None):
        #send to host send("SEND", "HOST", body)

    else:
        print(timestamp + "[SERVER]: Incorrect Message Formatting")

    # if/else
# send_message()


if __name__ == "__main__":
    return
# main()
