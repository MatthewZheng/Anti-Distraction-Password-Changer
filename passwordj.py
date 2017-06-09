#! usr/bin/env python
_author_ = "Matthew Zheng"
_purpose_ = "Make a password generator and keeps it locked for x period of time."

import sys
import tkinter


#setup window
window = tkinter.Tk()
window.configure(background = '#7ffb03')
window.title("Lifesaver: a pass at a time.")

#setup icons and background
myIcon = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\newicon-alt.gif")
window.tk.call('wm', 'iconphoto', window._w, myIcon)
title = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\bgupdated-c.gif")
w = tkinter.Label(window, image=title, borderwidth=0)
w.grid(column=0, row=0, pady=(0,0))

#pass generation
passGen = tkinter.Button(window, text="G E N E R A T E", width='15', fg="#e6f6d6", font=("Arial",8), bg='#b6e289')
passGen.grid(column=0, row=1, pady=(20,20))

#First set of instructions
# instruct = tkinter.Label(window, text="Click to generate a Military-Grade password and save it to the program. Copies to clipboard. Replace your current password in the field given by FaceBook/Online Game/Virtual instrument of terror of your own choosing. Don't press ctrl-v until you clear your clipboard!", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')
instructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-1.gif")
instruct = tkinter.Label(window, image=instructImg, borderwidth=0, height=130)
instruct.grid(column=0, row=2, pady=(0,0))

#Date enter field
dateField = tkinter.Entry()

#second set of instructions
secInstructImg = tkinter.PhotoImage(file=r"C:\Users\Zhenger\Desktop\MLH\Password-Jumbler\mid-instruct-2.gif")
secInstruct = tkinter.Label(window, image=secInstructImg, borderwidth=0, height=100)
secInstruct.grid(column=0, row=3, pady=(0,30))
# secondI = tkinter.Label(window, text="Enter the date you want the password to be locked until as YYYY-MM-DD. (Unlocks at 12am, typed date). Military-Grade AES-256 Encryption protected.", wraplength='800', font=("Arial", 13), fg='#F7F7F7', bg='#73e600')



window.mainloop()
