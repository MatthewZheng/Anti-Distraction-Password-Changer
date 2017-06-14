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

#setup window
window = tkinter.Tk()
window.configure(background = '#7ffb03')
window.title("LifeScript: saving you, one password at a time.")

#setup text entry
someEntry = tkinter.StringVar()

#Functions
def getNParse():
    intList = []
    listDate = parseEntry(someEntry.get())
    #remove leading zeros to avoid converting to hex
    for i in range(0, len(listDate)):
        intList.append(int(listDate[i].lstrip('0')))
    timeDifference(intList)

def parseEntry(someStr):
    userDate = someStr.split("-")
    return(userDate)

def timeDifference(userDate):
    today = date.today()
    #Reformat the user date into python date format
    formattedUD = date(userDate[0], userDate[1], userDate[2])
    #find difference between dates
    if formattedUD <= today:
        print("Smaller than")
        return(0)
    elif formattedUD > today:
         daysUntil = (formattedUD - today).days
         print(daysUntil)
         return(daysUntil)

def genPass():
    userPass = []
    for i in range(0, randint(9,30)):
        userPass.append(random.choice(string.ascii_letters+string.digits+string.punctuation))
    print(userPass)


#setup icons and background
myIcon = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\newicon-alt.gif")
window.tk.call('wm', 'iconphoto', window._w, myIcon)
title = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\bgupdated-c.gif")
w = tkinter.Label(window, image=title, borderwidth=0)
w.grid(column=0, row=0, pady=(0,0), columnspan='10')

#pass generation and date entry
dateEn = tkinter.Entry(window, textvariable=someEntry, justify='center', font=("Arial", 8), width='30')
passGen = tkinter.Button(window, text="G E N E R A T E", width='22', fg="#F7F7F7", font=("Arial",8), bg='#b6e289', command=getNParse)
keyReq = tkinter.Button(window, text="R E Q U E S T   P R E V I O U S L Y   G E N E R A T E D   K E Y", width='60', fg="#F7F7F7", font=("Arial",8), bg='#b6e289')
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

genPass()

window.mainloop()
