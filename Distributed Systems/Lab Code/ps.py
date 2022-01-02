"""
Name:Samhitha Nagendla
UTA ID:1001867208
Lab:CSE 5306 Distributed Systems Lab3
Lab Description:
1) A client/Server desktop application that supports minimum 3 Clients connection.
2) Allows user to upload multiple files to check for commonly mis-spelled words using Lexicon file in the server.
3) Allows users to add words to the Lexicon file. 
4) Addition is done by maintaining queues at the client end and for every 60 seconds, the server will poll the input and add the extra new words to the lexicon file.
5) Will connect to the backup server and share the lexicon file udates that it is implementing in its file.That is the new lexicon words that are added to it's lexicon file will be sent to backup server to maintain its replica in the backup server too. 
File Name:ps.py
Purpose: Handles Primary server interactions.
"""

#Reference:https://github.com/isiddheshrao/Distributed-Systems
import datetime
from queue import Queue
import socket
import tkinter as tk
import sys
import threading
from _thread import *
import os
from os import path
import dill
import re
import shutil 
import time
from socket import SHUT_RDWR
#Reference:https://stackoverflow.com/questions/20691258/is-it-possible-in-python-to-kill-process-that-is-listening-on-specific-port-for
from psutil import process_iter
from signal import SIGTERM 






#CREATING CODE FOR UI

#FUNCTION TO HANDLE QUIT
def QUIT(top):
    #Reference:https://stackoverflow.com/questions/20691258/is-it-possible-in-python-to-kill-process-that-is-listening-on-specific-port-for
    #To terminate the process with port number 2345 of connection type tcp if backup server has taken primary server responsibilities.
    
    #Iterates over all processes happening in the system. This will help in checking all the processes.
    for proc in process_iter():
        #Iterates over the tcp connections in the system.This will help in checking the connections of tcp kind.
        for conns in proc.connections(kind='tcp'):
            #Tries to check whether port number of that particular process and particular tcp connection is 2345. As backup server handles primary server responsibilites on 2345 port number.
            if conns.laddr.port == 2345:
                #sends a signal to terminate the process.
                proc.send_signal(SIGTERM) 
    #Destroy the desktop window
    top.destroy()
    #Exits the program.
    sys.exit()


#STATUS OF CLIENTS ON UI
#Reference:https://www.python-course.eu/tkinter_labels.php
#Reference:https://www.python-course.eu/tkinter_layout_management.php
"""In the below tkinter code, we folled a pattern to add widget to the frame, defining the position using place(), where they will be displayed and adding them to the canvas using pack(). Later used config() to addd appropriate text that can be displayed."""
def MAIN_DISPLAY(NULL):
    top = tk.Tk()
    top.title("Primary Server")
    #Setting Up canvas
    main = tk.Canvas(top, height= 500,width= 600)
    main.pack()
    #Dynamic Sizing of Frame
    frame = tk.Frame(main)
    frame.place(relwidth = 1, relheight= 0.9)
    #Quit button code. Triggers the QUIT() function on clicking on it.
    Button1 = tk.Button(frame, text = 'Quit', command = lambda: QUIT(top))
    Button1.place(x=0, y=0)
    Button1.pack()
    #Defined Label to show the clients connected status
    Label1 = tk.Label(frame)
    Label1.place(x=0, y=10)
    Label1.pack()
    #Label to show the title "Total usernames in this session"
    title_label1 = tk.Label(frame)
    title_label1.place(x=0, y=20)
    title_label1.config(text = "Total Usernames in this Session:")
    title_label1.pack()
    #Defined Label to show the total usernames that are connected.
    Label2 = tk.Label(frame)
    Label2.place(x=0, y=30)
    Label2.pack()
    #Label to show the title "Active usernames in this session"
    title_label2 = tk.Label(frame)
    title_label2.place(x=0, y=40)
    title_label2.config(text = "Active Usernames in this Session:")
    title_label2.pack()
    #Defined Label to show the active usernames that are connected.
    Label3 = tk.Label(frame)
    Label3.place(x=0, y=50)
    Label3.pack()
    #Function that will updates the clients connected status.
    UPDATE(Label1,top)
    #Function that will updates the total and active usernames connected.
    SHOW_LIST(top, Label2, Label3)
    top.mainloop()

#CODE TO UPDATE CLIENT STATUS UI IN EVERY 1000MS
def UPDATE(Label1,top):
    global USER_STATUS
    global count
    if USER_STATUS == True:
        PRINT_UI = str(str(count) + " Client(s) Connected")
        Label1.config(text = PRINT_UI)
    else:
        Label1.config(text = "No Client Connected")
    top.after(1000, lambda: UPDATE(Label1, top))

#CODE TO UPDATE USERNAMES AND ACTIVE USERNAMES AND UPDATE EVERY 1000MS
def SHOW_LIST(top, label2, Label3):
    label2.config(text = USERNAMES)
    Label3.config(text = ACTIVE_USERNAMES)
    top.after(1000, lambda: SHOW_LIST(top, label2, Label3))


#CODE FOR THREAD DELETION
def THREAD_DEL():
    #Flag that is used stopping the thread when user disconnects.
    global STOP_CLIENT_THREAD
    #count to keep track of active users.
    global count
    #Changed the status of flag to indicate that it is being closed.
    STOP_CLIENT_THREAD = True
    #Decresed the count as the client is getting disconnected.
    count -=1 #UI UPDATE


#Code for BackupServerLexicon Update
def BACKUP_SERVER_LEXICON_UPDATE(data):
    #Sending the new words to be added to lexicon file maintained by primary server to backup server to maintain the upadtes implemented in the backup server replica.
    bkproc.sendall(str.encode(data))
    

#---------------MAIN CODE---------------------------------#



class ClientThread(threading.Thread):
    #Thread initailization function for every newly added client.
    def __init__(self, ClientAddr, ClientSock):
        threading.Thread.__init__(self) #initialization
        self.csocket = ClientSock       #saving the client socket details that can be later used for sending and recieving messages.
        print("New Client Connection Added from address: ", ClientAddr) #displaying a message that client is connected in terminal.
   

    #FUNCTION TO GET AND CHECK USERNAME
    def USERNAME_CHECK(self):
        #accessing the global clientname that can later be used for creating/accessing buffer files for client server interaction for lexicon addition functionality
        #global clientname
        #accessing the global ACTIVE_USERNAMES that can later be used for updating the queue after client is disconnected.
        global ACTIVE_USERNAMES
        #Initially user falg is set to false that will be changed only on selecting a new username by client.
        USER_FLAG = False
        while not USER_FLAG:
            username = str(self.csocket.recv(4096),'utf-8')   #USERNAME RECVCIEVED FROM SERVER FOR CHECKING.
            #Checking if user name exist or not.
            if (username in USERNAMES) and (username in ACTIVE_USERNAMES):
                message = b"Username Exists and is Active"
                self.csocket.sendall(message)  #SENDING RESPONSE THAT USERNAME EXISTS
                continue
            USER_FLAG = True
        #CHECK IF USERNAME NOT ALREADY IN USERNAME LIST
        if username not in USERNAMES:
            USERNAMES.append(username)
            clientname = username
        #Append the username to list of active users
        ACTIVE_USERNAMES.append(username)
        #user status helps to keep track of currently connected clients.
        global USER_STATUS  #FOR UI UPDATE
        USER_STATUS = True  #FOR UI UPDATE
        #count helps to keep track of number of currently connected clients.
        global count
        count +=1 #FOR UI UPDATE
        #Displays welcome message in the server terminal.
        message = b"Welcome"
        print("Welcome", username)
        #Sents welcome message to client on logging with unique username.
        self.csocket.sendall(message) #SEND 1 USERNAME NEW
        return username

    #Function for client file upload, spell ceheck and sending updated file to client. It also handles closing of client connection.
    def FILE_UPLOAD(self,clientname):
        #Reference:https://www.educative.io/edpresso/what-are-locks-in-python
        lock = threading.Lock()
        while True:
            #Recieves the message from the client.It can be either filepath or client disconnecting message.
            FilePath= str(self.csocket.recv(4096),'utf-8')
            #If we didn't recieved any message then we will keep on waiting for respnse by continuing the loop for next interation.
            if not FilePath :
                continue
            #Reference:https://www.w3schools.com/python/ref_string_endswith.asp
            #To check whether the received message is file path or not.This will return true if it ends with ".txt" indicating the receievd message is file path.
            x = FilePath.endswith(".txt")
            #On checking whether the recieved message is file path, we will proceede with file uplaod and spell check.
            if x :
            #Reference:https://www.geeksforgeeks.org/python-move-or-copy-files-and-directories/
                print(FilePath) #prints file path selected in the terminal.
                shutil.copy2(FilePath, os.getcwd()) #Copies the file to server.
                #Sends a message that file is uploaded to client by converting it into bytes form.
                message =b"File is uploaded" 
                self.csocket.send(message)
                print(FilePath+" is uploaded") #Prints file upload status in terminal.
                #Reference:https://www.w3resource.com/python-exercises/python-basic-exercise-103.php
                #Retrieveing the absolute path of the file.
                FileName = os.path.basename(FilePath)
                #Appending Upd_ to the starting of the return file.
                ReturnFileName = "Upd_" + FileName 
                #Reference:https://stackoverflow.com/questions/49704498/how-do-i-search-if-a-word-exists-in-a-file-in-python
                #reading the inputs of lexicon file and splitting them on occurence of space thereby constructing list of words that exist in the file.
                lexiconfileHandle = open('Lexicon.txt', 'r') 
                lexiconfile = lexiconfileHandle.read()
                lexiconfile = lexiconfile.split()
                #Reference:https://www.geeksforgeeks.org/python-program-to-read-file-word-by-word/
                #opened the client sent file and the return file that server will send.
                with open(FileName,'r') as file, open(ReturnFileName,'w') as retfile :
                # reading each line     
                    for line in file: 
                        updString = ''
                        # reading each word 
                        #Reference:https://stackoverflow.com/questions/36510550/ignore-special-characters-in-file-read
                        for word in re.split(r'\W|\d', line):    
                            # displaying the words            
                            if word.lower() in lexiconfile: #checking whether it exist or not. If exist add braces around it , if not then add the word as it is.
                                updWord = "["+word+"]"
                            else :
                                updWord = word
                            updString = updString +updWord + " " #adding updated word
                        updString = updString +"\n" #after completion of one line adding next line escape character.
                        retfile.write(updString) #Updating the return file .
                #Closing all the opened files as Spell check is completed.
                file.close()
                retfile.close()
                lexiconfileHandle.close()
                #Reference:https://www.geeksforgeeks.org/python-convert-string-to-bytes/
                #Sends the message where the updated file is available.
                message = bytes(ReturnFileName,'utf-8')
                self.csocket.send(message)
            #If the recieved message is not file path.if it is message to close the connection then server update counters,kills the thread handling the interactions
            elif FilePath == "Close Client Connection" :
                #Can be updated by one thread at a time.
                lock.acquire()
                ACTIVE_USERNAMES.remove(clientname)  #REMOVING ACTIVE USERNAME FROM LIST
                lock.release()
                THREAD_DEL() #calling the function to update the flag mainted for status and decrease the count of active connections.
                #closing the buffer files opened for lexicon addition interations.
                if path.exists(clientname+'_pollStatus.txt'):
                    os.remove(clientname+'_pollStatus.txt')
                if path.exists(clientname+'_queueStatus.txt'):
                    os.remove(clientname+'_queueStatus.txt')
                if path.exists(clientname+'_lexiconUploadStatus.txt'):
                    os.remove(clientname+'_lexiconUploadStatus.txt')
                if path.exists(clientname+'_datafile.txt'):
                    os.remove(clientname+'_datafile.txt')
                if STOP_CLIENT_THREAD:  #As flag status is changed it will break the loop.
                    break
                        
        

    #Function to check and update the lexicon additions.
    def POLL_UPDATE(self,clientname):
        #while loop to run continuously.
        #Reference:https://www.educative.io/edpresso/what-are-locks-in-python
        lock = threading.Lock()
        while True:
            #Sleep to check the client queue after every 60 seconds.
            time.sleep(60)
            queueRetrieved = [] # For queue content retrieved.
            updatedString = ''  #For updated words concatenated string.
            pollstat = 'Poll was recieved'; #For updating the poll status.
            #Reference:https://thispointer.com/python-three-ways-to-check-if-a-file-is-empty/
            #Reference:https://www.guru99.com/python-check-if-file-exists.html
            #checks if file exist or not. If no words are added then it won't exist.
            if path.exists(clientname+'_datafile.txt'):
                #checks whether any new words are added to the queue or not.
                if not(os.stat(clientname+'_datafile.txt').st_size == 0) :
                    #load the contents client queue contents retrieved in to a local queue.
                    qrf = open(str(clientname+'_datafile.txt'), 'rb')
                    queueRetrieved = dill.load(qrf)
                    qrf.close() 
                    if ( len(queueRetrieved) > 0):
                        #Update the poll status.
                        with open(str(clientname+'_pollStatus.txt'), 'wb') as ps:
                            dill.dump(pollstat, ps)
                        ps.close()
                        #Update the queue content retrived.
                        with open(str(clientname+'_queueStatus.txt'), 'wb') as qr:
                            dill.dump(queueRetrieved, qr)
                        qr.close()
                        #Reference:https://www.geeksforgeeks.org/python-convert-case-of-elements-in-a-list-of-strings/
                        #converting the case of input words to lower , so the case of inputs will be ignored while retrieving unique values.
                        lst = queueRetrieved
                        queueRetrieved = [x.lower() for x in lst]
                        
                        #Reference:https://www.w3schools.com/python/python_howto_remove_duplicates.asp
                        #Removes duplicate values from the contenst retrieved.
                        queueRetrieved = list( dict.fromkeys(queueRetrieved) )
                        #Locking to prevent simultaneous inconsistent updates.
                        lock.acquire()
                        #Read the contents of lexicon file and split them on occurence of space.
                        lexiconfilecheckHandle = open('Lexicon.txt', 'r') 
                        lexiconfilecheck = lexiconfilecheckHandle.read()
                        lexiconfilecheck = lexiconfilecheck.split()
                        i = 0
                        #Retrieves the queue length for accessing each element one by one using while loop.
                        qslen = len(queueRetrieved)
                        while i < qslen:
                            checkWord = queueRetrieved.pop(0)
                            checkWord = checkWord.lower()   #converts the contents to lower case.
                            #Checks if exist then no action is required 
                            if(checkWord in lexiconfilecheck ):
                                pass
                            #if not then appended to the concatnated string of words.
                            else:
                                updatedString = updatedString +' '+checkWord
                            i = i+1
                        #Closing the lexicon file.
                        lexiconfilecheckHandle.close()
                        #If no new words are added then we won't update lexicon file else update the file with new values.
                        if updatedString == '':
                            pass
                        else :
                        #Reference:https://www.geeksforgeeks.org/python-append-to-a-file/
                            lexiconfileupdateHandle = open('Lexicon.txt', 'a')
                            lexiconfileupdateHandle.write(updatedString)
                            lexiconfileupdateHandle.close()
                            #This function will help in sending the new words to be added to lexicon file to backup server.
                            BACKUP_SERVER_LEXICON_UPDATE(updatedString)
                        #Releasing the lock, so that other users can access the file.
                        lock.release()
                        #If the no new words are added then sens "@@@@" to indicate no new words are added , otherwise send the list of words added.
                        if updatedString == '':
                            updatedString = '@@@@'
                        #Updating the file with status of lexicon update.
                        with open(str(clientname+'_lexiconUploadStatus.txt'), 'wb') as lu:
                            dill.dump(updatedString, lu)
                        lu.close()
                        
                
    def run(self):
        global STOP_CLIENT_THREAD
        clientname = ""
        userdata = self.USERNAME_CHECK() #USERNAME FUNCTION CALL 
#Reference:https://stackoverflow.com/questions/36847817/can-two-infinite-loops-be-ran-at-once/36848028#:~:text=To%20run%20both%20loops%20at,or%20interleave%20the%20loops%20together.&text=While%20Brian's%20answer%20has%20you,True%3A%20%23%20infinite%20loop%20nr.
        #To handle file upload, spell check and connection close
        thread1 = threading.Thread(target=self.FILE_UPLOAD,args=(userdata,))
        thread1.start()
        #To handle lexicon addition
        thread2 = threading.Thread(target=self.POLL_UPDATE,args=(userdata,))
        thread2.start()
        #As we need to handle simultaneously we added two thereads.
        
  
if __name__ == "__main__":
    STOP_CLIENT_THREAD = False
    USER_STATUS = False
    count = 0
    userdata = ''
    USERNAMES = []
    ACTIVE_USERNAMES = []
    HOST = '127.0.0.1'
    PORT = 2345

    NULL = ''
    #Reference:http://net-informations.com/python/net/thread.htm
    try:
        #Setting up socket to accept connections from client users.
        myserver = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        myserver.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Setting up socket for sending upadates of lexicon file, to backup server. 
        print("trying to connect to backup server....")
        bkproc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bkproc.connect(('127.0.0.1', 2346))
        print("connected to backup server.")
        #Binding port used by clients to connect to primary server.
        myserver.bind((HOST,PORT))
        print("Starting Server at HOST: "+ HOST + " and PORT: ", PORT)
        #Thread to handle the updates on Primary server GUI window.
        start_new_thread(MAIN_DISPLAY,(NULL,))
        while True:
            #Primary server listening for max 3 active client connections.
            myserver.listen(3)
            #Accpeting the client connections to establish TCP connection between primary server and client.
            conn, addr = myserver.accept()
            #Thread to handle the responsibilities of lexicon file udate, sharing the updates to backup server, file upload and check for each client.
            newclientthread = ClientThread(addr, conn)
            newclientthread.start()
    #To handle errors araised while creating connections.
    except socket.error as err:  
        print ("Client socket creation failed with error %s" %(err))
    finally:
        myserver.close()