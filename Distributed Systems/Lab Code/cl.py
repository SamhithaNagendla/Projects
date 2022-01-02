"""
Name:Samhitha Nagendla
UTA ID:1001867208
Lab:CSE 5306 Distributed Systems Lab3
Lab Description:
1) A client/Server desktop application that supports minimum 3 Clients connection.
2) Allows user to upload multiple files to check for commonly mis-spelled words using Lexicon file in the server.
3) Allows users to add words to the Lexicon file. 
4) Addition is done by maintaining queues at the client end and for every 60 seconds, the server will poll the input and add the extra new words to the lexicon file.
5) When Primary Server is not responding then it will connect to the backup server and will continue above functionalities.
File Name:cl.py
Purpose: Handles client interaction with the server.
"""

#Reference:https://github.com/isiddheshrao/Distributed-Systems
import socket
import sys
import tkinter as tk
from tkinter import filedialog
import queue
import dill
from threading import *
from datetime import datetime 
import time
import os
from os import path
import shutil
import subprocess


#Reference:https://www.geeksforgeeks.org/socket-programming-python/
#Variables and their initalization
#Sets HOST = '127.0.0.1' as the client process runs on the same machine.
HOST = '127.0.0.1'
#Define the port on which you want to connect .
PORT = 2345
#Queue to store newly added lexicon words.
inq=[]
#To show the queue content.
tq=""
#String to store the Poll status, to dynamically update in the client window.
CLIENT_POLL_STATUS = ''
#String to store the Queue Retrieval status, to dynamically update in the client window.
QUEUE_CONTENT_RETRIEVAL = ''
#String to store the Lexicon upload status, to dynamically update in the client window.
LEXICON_UPLOAD_STATUS = ''
#Flag for Primary Server Response Status.
PRIMARY_SERVER_STAT = True
#Flag for Backup Server Connection status.
BACKUP_SERVER_STAT = False
#Maintains Client Process Socket, useful for re-connecting to backup server for updating the value.
clientproc = 0



#Reference:https://www.geeksforgeeks.org/socket-programming-python/
#Reference:https://realpython.com/python-sockets/
#To establish connection with the server, returns socket, host and port addresses.
def setup():
    global clientproc
    #Try to create and connect client socket.
    try:  
        clientproc = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
        clientproc.connect((HOST, PORT))
        print ("Client socket is successfully created") 
    #To display error on failing to create client socket.
    except socket.error as err:  
        print ("Client socket creation failed with error %s" %(err))   
    return clientproc, HOST, PORT

#Function to get Client User Name, entered in the entry field. Returns the entered client name.
def UI_INPUT(Button, IntVal):
    Button.wait_variable(IntVal)
    INPUT = ClientNameEntry.get()
    #Removing the entered user name.So that if user happens to choose another name then it won't be appended to the existing value.
    ClientNameEntry.delete(0,'end') 
    return INPUT

#Function to check the unique client username. Returns Username and the user name status.
def GET_USERNAME():
    global clientproc
    USERNAME_STATUS = False
    while not USERNAME_STATUS:
        #To Retrieve the Username entered by Client
        username = UI_INPUT(EnterButton,int_var)
        #To send the username to server to check for unique username
        clientproc.send(str.encode(username))
        #Response recieved from the server 
        response = str(clientproc.recv(1024),'utf-8')
        #Checks the response. To update the user if user name exist.
        if response == 'Username Exists and is Active':
            UserNameStatusLabel.config(text="Username is taken and is active.Please enter another username.")            
            continue
        #if user name is available then the user status will be set to true.
        USERNAME_STATUS = True
    return USERNAME_STATUS, username
    
#Reference:https://stackoverflow.com/questions/57394016/browsing-file-and-getting-filepath-in-entrybox-in-tkinter    
# Function for opening the file explorer window, to browse the file.
def browseFiles():
    #Specifying the file browser window opened to select Text Files by default.
    filename = filedialog.askopenfilename(filetypes = (("Text files","*.txt*"),))
    #Insert the selected file name in the entry field in the client window.
    fileEntry.insert(tk.END,filename) 
    #Displays the message showing which file is selected.
    browsedFileLabel.config(text =str(filename+" is selected."))
    
#Reference:https://stackoverflow.com/questions/57394016/browsing-file-and-getting-filepath-in-entrybox-in-tkinter 
#Function to Upload the File to the server.
def FILE_UPLOAD():
    global clientproc
    #getting the file selected.
    filepath = fileEntry.get()
    #sending the selected file location.
    clientproc.sendall(str.encode(filepath))
    #Checking the response of the file upload.
    fileuploadresponse = str(clientproc.recv(1024),'utf-8')
    #Displaying the status of the file upload.
    fileUploadStatusLabel.config(text = fileuploadresponse)
    #Checking for mis-spelled words check response.
    lexiconsearchresponse = str(clientproc.recv(1024),'utf-8') 
    #Retrieving the updated file name from the response received from the server.
    updFile = lexiconsearchresponse
    #Reference:https://www.geeksforgeeks.org/create-a-directory-in-python/
    #Reference:https://www.tutorialspoint.com/How-can-I-create-a-directory-if-it-does-not-exist-using-Python
    #Defining the path of target directory for saving results.
    targetDirectory = os.path.join(os.getcwd(), 'results')
    #Checks if the target directory exists, if not then create it.
    if not os.path.exists(targetDirectory):
        os.makedirs(targetDirectory)
    #Copies the file from Server to client.
    shutil.copy2(updFile, targetDirectory)
    #Composed the message to be displayed on the client window.
    msg = updFile + " is recieved from the server after spell-check. It is available in the current directory, sub-folder results."
    #Displaying the updated file details, receievd from server after checking for mis-spelled words on the client window.
    spellCheckStatusLabel.config(text = msg)   
    #Removing the selected file entry. So that it won't get appended to the file that will be selected later.
    fileEntry.delete(0,'end')

#Reference:https://www.geeksforgeeks.org/queue-in-python/
#Reference:https://pythontic.com/queue-module/queue-class/empty
#Function to upload the entered words for lexicon addition into the Queue.
def WORD_UPLOAD():
#Instead of sending the queue continuously, we are maintaing the queue contents in a buffer file that can be accessed by the server when it is ready to access.
#It avoided blocking the process by sending multiple requests and waiting for action, by maintaing buffer file that can be accessed when server is ready.
#These buffer files are accessible by both client and server, there by avoiding the blocking of it, from carrying out other tasks. 
    #To retrieve the word entered in the lexicon words entry field.
    wordEntered = lexiconWordEntry.get()
    #Appending word entered to queue.
    inq.append(wordEntered)
    #Removing the entry field data. So that next word entered won't be appended to the existing one.
    lexiconWordEntry.delete(0,'end')
    #Reference:https://www.programcreek.com/python/example/95968/dill.dump  
    #Dumping the queue contents to username+'_datafile.txt'. So that server can check this file to retrieve the queue contents.
    with open(str(username+'_datafile.txt'), 'wb') as tmp:
        dill.dump(inq, tmp)
    tmp.close()
    #Updating the tq string to show the contents of queue in the client window.
    tq = "Contents of the Queue maintained by client : "+str(inq)
    #Displaying the contents of queue in the client window.
    queueContentLabel.config(text = tq)

    
    
#Function to update CLIENT_POLL_STATUS,QUEUE_CONTENT_RETRIEVAL AND LEXICON_UPLOAD_STATUS values for every 10secs.To display the status messages in the client window.
def UPDATE(window, clientPollStatusLabel, qContentRetrivedLabel,lexiconUploadStatusLabel):
#Instead of waiting for the responses from server when the queue is polled, we are using buffer files for updating the responses.
#These buffer files are accessible by both client and server, there by avoiding the blocking of it, from carrying out other tasks. 
        # username+'_pollStatus.txt'file maintains the server poll response.
        #Checking if the username+'_pollStatus.txt'file exist. It will be available only if the client queue is polled atleast once.
        if path.exists(username+'_pollStatus.txt'):
            #checks if the file is not empty. This will help us to avoid the cases where no new words are added to the queue after the queue is polled earlier.
            if not(os.stat(username+'_pollStatus.txt').st_size == 0) :
                #Opening the file to load the poll response of the server.
                cps = open(str(username+'_pollStatus.txt'), 'rb')
                CLIENT_POLL_STATUS = dill.load(cps)
                cps.close()
                #Formatting the message to be displayed on the client window.
                CLIENT_POLL_STATUS = str("Server Poll Response: "+CLIENT_POLL_STATUS)
                #Displaying the message on the client window.
                clientPollStatusLabel.config(text = CLIENT_POLL_STATUS)
                #removing the contents of the poll buffer file to avoid the confusion and to track the next time the client is polled.
                cpsupd = ''
                cps = open(str(username+'_pollStatus.txt'), 'wb')
                dill.dump(cpsupd,cps)
                cps.close()
                # username+'_queueStatus.txt' file maintains the contents of the queue retrieved by the server.
                #Checking if the username+'_queueStatus.txt' file exist.It will exist only when new words are added to the queue and the queue is polled by server. 
                if path.exists(username+'_queueStatus.txt'):
                    #checks if the file is not empty.It helps to avoid the cases where new words are not added after the content of queue is polled once.
                    if not(os.stat(username+'_queueStatus.txt').st_size == 0) :
                        #Opening the file to load the server response about the contents of the queue retrieved and assigning it to the variable maintained
                        qcr = open(str(username+'_queueStatus.txt'), 'rb')
                        QUEUE_CONTENT_RETRIEVAL = dill.load(qcr)
                        qcr.close()
                        #Emptying the buffer file as the contents are retrieved.
                        qrs = open(str(username+'_queueStatus.txt'), 'wb')
                        dill.dump(cpsupd,qrs)
                        qrs.close()
                        if ( len(QUEUE_CONTENT_RETRIEVAL) > 0):
                            #Checking the length of the queue retrieved by the server.
                            qrsize = len(QUEUE_CONTENT_RETRIEVAL)
                            #Interator variable to track the number of items poped from the queue.
                            i = 0
                            #Accessing the client queue.
                            global inq
                            """Iterates through the length of the queue contents retrieved by the server and will remove those items from the existing client queue."""
                            while i < qrsize and len(inq) > 0:
                                inq.pop(0) #Removing the first element in the existing list.
                                i = i+1    #Incrementing the counter as one element/item is removed from the existing client queue.
                            #Once the client queue is updated, the buffer file maintained for the saving contents of the queue is updated.
                            with open(str(username+'_datafile.txt'), 'wb') as tmp:
                                dill.dump(inq, tmp)
                            tmp.close()
                            #Formatting the existing client queue contents message, after being retrieved by the server.
                            tq ="Contents of the Queue maintained by client : "+str(inq) 
                            #Displaying the existing client queue contents, after being retrived by the server, message on the client window.
                            queueContentLabel.config(text = tq) 
                            #Formatting the queue contents retrieved by the server message to be displayed on the client window.
                            qrstat = "Contenets of Queue retrieved by server : " +str(QUEUE_CONTENT_RETRIEVAL)
                            #Displaying the queue contents retrieved by the server message on the client window
                            qContentRetrivedLabel.config(text = qrstat)
                            #username+'_lexiconUploadStatus.txt' file maintains the words uploaded to the server.
                            #Checks if the file exist or not. File will exist only once the client queue is polled once.
                            if path.exists(username+'_lexiconUploadStatus.txt'):
                            #Checks if file is not empty.It helps to avoid the cases where new words are not added after the content of queue is polled once.
                                if not(os.stat(username+'_lexiconUploadStatus.txt').st_size == 0) :
                                #Loading the response after updating the lexicon file.
                                    lus = open(str(username+'_lexiconUploadStatus.txt'), 'rb')
                                    LEXICON_UPLOAD_STATUS = dill.load(lus)
                                    lus.close()
                                    #Emptying the buffer as the contents are retrieved.
                                    lupf = open(str(username+'_lexiconUploadStatus.txt'), 'wb')
                                    dill.dump(cpsupd,lupf)
                                    lupf.close()
                                    #Reference:https://www.tutorialspoint.com/python/python_lists.htm
                                    #"@@@@" response will be added if no new words are added to the lexicon file.If already existing words are passed through client GUI.
                                    if LEXICON_UPLOAD_STATUS == '@@@@':
                                    #Formatting the message to display no new words are added.
                                        LEXICON_UPLOAD_STATUS = "No new words are added to Lexicon file"
                                        #Displaying the message on the client window.
                                        lexiconUploadStatusLabel.config(text = LEXICON_UPLOAD_STATUS)
                                    else: 
                                        #Formatting the message to show which words are added to lexicon file.
                                        LEXICON_UPLOAD_STATUS = str("Words added to lexicon file : "+LEXICON_UPLOAD_STATUS)
                                        #Displaying the response on client window.
                                        lexiconUploadStatusLabel.config(text = LEXICON_UPLOAD_STATUS)
        #To trigger this function for every 10 secs to update the contents of the file.                        
        window.after(60000, lambda: UPDATE(window, clientPollStatusLabel, qContentRetrivedLabel,lexiconUploadStatusLabel))
        
        
#Reference:https://stackoverflow.com/questions/14110841/how-do-i-test-if-there-is-a-server-open-on-a-port-with-python
#Reference:https://stackoverflow.com/questions/35375585/call-subprocess-ls-l-folder-wc-l-in-python-cant-be-done
#Reference:https://geekflare.com/netstat-command-usage-on-windows/     
#Function to check Primary Server status whether it is responding or not for every 100ms
#window, PrimaryServerStatus are passed as arguments to update the Primary server status label in the client window.
def PS_STAT_CHECK(window, PrimaryServerStatus):
    #Flag to indicate whether primary server is responding or not.
    global PRIMARY_SERVER_STAT
    #If Primary Server flag was true(responding) then we will try to check whether it is still responding.If not then it will display primary server is not responding message in the client window.It will try to connect to backup server and will not check the response further.
    if PRIMARY_SERVER_STAT == True:
        try:
            #We are trying to execute "netstat -a |findstr 127.0.0.1.2345" windows command to check the status of Primary Server "127.0.0.1.2345", to conclude whether server is responding or not.
            tn = subprocess.call("netstat -a |findstr 127.0.0.1.2345",shell=True)
            #If no netstat of Primary Server(127.0.0.1.2345) is returned then it will return 1 in other cases it will return 0.
            #Below condition is satisfied if the server is unavailable.
            if tn == 1:
                print("Failed! Primary server is unavailable") 
                #Updating the flag to indicate the primary server is not responding. It can be used to initiate the backup connection.
                PRIMARY_SERVER_STAT = False
                #Displaying the message that Primary server is not responding in the client window.
                PrimaryServerStatus.config(text = "Primary Server is not responding")                
        except:
            print("Exception in checking the Primary Server Status")
        #To trigger this function after 100ms as the primary server is still responding and check the status periodically to find when Primary server stopped responding.
        window.after(100, lambda: PS_STAT_CHECK(window, PrimaryServerStatus))
           
#Function to check the unique client username with backup server. Returns Username and the user name status.
def SEND_USERNAME():
    global clientproc
    USERNAME_STATUS = False
    while not USERNAME_STATUS:
        #To send the username to backup-server to check for unique username
        clientproc.send(str.encode(username))
        #Response recieved from the backup-server 
        response = str(clientproc.recv(1024),'utf-8')
        #Checks the response. To update the user if user name exist.
        if response == 'Username Exists and is Active':
            UserNameStatusLabel.config(text="Username is taken and is active.Please enter another username.")            
            continue
        #if user name is available then the user status will be set to true.
        USERNAME_STATUS = True
    return USERNAME_STATUS, username
  
#Function to connect to backup server by checking falg that indicates the primary server responding or not for every 100ms.
def BK_SETUP_CONNECTION(window, BackupServerConnectionStatus):
    #To update the back-up server status flag after establishing connection. Can be used to control the loop. If the status is true then the loop will end as the client is successfully connected to the backup server and there is no need to try reconnect to the backup server again.
    global BACKUP_SERVER_STAT
    #To update the Client process socket value after switching connection to backup value.
    global clientproc
    #When Primary server stops responding then PRIMARY_SERVER_STAT will be false. So, we will try to connect to backup server.
    if PRIMARY_SERVER_STAT == False:
        #As we are trying to execute a system command using subprocess.call(), we are using try to handle exceptions.
        try:
            #We are trying to execute "netstat -a |findstr 127.0.0.1.2345" windows command to check the status of back-up Server "127.0.0.1.2345", to identify whether the backup server realised that primary server is unavailable and taken responsibility to handle the Primary Server responsibilities.
            tn = subprocess.call("netstat -a |findstr 127.0.0.1.2345",shell=True)
            if tn == 0:
                #Retrieving the setup details used for backup server communication.
                clientproc, HOST, PORT = setup()
                print("Tried to connect to backup server")
                #To retrieve user status after sending username to backup server.
                USERNAME_STATUS, username = SEND_USERNAME() 
                #On successfully sending username, we will display the message that connection switch is completed.
                if USERNAME_STATUS:
                    #To display "Connection is switched to backup server" message in the client window as it reconnected and shared its user details.
                    BackupServerConnectionStatus.config(text = "Connection is switched to backup server")
                #Updated the flag as the connection switch is completed. This falg is used to stop calling this function again.
                BACKUP_SERVER_STAT = True   
        #To diaplay a message indicating occurence of error when checking for availability of backup server.
        except:
            print("Exception when checking availability of backup server")  
    #If backup server switch is not completed then this fuction is called after 100ms to connect to backup server if the primary server stopped responding.
    if BACKUP_SERVER_STAT == False:
        #Calling the same function after 100 ms to check periodically. And to connect to backup server if primary server is not responding.
        window.after(100, lambda: BK_SETUP_CONNECTION(window, BackupServerConnectionStatus))  


#Function to Close the client Process
#Reference:https://www.codegrepper.com/code-examples/python/check+if+variable+is+undefined+python
def QUIT(window):
#Removes all the buffer files maintained by the existing user to avoid confusion if another user with same name connects after the existing client disconnects.
    global clientproc
    try:
        USERNAME_STATUS
        #sends a message to the server that the client is getting disconnected.
        clientproc.sendall(str.encode("Close Client Connection"))
    except:
        if path.exists(username+'_pollStatus.txt'):
            os.remove(username+'_pollStatus.txt')
        if path.exists(username+'_queueStatus.txt'):
            os.remove(username+'_queueStatus.txt')
        if path.exists(username+'_lexiconUploadStatus.txt'):
           os.remove(username+'_lexiconUploadStatus.txt')
        if path.exists(username+'_datafile.txt'):
           os.remove(username+'_datafile.txt')
        time.sleep(1)
        window.destroy()
        sys.exit(0)
    else:
        if path.exists(username+'_pollStatus.txt'):
            os.remove(username+'_pollStatus.txt')
        if path.exists(username+'_queueStatus.txt'):
            os.remove(username+'_queueStatus.txt')
        if path.exists(username+'_lexiconUploadStatus.txt'):
           os.remove(username+'_lexiconUploadStatus.txt')
        if path.exists(username+'_datafile.txt'):
           os.remove(username+'_datafile.txt')
        time.sleep(1)
        window.destroy()
    


#Reference:https://www.python-course.eu/tkinter_labels.php
#Reference:https://www.tutorialsteacher.com/python/create-gui-using-tkinter-python
#Code for Client Application Window Display
"""In the below tkinter code, we folled a pattern to add widget to the frame, defining the position using place(), where they will be displayed and adding them to the canvas using pack(). Later used config() to addd appropriate text that can be displayed."""
window = tk.Tk()
window.title("Client")
int_var = tk.IntVar()
#Setting Up canvas
main = tk.Canvas(window, height = 800, width = 900)
main.pack()
#Dynamic Sizing of Frame
frame = tk.Frame(main)
frame.place(relwidth = 1, relheight = 0.9)
#Retrieving the setup details
clientproc, HOST, PORT = setup()


#Label to enter UserName
ClientNameLabel = tk.Label(frame)
ClientNameLabel.config(text = "Enter Your Username:")
ClientNameLabel.place(x=10, y=80)
ClientNameLabel.pack()
#Entry for Client Name
ClientNameEntry = tk.Entry(frame)
ClientNameEntry.place(x=20, y=80)
ClientNameEntry.pack()
#Enter Button Setup
EnterButton = tk.Button(frame, text = 'Enter', command = lambda: int_var.set(1))
EnterButton.place(x=10, y=100)
EnterButton.pack()
#Status of Client Name
UserNameStatusLabel = tk.Label(frame)
UserNameStatusLabel.place(x=10, y=90)
UserNameStatusLabel.pack() 
#To display user status after user is connected.
USERNAME_STATUS, username = GET_USERNAME() 
if USERNAME_STATUS:
    UserNameStatusLabel.config(text=str("Client "+username+" has been connected"))
window.title(username+" - Client")

#Reference:https://www.geeksforgeeks.org/file-explorer-in-python-using-tkinter/
# Create a File Explorer label
fileExplorerLabel = tk.Label(frame, text = "Please select the file to upload")
fileExplorerLabel.place(x=10, y=150)
fileExplorerLabel.pack() 
#Create an entry for file to be selected
fileEntry = tk.Entry(frame)
fileEntry.place(x=10, y=160)
fileEntry.pack()
#Browse File button code.Triggers browseFiles() function on clicking on it.Helps in browsing the file.
button_explore = tk.Button(frame,text = 'Browse File',command = lambda: browseFiles()) 
button_explore.place(x=10, y=170)
button_explore.pack()
#Displays messge to select the file to upload label.
browsedFileLabel = tk.Label(frame, text = "Please select the file to upload")
browsedFileLabel.place(x=10, y=180)
browsedFileLabel.pack() 
#Upload file Button code. Triggers FILE_UPLOAD() function on clicking on it.Helps in uploading the files.
UploadButton = tk.Button(frame,text = 'upload File',command = lambda: FILE_UPLOAD())
UploadButton.place(x=10, y=190)
UploadButton.pack()
#upload file status
fileUploadStatusLabel = tk.Label(frame)
fileUploadStatusLabel.place(x=10, y=200)
fileUploadStatusLabel.pack() 
#Spell check status
spellCheckStatusLabel = tk.Label(frame)
spellCheckStatusLabel.place(x=10, y=210)
spellCheckStatusLabel.pack() 

#Label to enter words to Lexicon File
lexiconWordLabel = tk.Label(frame)
lexiconWordLabel.config(text = "Enter words to be added to lexicon file in the server:")
lexiconWordLabel.place(x=10, y=260)
lexiconWordLabel.pack()
#Entry for words to Lexicon File
lexiconWordEntry = tk.Entry(frame)
lexiconWordEntry.place(x=10, y=270)
lexiconWordEntry.pack()
#Queue Content 
queueContentLabel = tk.Label(frame)
queueContentLabel.place(x=10, y=290)
queueContentLabel.pack()
#Submit Button Setup. Triggers the WORD_UPLOAD() function on clicking on it.That adds word to queue.
SubmitButton = tk.Button(frame, text = 'Submit', command = lambda: WORD_UPLOAD())
SubmitButton.place(x=10, y=280)
SubmitButton.pack()
#Client Polling status
clientPollStatusLabel = tk.Label(frame)
clientPollStatusLabel.place(x=10, y=320)
clientPollStatusLabel.pack()
#Queue Contents Retrieved by server
qContentRetrivedLabel = tk.Label(frame)
qContentRetrivedLabel.place(x=10, y=330)
qContentRetrivedLabel.pack()
#Lexicon Word Upload status
lexiconUploadStatusLabel = tk.Label(frame)
lexiconUploadStatusLabel.place(x=10, y=360)
lexiconUploadStatusLabel.pack()

#Quit button code. Triggers the QUIT() function on clicking on it.
QuitButton = tk.Button(frame, text = 'Quit', command = lambda: QUIT(window))
QuitButton.place(x=10, y=390)
QuitButton.pack()

#Label to display primary server response status
PrimaryServerStatus = tk.Label(frame)
PrimaryServerStatus.place(x=10, y=420)
PrimaryServerStatus.pack()
#Label to display backup server connection setup status
BackupServerConnectionStatus = tk.Label(frame)
BackupServerConnectionStatus.place(x=10, y=430)
BackupServerConnectionStatus.pack()
#Calling the PS_STAT_CHECK function to check the status of primary server.
PS_STAT_CHECK(window, PrimaryServerStatus)
#Calling the BK_SETUP_CONNECTION function to switch connection to backup server.
BK_SETUP_CONNECTION(window, BackupServerConnectionStatus)


#calling the update function that can update the status of Lexicon words addition to the file available in the server.
UPDATE(window, clientPollStatusLabel, qContentRetrivedLabel,lexiconUploadStatusLabel)

window.mainloop()
