#! usr/bin/env python
_author_ = "Matthew Zheng"
_purpose_ = "Generate a password and keep the it locked and encrypted until a specified date."

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

#setup global variables
someEntry = tkinter.StringVar()

#Functions
#copys content to clipboard
def copyClipboard(mess):
    #clear out any old entries
    window.clipboard_clear()
    window.clipboard_append(mess)

#clears clipboard
def clearClipboard():
    window.clipboard_clear()
    window.clipboard_append("Where's your self-confidence? Let time be your friend and trust that your password is safe with the NSA-sanctioned algorithm, AES-196.")

#parses user's entry and encrypts their password into a hash and saves it to their project directory along with date of release
def keyCreation():
    #setup files for writing out
    keyFile = open("key.txt", "wb")
    passFile = open("pass.txt", "wb")
    #gen password and key (used 32 bytes for AES-196)
    key = get_random_bytes(16)
    #write out key to file
    keyFile.write(key)
    #generate password and copies to clipboard
    userPass = str.encode(genPass())
    copyClipboard(userPass.decode("utf-8"))
    #get the specified date
    usersDate = str.encode(str(getNParse()))
    #combine outputs and encrypt
    output = usersDate+userPass
    cipher = AES.new(key, AES.MODE_EAX)
    ciphertext, tag = cipher.encrypt_and_digest(output)
    [passFile.write(x) for x in (cipher.nonce, tag, ciphertext)]
    copyClip = tkinter.Label(window, text="C O P I E D   T O   C L I P B O A R D.", fg="#F7F7F7", font=("Arial",8), bg='#b6e289', width='31')
    copyClip.grid(column=6, row=1, pady=(20,10), sticky='W')
    #write out precautionary message(s)
    topL = tkinter.Toplevel()
    today = date.today()
    userDay = getNParse()
    if userDay == "error":
        warning1 = tkinter.Message(topL, text="You did not read the instructions.", width=800, pady=20, padx=20)
        warning1.grid(column=5, row=5)
    elif userDay == today:
        warning2 = tkinter.Message(topL, text="Your date is today. It seems counter-intuitive to choose today, but do as you wish.", width=1000, pady=20, padx=20)
        warning2.grid(column=5, row=5)
        tamperWarning()
    elif userDay < today:
        warning3 = tkinter.Message(topL, text="Your date is in the past. To avoid problems, it is highly advisable to choose a future date", width=1000, pady=20, padx=20)
        warning3.grid(column=5, row=5)
        tamperWarning()
    else:
        topL.withdraw()
        tamperWarning()

#finds if given date is realistic
def dateValid(userDList):
    if(userDList[1]>12):
        return(False)
    #31 days in  1 3 5 7 8 10 12
    if (userDList[1] == 1 or userDList[1] == 3 or userDList[1] == 5 or userDList[1] == 7 or userDList[1] == 8 or userDList[1] == 10 or userDList[1] == 12):
        if (userDList[2] > 31 or userDList[2]<1):
            return(False)
    #28 in 2
    elif (userDList[1] == 2):
        if(userDList[2] > 28 or userDList[2]<1):
            return(False)
    #30 in 4 6 9 11
    elif (userDList[1] == 4 or userDList[1] == 6 or userDList[1] == 9 or userDList[1] == 11):
        if(userDList[2] > 30 or userDList[2]<1):
            return(False)
    else:
        return(True)

#pints tamper warning
def tamperWarning():
    topL2 = tkinter.Toplevel()
    inform = tkinter.Message(topL2, text="Copied to password to clipboard. Do not move, delete, or tamper with the password file or the key. This will prevent you from decrypting your password.", width=1200, pady=20, padx=20)
    inform.grid(column=5, row=5)

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
    #splits into list of strings
    unfilteredP = (cipher.decrypt_and_verify(ciphertext, tag))
    passwordDecrypt = unfilteredP.decode("utf-8")
    passwordDecrypt = passwordDecrypt[10:]
    dateDecrypt = parseEntry(unfilteredP.decode("utf-8"))
    #cut off non-date data
    dateDecrypt[2] = dateDecrypt[2][:2]
    dateDecrypt = dateDecrypt[:3]
    #remove leading zeros to avoid converting to hex and appends to listDate
    for i in range(0, len(dateDecrypt)):
        listDate.append(int(dateDecrypt[i].lstrip('0')))
    #convert into date format
    convertedDate = date(listDate[0], listDate[1], listDate[2])
    #checks if today is the day specified and decrypts or witholds password with a message
    topL = tkinter.Toplevel()
    if(checkIfToday(listDate) == 'y'):
        unEncrypt = tkinter.Message(topL, text="Your key has been un-encrypted after the colon: %s" % (passwordDecrypt), width=800, pady=20, padx=20)
        unEncrypt.grid(column=5, row=5)
        copyPass = tkinter.Button(topL, text="Copy to clipboard.", width=20, command=copyClipboard(passwordDecrypt))
        copyPass.grid(column=5, row=6, pady=(0,20))
    elif(checkIfToday(listDate) == 's'):
        unEncrypt = tkinter.Message(topL, text="Why would you encrypt for a past date? Looks like you're a bit hooped.", width=1000, pady=20, padx=20)
        unEncrypt.grid(column=5, row=5)
    else:
        unEncrypt = tkinter.Message(topL, text="Nope, you can't un-encrypt your password just yet. Signed, your past self.", width=1000, pady=20, padx=20)
        unEncrypt.grid(column=5, row=5)


#Parses entry typed by user into a python date format
def getNParse():
    intList = []
    #read entry
    listDate = parseEntry(someEntry.get())
    #check for length error
    if(len(listDate)!=3):
        return("error")
    #remove leading zeros to avoid converting to hex and appends to intList
    for i in range(0, len(listDate)):
        intList.append(int(listDate[i].lstrip('0')))
    #check for date error
    if(dateValid(intList) == False):
        return("error")
    #return in date format
    return(date(intList[0], intList[1], intList[2]))


#Removes dashes from given format and formats into list
def parseEntry(someStr):
    userDate = someStr.split("-")
    return(userDate)


def checkIfToday(userDate):
    today = date.today()
    #Reformat the user date into python date format
    formattedUD = date(userDate[0], userDate[1], userDate[2])
    if formattedUD == today:
        return('y')
    elif formattedUD < today:
        return('s')
    else:
        return('n')


#generates random password
def genPass():
    userPass = []
    for i in range(0, randint(9,30)):
        userPass.append(random.choice(string.ascii_letters+string.digits+string.punctuation))
    return(''.join(userPass))

def main():
    #setup icons and background
    myIcon = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\newicon-alt.gif")
    window.tk.call('wm', 'iconphoto', window._w, myIcon)
    title = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\logo.gif")
    w = tkinter.Label(window, image=title, borderwidth=0)
    w.grid(column=0, row=0, pady=(0,0), columnspan='10')

    #pass generation and date entry
    dateEn = tkinter.Entry(window, textvariable=someEntry, justify='center', font=("Arial", 8), width='30')
    passGen = tkinter.Button(window, text="G E N E R A T E", width='22', fg="#F7F7F7", font=("Arial",8), bg='#b6e289', command=keyCreation)
    keyReq = tkinter.Button(window, text="R E Q U E S T   P R E V I O U S L Y   G E N E R A T E D   P A S S", width='63', fg="#F7F7F7", font=("Arial",8), bg='#b6e289', command=keyManager)
    clearClip = tkinter.Button(window, text="C L E A R   C L I P B O A R D.", fg="#F7F7F7", font=("Arial",8), bg='#b6e289', width='30', command=clearClipboard)
    dateEn.grid(column=4, row=1, pady=(20,10), sticky='E')
    passGen.grid(column=5, row=1, pady=(20,10))
    clearClip.grid(column=6, row=3, pady=(10,20), sticky='W')
    keyReq.grid(column=4, row=3, pady=(10,20), columnspan=2)

    #First set of instructions
    # instruct = tkinter.Label(window, text="Click to generate a Military-Grade password and save it to the program. Copies to clipboard. Replace your current password in the field given by FaceBook/Online Game/Virtual instrument of terror of your own choosing. Don't press ctrl-v until you clear your clipboard!", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')
    instructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-2-updated.gif")
    instruct = tkinter.Label(window, image=instructImg, borderwidth=0, height=130)
    instruct.grid(column=0, row=4, pady=(0,0), columnspan='10')

    #Date enter field
    dateField = tkinter.Entry()

    #second set of instructions
    # secondI = tkinter.Label(window, text="Enter the date you want the password to be locked until as YYYY-MM-DD. (Unlocks at 12am, typed date). Military-Grade AES-256 Encryption protected.", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')
    secInstructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-1.gif")
    secInstruct = tkinter.Label(window, image=secInstructImg, borderwidth=0, height=100)
    secInstruct.grid(column=0, row=5, pady=(0,30), columnspan='10')

    window.mainloop()


if __name__ == "__main__":
    main()
