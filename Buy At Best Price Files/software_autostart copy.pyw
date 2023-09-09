import time
from tkinter import *
from tkinter.font import BOLD
from PIL import ImageTk, Image ,  ImageSequence
from tkinter.ttk import Notebook
from tkinter import ttk
from tkinter import messagebox
from urllib.request import urlopen
import webbrowser
import threading
from datetime import date
import socket

import urllib3


play_var=1


###



def playgiff(gifname,frameforgif):
    global play_var
    #play_var=1
    global img
    img= Image.open(gifname)
    lbl =Label(frameforgif,bg="#232430")
    lbl.place(x=0,y=0)
    try:
        for img in ImageSequence.Iterator(img):
            if play_var==1:
                img= img.resize((30,30))
                img = ImageTk.PhotoImage(img)
                lbl.config(image=img,borderwidth=0)
                frameforgif.update()
                time.sleep(0.03)
            else:
                break
        if play_var==1:
            frameforgif.after(0,playgiff(gifname,frameforgif))
        else:
            return
    except:
        print('An error in status_gif- image sequence iteration!')
        play_var=0
        return

def exitgiff():
    global play_var
    play_var=0
    frameforgif.destroy()


def internetpopup():
    try:
        urlopen('https://www.google.com', timeout=1)
        return True
        
    except urllib3.error.URLError as Error:
        return False

###

def updation():
    root.iconify()
    global internetcheck
    internetcheck=internetpopup()
    while internetcheck==False:
        internetcheck=internetpopup()
        if internetcheck==True:
            break
        print("Internet not found in while")
        time.sleep(5)
        print("retrying")
    print("updation started")
    try:
        global overr
        overr="override"
        update_t=threading.Thread(target=(lambda:grab_rowid_url(overr,override=True)))
        update_t.start()
        #time.sleep(3)
    except:
        print("error in updation!!")
    update_t.join()
    print("Execution completed \nClosing Program!!!")
    
    try:
        exitgiff()
        gif_t.join()
        exitgiff()
        print("CLOSED gif")
        root.destroy()
        exit(0)
    except:
        print("not able to close")
    print("CLOSED")


#####################################################################################

root = Tk()
root.geometry("300x50")
root.resizable(height=False, width=False)
root.iconbitmap("BABP-transparentico.ico")
root.title("Buy at best price - Database Updation")


frame1=Frame(root,background="#E3DFF9")
frame1.place(x=0,y=0,width=300,height=50)

frameforgif=Frame(frame1,background="#E3DFF9")
frameforgif.place(x=0,y=0,width=50,height=50)


Label1 = Label(frame1,background='#E3DFF9',text="  Updating database of Buy At Best Price !\nPlease Wait...")
Label1.place(x=70,y=0,width=220,height=50)
internetcheck=internetpopup()
print("statement: ",internetcheck)


gif_t=threading.Thread(target=(lambda:playgiff("Gear-0.3s-200px.gif",frameforgif)))
gif_t.start()
threading.Thread(target=(updation)).start()


root.mainloop()
