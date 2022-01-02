"""
Assignment 11:Input Validation
References:
1)https://stackoverflow.com/questions/38579725/return-string-with-first-match-regex
2)https://www.w3schools.com/python/python_regex.asp
3)https://www.geeksforgeeks.org/command-line-arguments-in-python/
4)https://en.wikipedia.org/w/index.php?title=Category:Area_codes_in_the_United_States&pagefrom=734%0AArea+code+734#mw-pages
5)https://likegeeks.com/python-sqlite3-tutorial/
6)https://pynative.com/python-sqlite-delete-from-table/
7)https://www.sqlitetutorial.net/sqlite-python/delete/
8)https://python.plainenglish.io/python-file-handling-97e967dce091
9)https://www.geeksforgeeks.org/get-current-timestamp-using-python/
10)https://stackoverflow.com/questions/36745577/how-do-you-create-in-python-a-file-with-permissions-other-users-can-write
11)https://www.tutorialspoint.com/python/os_chown.htm#:~:text=Python%20method%20chown()%20changes,would%20need%20super%20user%20privilege..
12)https://www.geeksforgeeks.org/command-line-arguments-in-python/
"""

import sys
import re
import os
import sqlite3
from sqlite3 import Error
import datetime

#checks First name.
def First_Name(firstname):
    try:
        first_name_match = re.search("^[A-Z][a-z]+",firstname)
        return first_name_match.group(0)
    except:
        return ''

#Checks Middle Name.    
def Middle_Name(middlename):
    try:
        middle_name_match = re.search("^[A-Z][a-z]+",middlename)
        return middle_name_match.group(0)
    except:
        return ''

#checks for middle name/ Initial.    
def MI(mi):
    try:
        if(len(mi) == 2):
            mii_match = re.search("^[A-Z]\.",mi)
            return mii_match.group(0)
        else:
            miname_match = re.search("^[A-Z][a-z]+",mi) 
            return miname_match.group(0)
    except:
        return ''

#checks for validity of last name.        
def Last_Name_first(lastname):
    try:
        last_name_first_sd_match = re.search("^[A-Z]\'[A-Z][a-z]+\-[A-Z][a-z]+\,",lastname)
        return last_name_first_sd_match.group(0)
    except:
        try:
            last_name_first_s_match = re.search("^[A-Z]\'[A-Z][a-z]+\,",lastname)
            return last_name_first_s_match.group(0)
        except:
            try:
                last_name_first_match = re.search("^[A-Z][a-z]+\,",lastname)
                return last_name_first_match.group(0)
            except:
                return ''

#Checks for validity of last name.        
def Last_Name_last(lastname):
    try:
        last_name_last_sd_match = re.search("^[A-Z]\'[A-Z][a-z]+\-[A-Z][a-z]+",lastname)
        return last_name_last_sd_match.group(0)
    except:
        try:
            last_name_last_s_match = re.search("^[A-Z]\'[A-Z][a-z]+",lastname)
            return last_name_last_s_match.group(0)
        except:
            try:
                last_name_last_match = re.search("^[A-Z][a-z]+",lastname)
                return last_name_last_match.group(0)
            except:
                return ''

#Checks whether name is valid or not.                
def Full_Name_check(fullname):
    if( len(fullname.split(' ')) == 3 and len(fullname.split(',')) == 1):
        firstname, middlename, lastname = fullname.split(' ')
        firstname_check = First_Name(firstname)
        middlename_check = Middle_Name(middlename)
        lastname_check= Last_Name_last(lastname)
        if (firstname == firstname_check) and (middlename == middlename_check) and (lastname == lastname_check):
            return "Valid Format"
        else:
            return "Invalid Format"
  
    elif( len(fullname.split(' ')) == 2 and len(fullname.split(',')) == 1):
        firstname, lastname = fullname.split(' ')
        firstname_check = First_Name(firstname)
        lastname_check = Last_Name_last(lastname)
        if (firstname == firstname_check) and (lastname == lastname_check):
            return "Valid Format"
        else:
            return "Invalid Format"

    elif( len(fullname.split(' ')) == 3 and len(fullname.split(',')) == 2):
        lastname, firstname, mi = fullname.split(' ')
        firstname_check = First_Name(firstname)
        mi_check = MI(mi)
        lastname_check = Last_Name_first(lastname)
        if (firstname == firstname_check) and ( mi == mi_check) and (lastname == lastname_check):
            return "Valid Format"
        else:
            return "Invalid Format"
      
    elif( len(fullname.split(' ')) == 2 and len(fullname.split(',')) == 2):
        lastname, firstname = fullname.split(' ')
        firstname_check = First_Name(firstname)
        lastname_check = Last_Name_first(lastname)
        if (firstname == firstname_check) and (lastname == lastname_check):
            return "Valid Format"
        else:
            return "Invalid Format"
    
    elif( len(fullname.split(' ')) == 1 and len(fullname.split(',')) == 1):
        firstname = fullname
        firstname_check = First_Name(firstname)
        if (firstname == firstname_check):
            return "Valid Format"
        else:
            return "Invalid Format"

    else:
        return "Invalid Format"

#chceks for the valid format of number passed.
def Contact_Number_m17(cno):
    try:
        cno_match = re.search("^[0][1][1]\s[1-9][0-9]\s\([1-9][0-9]{2}\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^[0][0]\s[1-9][0-9]\s\([1-9][0-9]{2}\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[0][1][1]\s[1-9][0-9]\s\([1-9][0-9]\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[0][0]\s[1-9][0-9]\s\([1-9][0-9]\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^\+[1-9][0-9]\s\([1-9][0-9]{2}\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[0][1][1]\s[1]\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[0][1][1]\s[1]\-[2-9][0-8][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^[0][1][1]\s[1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^[0][1][1]\s[1]\.[2-9][0-8][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                        return cno_match.group(0)
                                    except:
                                        try:
                                            cno_match = re.search("^[0][1][1]\s[4][5]\s[1-9][0-9]\s[0-9]{2}\s[0-9]{2}\s[0-9]{2}",cno)
                                            return cno_match.group(0)
                                        except:
                                            try:
                                                cno_match = re.search("^[0][1][1]\s[4][5]\s[1-9][0-9]\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}",cno)
                                                return cno_match.group(0)
                                            except:
                                                return Contact_Number_17(cno)

 
def Contact_Number_17(cno):
    try:
        cno_match = re.search("^[0][1][1]\s[1]\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^[0][1][1]\s[1]\-[1-9][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[0][1][1]\s[1]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[0][1][1]\s[1]\.[1-9][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^[0][0]\s[1]\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[0][0]\s[1]\-[2-9][0-8][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[0][0]\s[1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^[0][0]\s[1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^[0][0]\s[1]\.[2-9][0-8][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                        return cno_match.group(0)
                                    except:
                                        try:
                                            cno_match = re.search("^[0][0]\s[4][5]\s[1-9][0-9]\s[0-9]{2}\s[0-9]{2}\s[0-9]{2}",cno)
                                            return cno_match.group(0)
                                        except:
                                            try:
                                                cno_match = re.search("^[0][0]\s[4][5]\s[1-9][0-9]\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}",cno)
                                                return cno_match.group(0)
                                            except:
                                                try:
                                                    cno_match = re.search("^\+[1-9][0-9]{1}\s\([1-9][0-9]\)\s[1-9][0-9]{2}\-[0-9]{4}",cno)
                                                    return cno_match.group(0)
                                                except:
                                                    return Contact_Number_16(cno)

def Contact_Number_16(cno):
    try:
        cno_match = re.search("^[0][0]\s[1]\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^[0][0]\s[1]\-[1-9][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[0][0]\s[1]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[0][0]\s[1]\.[1-9][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^[0][1][1]\s[4][5]\s[1-9][0-9]{3}\s[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[0][1][1]\s[4][5]\s[1-9][0-9]{3}\.[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[0][1][1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                return Contact_Number_15(cno)

def Contact_Number_15(cno):
    try:
        cno_match = re.search("^[0][1][1]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^[0][0]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[0][0]\s[4][5]\s[1-9][0-9]{3}\s[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[0][0]\s[4][5]\s[1-9][0-9]{3}\.[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^\+[4][5]\s[1-9][0-9]\s[0-9]{2}\s[0-9]{2}\s[0-9]{2}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^\+[4][5]\s[1-9][0-9]\.[0-9]{2}\.[0-9]{2}\.[0-9]{2}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^\+[1]\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^\+[1]\-[2-9][0-8][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^\+[1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                        return cno_match.group(0)
                                    except:
                                        try:
                                            cno_match = re.search("^\+[1]\.[2-9][0-8][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                            return cno_match.group(0)
                                        except:
                                            return Contact_Number_14(cno)

def Contact_Number_14(cno):
    try:
        cno_match = re.search("^\+[1]\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^\+[1]\-[1-9][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^\+[1]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^\+[1]\.[1-9][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^[0][0]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[1]\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[1]\-[2-9][0-8][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^[1]\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^[1]\s[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                        return cno_match.group(0)
                                    except:
                                        try:
                                            cno_match = re.search("^[1]\.[2-9][0-8][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                            return cno_match.group(0)
                                        except:
                                            return Contact_Number_13(cno)

def Contact_Number_13(cno):
    try:
        cno_match = re.search("^\+[4][5]\s[1-9][0-9]{3}\s[0-9]{4}",cno)
        return cno_match.group(0)
    except:
        try:
            cno_match = re.search("^\+[4][5]\s[1-9][0-9]{3}\.[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[1]\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[1]\-[1-9][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^[1]\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[1]\s[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[1]\.[1-9][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^\([2-9][0-8][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^\+[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                                        return cno_match.group(0)                                   
                                    except:
                                        return Contact_Number_l13(cno)
                                
def Contact_Number_l13(cno):
    try:
        cno_match = re.search("^\+[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
        return cno_match.group(0)                                   
    except:
        try:
            cno_match = re.search("^\([1-9][0-9]\)[1-9][0-9]{2}\-[0-9]{4}",cno)
            return cno_match.group(0)
        except:
            try:
                cno_match = re.search("^[2-9][0-8][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                return cno_match.group(0)
            except:
                try:
                    cno_match = re.search("^[2-9][0-8][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                    return cno_match.group(0)
                except:
                    try:
                        cno_match = re.search("^[2-9][0-8][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                        return cno_match.group(0)
                    except:
                        try:
                            cno_match = re.search("^[1-9][0-9]\s[1-9][0-9]{2}\s[0-9]{4}",cno)
                            return cno_match.group(0)
                        except:
                            try:
                                cno_match = re.search("^[1-9][0-9]\.[1-9][0-9]{2}\.[0-9]{4}",cno)
                                return cno_match.group(0)
                            except:
                                try:
                                    cno_match = re.search("^[1-9][0-9]\-[1-9][0-9]{2}\-[0-9]{4}",cno)
                                    return cno_match.group(0)
                                except:
                                    try:
                                        cno_match = re.search("^[1-9][0-9]{4}\.[0-9]{5}",cno)
                                        return cno_match.group(0)
                                    except:
                                        try:
                                            cno_match = re.search("^[1-9][0-9]{4}\s[0-9]{5}",cno)
                                            return cno_match.group(0)
                                        except:
                                            try:
                                                cno_match = re.search("^[1-9][0-9]{2}\-[0-9]{4}",cno)
                                                return cno_match.group(0)
                                            except:
                                                try:
                                                    cno_match = re.search("^[1-9][0-9]{4}",cno)
                                                    return cno_match.group(0)
                                                except:
                                                    return ''

#Checks if it is a avlid command or not.
def Command_check(command_input):
    if (len(command_input) < 5 and len(command_input) > 2 and command_input.isalpha()):
        if( command_input == "ADD" or command_input == "DEL" or command_input == "LIST") :
            return "Valid Command"
        else:
            return "Inavlid Command entered"
    else:
        print("Valid Commands are ADD, DEL and LIST alone")
        return "Inavlid Command entered"
    
#Creating connection to database.    
def sql_connection():
    try:
        con = sqlite3.connect('mydatabase.db')
        return con
    except Error:
        print(Error)
        sys.exit(1)

#Creates a table if does not exist to maintain records of telephone directory.
def sql_table(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('create table if not exists telephone(name VARCHAR[120], ContactNumber VARCHAR[21])')
        con.commit()
    except Error:
        print(Error)
        con.close()
        sys.exit(1)

#Code to insert the records to telephone directory.
def sql_insert(con, insert_entities):
    try:
        cursorObj = con.cursor()    
        cursorObj.execute('INSERT INTO telephone(name, ContactNumber) VALUES(?, ?)', insert_entities)
        con.commit()
        cursorObj.close()
        #Audit log entry
        name = insert_entities[0]
        contact = insert_entities[1]
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tADD\tSuccess\tAdded a record with a name \""+str(name)+"\" and contact number \""+ str(contact)+"\".")
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")
    except Error:
        #Audit log entry
        name = insert_entities[0]
        contact = insert_entities[1]
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tADD\tFailed\tTried to add a record with name \""+str(name)+"\" and contact number \""+ str(contact)+"\".")
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")     
        print(Error)
        con.close()
        sys.exit(1)

#Code to remove the records from telephone directory when name is passed.
def sql_del_name(con, del_name_entities):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM telephone WHERE name =?', del_name_entities).rowcount
        rows = cursorObj.fetchall()
        if(len(rows) == 0):
            print("An attempt to remove a non-existent name from the directory ")
            #Audit log entry
            name = del_name_entities[0]
            ct = datetime.datetime.now()
            upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tFailed\tTried to remove a record with name \""+str(name)+"\"")
	    cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
            os.system(cmd)
    	    os.system("sudo chmod 600 AuditFile.txt")
    	    f = open("AuditFile.txt", "a")
            f.write(upd_str)
            f.close()
            os.system("sudo chown root AuditFile.txt")
    	    os.system("sudo chmod 600 AuditFile.txt")
            cursorObj.close()
            con.close()
            sys.exit(1)
        else:
            cursorObj.execute('DELETE FROM telephone WHERE name =?', del_name_entities)
            con.commit()
            #Audit log entry
            name = del_name_entities[0]
            ct = datetime.datetime.now()
            upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tSuccess\tRemoved a record with name \""+str(name)+"\"")
	    cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	    os.system(cmd)
    	    os.system("sudo chmod 600 AuditFile.txt")
    	    f = open("AuditFile.txt", "a")
            f.write(upd_str)
            f.close()
            os.system("sudo chown root AuditFile.txt")
    	    os.system("sudo chmod 600 AuditFile.txt")
            cursorObj.close()
   
    except Error:
        #Audit log entry
        name = del_name_entities[0]
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tFailed\tTried to remove a record with name \""+str(name)+"\"")
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")
        print(Error)
        con.close()
        sys.exit(1)

#Code to remove the records from telephone directory when number is passed.
def sql_del_number(con, del_number_entities):
    try:
        cursorObj = con.cursor() 
        cursorObj.execute('SELECT * FROM telephone WHERE ContactNumber =?', del_number_entities).rowcount
        rows = cursorObj.fetchall()
        if(len(rows) == 0):
            print("An attempt to remove a non-existent number from the directory ")
            #Audit log entry
            contact = del_number_entities[0]
            ct = datetime.datetime.now()
            upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tFailed\tTried to remove a record with contact number \""+str(contact)+"\"")
	    cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	    os.system(cmd)
    	    os.system("sudo chmod 600 AuditFile.txt")
    	    f = open("AuditFile.txt", "a")
            f.write(upd_str)
            f.close()
            os.system("sudo chown root AuditFile.txt")
    	    os.system("sudo chmod 600 AuditFile.txt")
            cursorObj.close()
            con.close()
            sys.exit(1)
        else: 
            namelist =''
            cursorObj.execute('SELECT name FROM telephone WHERE ContactNumber =?', del_number_entities)
            names = cursorObj.fetchall() 
            for name in names:
                namelist = str(namelist) + str(name) +","
            namelist = namelist.strip(",")            
            cursorObj.execute('DELETE FROM telephone WHERE ContactNumber =?', del_number_entities)
            con.commit()
            #Audit log entry
            ct = datetime.datetime.now()
            upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tSuccess\tRemoved a record with names "+str(namelist))
	    cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	    os.system(cmd)
    	    os.system("sudo chmod 600 AuditFile.txt")
    	    f = open("AuditFile.txt", "a")
            f.write(upd_str)
            f.close()
            os.system("sudo chown root AuditFile.txt")
    	    os.system("sudo chmod 600 AuditFile.txt")
            cursorObj.close()
        
    except Error:
        #Audit log entry
        contact = del_number_entities[0]
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tDEL\tFailed\tTried to remove a record with contact number \""+str(contact)+"\"")
        f.write(upd_str)
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")
        sys.exit(1)
        print(Error)
        
#Code to display records in the telephone directory.
def sql_fetch(con):
    try:
        cursorObj = con.cursor()
        cursorObj.execute('SELECT * FROM telephone')
        rows = cursorObj.fetchall()
        for row in rows:
            print(row)
        cursorObj.close()
        #Audit log entry
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tLIST\tSuccess\tDisplayed contents of Table.")
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")
    except Error:
        #Audit log entry
        ct = datetime.datetime.now()
        upd_str= str("\n"+str(ct)+"\t"+str(realuserid)+"\tLIST\tFailed\tTried to display the contents of table.")
	cmd = "sudo chown "+str(realuserid)+" AuditFile.txt"
    	os.system(cmd)
    	os.system("sudo chmod 600 AuditFile.txt")
    	f = open("AuditFile.txt", "a")
        f.write(upd_str)
        f.close()
        os.system("sudo chown root AuditFile.txt")
    	os.system("sudo chmod 600 AuditFile.txt")
        print(Error)
        con.close()
        sys.exit(1)

#Retrieves the real user id of the user running the program for audit log file entries.
realuserid = os.getuid()
#Checks whether "AuditFile.txt" used for log entries exist or not.If exists then sets its owner as root and owner alone can read/write log entries.
if os.path.exists("AuditFile.txt"):
    os.system("sudo chown root AuditFile.txt")
    os.system("sudo chmod 600 AuditFile.txt") 
#Creates an "AuditFile.txt" for log entries and mentioned the format of entries. Then set root as owner and owner alone can read/write log entries.
else:
    f = open("AuditFile.txt", "w")
    f.write("Entries in this file will be in the format: TimeStamp Real-UserId Command Status Additional Details")
    f.close()
    os.system("sudo chown root AuditFile.txt")
    os.system("sudo chmod 600 AuditFile.txt")   
   
#Connecting to database mydatabase.db
con = sql_connection()
#Creating a table if does not exist
sql_table(con)
#When no arguments are passed then help will be displayed.
if len(sys.argv) < 2 :
	print("Please enter command and arguments")
	print("\n--help\n	ADD \"<Person>\" \"<Telephone #>\" - Add a new person to the database")
	print("\n	DEL \"<Person>\" - Remove someone from the database by name\n	DEL \"<Telephone #>\" - Remove someone by telephone #")
	print("\n	LIST - Produce a list of the members of the database")
#When arguments are passed
else:
	command_input = sys.argv[1]
	command_check_results = Command_check(command_input) 
    #Checks if a valid command is specified or not.
	if(command_check_results =="Inavlid Command entered"):
    		print("Invalid Command Entered")
	else:
            #ADD command code part
    		if (command_input == "ADD"):
                #Checks whether required number of arguments are passed.
        		if( len(sys.argv) == 4):
                        #Retrives fullname and check its format.
            			fullname = sys.argv[2]
            			full_name_check_results = Full_Name_check(fullname)
                        #when passed name is in invalid input format.
            			if full_name_check_results == "Invalid Format":
                			print("\nInvalid Name Format!!")
                			con.close()
                			sys.exit(1)
                        #Retrieves telephone number and check whether its format is valid or not.
            			else:
                			cno = sys.argv[3]
                			cno_check_results = Contact_Number_m17(cno)
                            #when passed number is in invalid input format.
                			if(cno != cno_check_results):
                    				print("Invalid Contact Number")
                    				con.close()
                    				sys.exit(1)
                            # Add the record to telephone directory.
                			else:
                    				insert_entities = (fullname, cno)
                    				sql_insert(con, insert_entities)
                    				con.close()
                    				sys.exit(0)
                #Displays help of ADD command
        		else:
            			print("\n--help\n	ADD \"<Person>\" \"<Telephone #>\" - Add a new person to the database")
            			con.close()
            			sys.exit(1)
            #DEL Command code part
    		elif (command_input == "DEL"):
                #Checks whether required number of arguments are passed.
        		if( len(sys.argv) == 3):
                        #Retrives argument and checks whether it is valid telephone number or not. If so then records with that telephone number will be removed.
            			cno = sys.argv[2]
            			cno_check_results = Contact_Number_m17(cno)
                        #removing records with the telephone number from the directory.
            			if(cno == cno_check_results):
                			del_number_entities = (cno,)
                			sql_del_number(con, del_number_entities)
                			con.close()
               				sys.exit(0)
                        #If not valid contact number then chceks whether it is a valid name then records with that name will be removed from directory.
            			else:
                			fullname = sys.argv[2]
                			full_name_check_results = Full_Name_check(fullname)
                            #If not valid then diaplays invalid argument format message.
                			if full_name_check_results == "Invalid Format":
                    				print("Invalid Argument Format!")
                    				con.close()
                    				sys.exit(1)
                            #Remove records with that name from directory.
                			else:
                    				del_name_entities = (fullname,)
                    				sql_del_name(con, del_name_entities)
                    				con.close()
                    				sys.exit(0)
                #Help for DEL command.
        		else:
            			print("\n--help\n	DEL \"<Person>\" - Remove someone from the database by name\n   DEL \"<Telephone #>\" - Remove someone by telephone #")
            			con.close()
            			sys.exit(1)
            #Code for LIST command.
    		elif (command_input == "LIST"):
                #If no other arguments are passed then displays list of records in telephone directory.
        		if( len(sys.argv) == 2):
            			sql_fetch(con)
            			con.close()
            			sys.exit(0)
                #Help page for LIST command.
        		else:
            			print("\n--help\n	LIST - Produce a list of the members of the database")
            			con.close()
            			sys.exit(1)
            #Closes the connection
    		else:
        		con.close()
        		sys.exit(1)
	con.close()
sys.exit(0)
