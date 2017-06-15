#! usr/bin/env python
_author_ = "Matthew Zheng"
_purpose_ = "Make a password generator and keeps it locked for x period of time."

#imports
import sys
import tkinter
import time
import random
import string
import base64
from datetime import date
from random import randint
from Crypto.Random import get_random_bytes
from Crypto.Cipher import AES

#setup window
window = tkinter.Tk()
window.configure(background = '#7ffb03')
window.title("LifeScript: saving you, one password at a time.")

#setup text entry
someEntry = tkinter.StringVar()

#Functions
#parses user's entry and encrypts their password into a hash and saves it to their project directory along with date of release
def keyCreation():
    #setup files for writing out
    keyFile = open("key.txt", "wb")
    passFile = open("pass.txt", "wb")
    #gen password and key (used 32 bytes for AES-196)
    key = get_random_bytes(16)
    #write out key to file
    keyFile.write(key)
    print("Do not move, delete, or tamper with this key. This will prevent you from decrypting your password.")
    #generate password
    userPass = genPass()
    #get the specified date
    usersDate = str.encode(str(getNParse()))
    #combine outputs and encrypt
    output = usersDate+userPass
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(output)
    [passFile.write(x) for x in (cipher.nonce, tag, ciphertext)]
    print(output)


#checks current date against the date they set, releases or withholds the key
def keyManager():
    #variables and dependents
    listDate = []
    today = date.today()
    #setup files for reading
    keyFile = open("key.txt", "rb")
    passFile = open("pass.txt", "rb")
    nonce, tag, ciphertext = [passFile.read(x) for x in (16, 16, -1)]
    #read in the key
    key = keyFile.read()
    keyFile.close()
    cipher = AES.new(key, AES.MODE_EAX, nonce)
    dateDecrypt = parseEntry(str(cipher.decrypt_and_verify(ciphertext, tag)))
    print(dateDecrypt)
    return(0)
    #remove leading zeros to avoid converting to hex and appends to listDate
    for i in range(0, len(dateDecrypt)):
        listDate.append(int(userDFormatted[i].lstrip('0')))
    #checks if today is the day specified
    if(checkIfToday(listDate)):
        print("Your key has be un-encrypted. Open pass.txt for your password. (If you have it open, close it and re-open it).")
    else:
        print("Nope, you can't un-encrypt your password just yet. --Your past self.")


#Parses entry typed by user into a python date format
def getNParse():
    intList = []
    #read entry
    listDate = parseEntry(someEntry.get())
    #remove leading zeros to avoid converting to hex and appends to intList
    for i in range(0, len(listDate)):
        intList.append(int(listDate[i].lstrip('0')))
    #return in date format
    return(date(intList[0], intList[1], intList[2]))


#Removes dashes from given format and formats into list
def parseEntry(someStr):
    userDate = someStr.split("-")
    return(userDate)


#calulates difference in date from today, prints out the difference.
def timeDifference(userDate):
    today = date.today()
    #Reformat the user date into python date format
    formattedUD = date(userDate[0], userDate[1], userDate[2])
    #find difference between dates
    if formattedUD <= today:
        print("Your date is in the past.")
        return(0)
    elif formattedUD > today:
         daysUntil = (formattedUD - today).days
         print(daysUntil)
         return(daysUntil)


def checkIfToday(userDate):
    today = date.today()
    #Reformat the user date into python date format
    formattedUD = date(userDate[0], userDate[1], userDate[2])
    if formattedUD == today:
        return(True)
    else:
        return(False)


#generates random password
def genPass():
    userPass = []
    for i in range(0, randint(9,30)):
        userPass.append(random.choice(string.ascii_letters+string.digits+string.punctuation))
    return(str.encode(str(userPass)))


#setup icons and background
myIcon = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\newicon-alt.gif")
window.tk.call('wm', 'iconphoto', window._w, myIcon)
title = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\bgupdated-c.gif")
w = tkinter.Label(window, image=title, borderwidth=0)
w.grid(column=0, row=0, pady=(0,0), columnspan='10')

#pass generation and date entry
dateEn = tkinter.Entry(window, textvariable=someEntry, justify='center', font=("Arial", 8), width='30')
passGen = tkinter.Button(window, text="G E N E R A T E", width='22', fg="#F7F7F7", font=("Arial",8), bg='#b6e289', command=keyCreation)
keyReq = tkinter.Button(window, text="R E Q U E S T   P R E V I O U S L Y   G E N E R A T E D   K E Y", width='60', fg="#F7F7F7", font=("Arial",8), bg='#b6e289', command=keyManager)
dateEn.grid(column=4, row=1, pady=(20,10), sticky='E', padx='10')
passGen.grid(column=5, row=1, pady=(20,10), stick='W')
keyReq.grid(column=0, row=3, pady=(10,20), columnspan='10')

#First set of instructions
# instruct = tkinter.Label(window, text="Click to generate a Military-Grade password and save it to the program. Copies to clipboard. Replace your current password in the field given by FaceBook/Online Game/Virtual instrument of terror of your own choosing. Don't press ctrl-v until you clear your clipboard!", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')
instructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-1.gif")
instruct = tkinter.Label(window, image=instructImg, borderwidth=0, height=130)
instruct.grid(column=0, row=4, pady=(0,0), columnspan='10')

#Date enter field
dateField = tkinter.Entry()

#second set of instructions
# secondI = tkinter.Label(window, text="Enter the date you want the password to be locked until as YYYY-MM-DD. (Unlocks at 12am, typed date). Military-Grade AES-256 Encryption protected.", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')
secInstructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-2.gif")
secInstruct = tkinter.Label(window, image=secInstructImg, borderwidth=0, height=100)
secInstruct.grid(column=0, row=5, pady=(0,30), columnspan='10')

#test functions
genPass()
# lockDownKey("abcdef")

window.mainloop()
