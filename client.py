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
}

#LOCAL VARS
ishost = false
displayname = ""
roomname = ""
users = {
    "some user", "some IP or socket or something"
}

def send(mtype: str, recip: str, body: str = None):
    return mtype + " " +\
        displayname + " " +\
        dt.now().strftime("%H:%M") + " " +\
        recip + "/n" +\
        body
# send()

def recieve(message: str):
    head, body = message.split("\n", 1)
    mtype, sender, timestamp, recip = head.split(" ", 3)

    if (mtype == "SEND"):

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
            # reply with send("DECLINE", sender, 100)
            
        else :
            
            if (sender in users.keys):
                # reply with send("DECLINE", sender, 200)

            else if (recip != roomname):
                # reply with send("DECLINE", sender, 102)

            else:
                # reply with send("INVITE", sender)
            # if/else
        # if/else
    
    elif (mtype == "INVITE"):
        # join the chat room
    
    elif (mtype == "DECLINE"):
        print("[DECLINED]: " + Errors[body])
        # do something
    
    else:
        return
    # if/else
        
# recieve()


if __name__ == "__main__":
    return
# main()
