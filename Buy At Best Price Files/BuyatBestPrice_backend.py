######### main backend #########

from aifc import Error
from os import error
import sqlite3
import bs4
import urllib.request
import urllib
from urllib.request import urlopen
import time
from tkinter import messagebox
from tkinter import *
from PIL import ImageTk, Image ,ImageSequence
from tkinter.ttk import Notebook
from tkinter import ttk
import mplcursors
from plyer import notification
import smtplib
from email.message import EmailMessage
from configparser import ConfigParser
from cryptography.fernet import Fernet
import threading
import os
import subprocess
import shutil
from tkinterweb import HtmlFrame #import the HTML browser
from tkinterweb import *
import datetime
from tkPDFViewer import tkPDFViewer as pdf
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,NavigationToolbar2Tk)

import csv
import pandas as pd
import matplotlib.backends.backend_tkagg as tkagg
from matplotlib import backend_bases
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Cursor
########Colour Pallet##########
purple = "#E3DFF9"
darkblue = "#232430"
darkgray = "#4A4A4F"
white = "#FFFFFF"
navyblue = "#24305E"
bluishgray = "#8EAEBD"

########Font Pallet##########
#our_desired_font = "bold"
our_desired_font = "Comic Sans MS"
#our_desired_font = "bold"
our_desired_font2 = "Calibri"
#################################

##########Global############
play=0

#################################

########## NOTIFICATION Database############################################################################################

# Create query function for notification db
def query_notify(notify_tree):
    for Notify_record in notify_tree.get_children():
        notify_tree.delete(Notify_record)
    # Create a db or connect to one
    conn1 = sqlite3.connect('Notification.db')
    # Create cursor
    c1 = conn1.cursor()

    # query the db
    c1.execute("SELECT rowid, * FROM notification ORDER BY rowid DESC")
    Notify_records = c1.fetchall()
    #print(records)

    # Add our data to the screen
    global count1
    count1 = 0
    #rowID = my_tree.identify('item', event.x, event.y)
    for Notif_record in Notify_records:
        #print(Notif_record)
        if count1 % 2 == 0:
                notify_tree.insert(parent='', index='end', text='',iid=count1, values=(Notif_record[0], Notif_record[1], Notif_record[2]),tags=('evenrow',))
        else:
                notify_tree.insert(parent='', index='end', text='', iid=count1,values=(Notif_record[0], Notif_record[1], Notif_record[2]), tags=('oddrow',))
        # increment counter
        count1 += 1
    print("Notification treeview refreshed!")
    # Commit changes
    conn1.commit()

    # Close connection
    conn1.close()


# Create submit function for db
def submit_notify(notify_msg,datetime,notify_tree):
    try:
        notify_msg= str(notify_msg)
        notify_msg = notify_msg.replace('\n'," ")
        #notify_msg = notify_msg.strip('The Price of Product :')
        datetime= str(datetime)
        # Create a db or connect to one
        conn1 = sqlite3.connect('Notification.db')
        # Create cursor
        c1 = conn1.cursor()

        # Insert into table
        c1.execute("INSERT INTO notification VALUES ( :datetime, :main_notify)",
                {
                    'datetime': datetime,
                    'main_notify': notify_msg,
                })

        # Commit changes
        conn1.commit()
        print("Notification added!-submit_notify()")
        # Close connection
        conn1.close()
        query_notify(notify_tree)
    except:
        print("Error in submitnotify")
def store_notifications(notify_str,notify_tree):
    now = datetime.datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    submit_notify(notify_str,dt_string,notify_tree)	


######################################################################################################


#autostart
def auto_start():
    """
    echo off
    E:
    cd E:\testing soft\Simple database by ak
    start database_front.exe
    exit
    """
    name_ofbat_file= "BuyatBestPrice_autostart_updation.bat"
    print('curent working directory:      ', os.getcwd())
    full_cwd=os.getcwd()
    c_dir= os.getcwd()[:2]
    print("Directory name / drive name =",c_dir)
    print('running file name:    ', os.path.basename(__file__))
    print('__file__:    ', __file__)
    print("user path : ",os.path.expanduser('~'))
    pathofstartup= os.path.expanduser('~')+fr"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\{name_ofbat_file}"
    print("startup folder pat: ",pathofstartup)

    myBat = open(f"{name_ofbat_file}","w") 
    myBat.write(f'''echo off
    {c_dir}
    cd {full_cwd}
    start /min  Buy_At_Best_Price.exe
    exit
    ''')
    myBat.close() 

    src= fr"{full_cwd}\{name_ofbat_file}"
    print("src file: ",src)
    shutil.move(src,pathofstartup)


def delete_autostart():
    name_ofbat_file= "BuyatBestPrice_autostart_updation.bat"
    pathofstartup= os.path.expanduser('~')+fr"\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\{name_ofbat_file}"
    try:
        if os.path.exists(pathofstartup) :
            os.remove(pathofstartup)
            print("file deleted")
        else:
            print("file not found")
    except:
        print("unable to delete autostart")

######################################################################################################

#validate buttons
def validate_buttons(on,off,on_button1,on_button2,on_button3,on_button4,on_button5):
    try:
        parser = ConfigParser()
        parser.read('settings.ini')
        s1 = parser.get('setting_menu','email_suggestion')  
        b1 = parser.get('setting_menu','win_notification_engine')  
        b2 = parser.get('setting_menu','email_notification_engine')  
        b3 = parser.get('setting_menu','continous_price_tracking_bg')  
        b4 = parser.get('setting_menu','alert_only_if_price_down')  
        b5 = parser.get('setting_menu','autostart_on_windows_startup')
        b_ini_list=[b1,b2,b3,b4,b5]
        b_name_list=[on_button1,on_button2,on_button3,on_button4,on_button5]
        for item_ini,item_name in zip(b_ini_list , b_name_list):
            #print(item_name," = ",item_ini)
            if item_ini=="1":
                item_name.config(image=on)
            else:
                item_name.config(image=off)
        return s1,b1,b2,b3,b4,b5
    except: 
        print("Error in validate buttons")

# Define our switch function
def switch(button_name,button_ini,on,off):
    is_on = button_ini

    #read .ini files
    parser = ConfigParser()
    parser.read('settings.ini')
    saved_ison = parser.get('setting_menu',is_on)  
     
    # Determine is on or off
    if saved_ison=="1":  
        button_name.config(image=off)
        #write to ini file
        parser.set('setting_menu',is_on,"0") 
        with open('settings.ini','w') as configsetting:
            parser.write(configsetting)

    elif saved_ison=="0":
        button_name.config(image=on)
        #write to ini file
        parser.set('setting_menu',is_on,"1") 
        with open('settings.ini','w') as configsetting:
            parser.write(configsetting)

######################################################################################################

def profile_modify(nameEntry,emailEntry,phnnoEntry,saveB,cancelProf):
    nameEntry.config(state= "normal")
    emailEntry.config(state= "normal")
    phnnoEntry.config(state= "normal")
    saveB.config(state= "normal")
    cancelProf.config(state= "normal")

def profile_cancel(nameEntry,emailEntry,phnnoEntry):
    nameEntry.delete(0,END)
    emailEntry.delete(0,END)
    phnnoEntry.delete(0,END)


def profile_save(username_var,useremail_var,userphnno_var,n_entry,em_entry,phn_entry,s_buton,can_buton,labe_status,Tabs,tab1):
    if messagebox.askyesnocancel("Profile Updation","Do you want to save changes to Profile?"):
        user_name=username_var.get()
        user_email=useremail_var.get()
        user_phnno=userphnno_var.get()
        parser = ConfigParser()
        parser.read('settings.ini')
        if (len(user_name) > 0) and (len(user_email) > 0) and (len(user_phnno) > 0):
            parser.set('user_profile','user_name',user_name) 
            parser.set('user_profile','user_email',user_email) 
            parser.set('user_profile','user_phnno',user_phnno) 
            with open('settings.ini','w') as configsetting:
                parser.write(configsetting)
            n_entry.config(state= "disabled")
            em_entry.config(state= "disabled")
            phn_entry.config(state= "disabled")
            s_buton.config(state= "disabled")
            can_buton.config(state= "disabled")
            def update_status_forprofile():
                labe_status.config(text = "Status: Profile Updated!")
                time.sleep(5)
                labe_status.config(text = "Status: Active")
            threading.Thread(target=(update_status_forprofile)).start()
            Tabs.select(tab1)
            ##########        
            n= parser.get('user_profile','user_name')
            em= parser.get('user_profile','user_email')
            phn= parser.get('user_profile','user_phnno')
            print(n,type(n))
            print(em,type(em))
            print(phn,type(phn))
        else:
            parser.set('user_profile','user_name',"null") 
            parser.set('user_profile','user_email',"null") 
            parser.set('user_profile','user_phnno',"null") 
            with open('settings.ini','w') as configsetting:
                parser.write(configsetting)
            can_buton.config(state= "disabled")

######################################################################################################

#User Guide
def userguidepdfopen(frame):
    try:
        v1 = pdf.ShowPdf()
    
        # Adding pdf location and width and height.
        v2 = v1.pdf_view(frame,
                        pdf_location = r"Buy_At_Best_Price.pdf", 
                        width = 75, height = 32,bar=False)
    
        # Placing Pdf in my gui.
        v2.pack(padx=56)
    except:
        print("Error in opening pdf in userguide.")

######################################################################################################
#Working of gif in status

def play_gif(gifname,frameforgif):
    frameforgif.grid_forget()
    global play
    play=1

    frameforgif.grid(row=0,column=1,padx=30,rowspan=30,ipadx=40, ipady=20)

    global img
    img= Image.open(gifname)
    lbl =Label(frameforgif,bg=darkblue)
    lbl.place(x=0,y=0)

    try:
        for img in ImageSequence.Iterator(img):
                if play==1:
                    img= img.resize((30,30))
                    img = ImageTk.PhotoImage(img)
                    lbl.config(image=img,borderwidth=0)
                    frameforgif.update()
                    time.sleep(0.03)
                else: break
        if play==1:
            frameforgif.after(0,play_gif(gifname,frameforgif))

    except:
        print('An error in status_gif- image sequence iteration!')


def exitgif(frameforgif):
    global play
    play=0
    frameforgif.grid_forget()


def thumbs_up(frameforgif):
    exitgif(frameforgif)
    frameforgif.grid(row=0,column=1,padx=30,rowspan=50,ipadx=40, ipady=15)
    global img
    img= Image.open("like.png")
    reimg= img.resize((30,30), Image.ANTIALIAS)
    newimg = ImageTk.PhotoImage(reimg)
    lbl1 =Label(frameforgif,bg=darkblue,image=newimg,borderwidth=0)
    lbl1.place(x=0,y=0)    
    time.sleep(3)
    frameforgif.grid_forget()

def disappearing_status_backend(message,labe_lode):
    labe_lode.config(text = message)
    time.sleep(3)
    labe_lode.config(text = "Status: Active")

######################################################################################################

#Sending suggestion email to developer
def send_suggestion_email(suggestion_text,labe_lode):
    global respon
    global username
    if len(suggestion_text) !=0:
        try:
            parser = ConfigParser()
            parser.read('settings.ini')
            username = parser.get('user_profile','user_name')
            useremail = parser.get('user_profile','user_email')
            if username == "null" or useremail == "null":
                username= "Default_User"
                useremail= "Default_User"
            user_info="Username- "+username+", User_email- "+useremail+"\n \n"
            suggestion_mssg=user_info+suggestion_text
            respon=mailing(username,'care.buyatbestprice@gmail.com',f'Suggestion for BABP from - {username}',suggestion_mssg)
            if respon ==True:
                labe_lode.config(text = "Status: Suggestion sent!")
                return True
            else:
                print(error)
                labe_lode.config(text = "Status: Error occured while sending Suggestion!")
                return False
        except:
            print(error)
            labe_lode.config(text = "Status: Error occured while sending Suggestion!")
            return False
    else:
      labe_lode.config(text = "Status: Enter a valid Suggestion!")
      return False

###########email notification system############################################################################################

#email notification system
def email_notification(product_name,productprice_whenadded,product_current_price,custompriceset,old_current_price):
    try:
        if old_current_price==product_current_price:
                        
            print(f"old curent price {old_current_price} = curent price {product_current_price} ")
            return
        parser = ConfigParser()
        parser.read('settings.ini')
        ene_allowed = parser.get('setting_menu','email_notification_engine')
        alertonly_pricedown=parser.get('setting_menu','alert_only_if_price_down')
        username = parser.get('user_profile','user_name')
        useremail = parser.get('user_profile','user_email')
        if ene_allowed=="1":
            productprice_whenadded=int(productprice_whenadded)
            product_current_price=int(product_current_price)
            custompriceset=int(custompriceset)
            if custompriceset!=False and custompriceset!=None:
                if (product_current_price<=custompriceset):
                    mssg =f"Hello {username},😎\nThe Price of Product : {product_name} is decreased beyond your custom set price from ₹{productprice_whenadded} to ₹{product_current_price}.🥳\nWith difference of ₹ {productprice_whenadded-product_current_price} since you added the product 😮 \nIts your dream offer🤩, A Buy-At-Best-Price-deal.😉🤘\nRegards from Team- Buy At Best Price.😁\n\n*Note you can delete this product from MyProducts section to stop its email alerts."
                    subj= f"Price of {product_name} has been decreased beyond your custom set price!🥳"
                    mailbool=mailing('Buy At Best Price Alert!',useremail,subj,mssg)
                    if mailbool:
                        print("Email notification sent!")
                return  
                
            if ((productprice_whenadded<product_current_price)and(alertonly_pricedown=='0')):
                mssg =f"Hello {username},😎\nThe Price of Product : {product_name} is increased from ₹{productprice_whenadded} to ₹{product_current_price}.\nWith increase of ₹{product_current_price-productprice_whenadded} \nSo we suggest to wait until the product price gets cheaper, We'll notify you soon.😉👍\nRegards from Team- Buy At Best Price.😁\n\n*Note you can delete this product from MyProducts section to stop its email alerts."
                subj= f"Price of {product_name} has been increased!😢"
                mailbool=mailing('Buy At Best Price Alert!',useremail,subj,mssg)
                if mailbool:
                    print("Email notification sent!")
            elif (productprice_whenadded>product_current_price):
                mssg =f"Hello {username},😎\nThe Price of Product : {product_name} is decreased from ₹{productprice_whenadded} to ₹{product_current_price}.🥳\nWith difference of -₹{abs(product_current_price-productprice_whenadded)} 😮 \nSo we suggest its a better offer to buy🤩, A Buy-At-Best-Price-deal.😉🤘\nRegards from Team- Buy At Best Price.😁\n\n*Note you can delete this product from MyProducts section to stop its email alerts."
                subj= f"Price of {product_name} has been decreased!🥳"
                mailbool=mailing('Buy At Best Price Alert!',useremail,subj,mssg)
                if mailbool:
                    print("Email notification sent!")  
            else:pass
        else:
            print("Email notification- not allowed by settings!")
    except:
        print("Error in Email notification system!")


#mailing
def mailing(fromm,to,subj,mssg):
    try:
        key = b'rb0OgZ4SAc_GTU9clnPqKKJMAa0dJa4hPTxheYfnfng='
        parser = ConfigParser()
        parser.read('settings.ini')

        saved_em = parser.get('e_p','em')
        saved_pas = parser.get('e_p','pp')

        em=bytes(saved_em.replace('"', ''),'utf-8')
        pa=bytes(saved_pas.replace('"', ''),'utf-8')

        cipher = Fernet(key)

        email = cipher.decrypt(em).decode('utf-8')
        pwd = cipher.decrypt(pa).decode('utf-8')
        
        msg = EmailMessage()
        msg['Subject']=subj
        msg['From']=fromm
        msg['To']=to
        msg.set_content(mssg)

        server = smtplib.SMTP_SSL( "smtp.gmail.com", 465 ) 
        server.login(str(email),str(pwd))
        server.send_message(msg)
        server.quit()
        return True
    except:
        print("Error while mailing.")
        return False

##########Notification working############################################################################################
    

def notification_engine(product_name,prices):
    try:
        parser = ConfigParser()
        parser.read('settings.ini')
        wne_allowed = parser.get('setting_menu','win_notification_engine')
        notify_mssg="Your Product : \n"+product_name+"\nis at price of "+prices
        if wne_allowed=="1":
            notification.notify(
                title = "Buy At Best Price!",
                message = notify_mssg,
                app_icon = "BABP-transparentico.ico",
                timeout=10
                )
        else:
            print("Windows notification- not allowed by settings!")
            
    except:
        print('An exception occurred')
        print(error)

def notification_engine_ifchagneinprice(name_product,price_when_added,current_price,notify_tree,custompriceset,old_current_price):
    try:
        if old_current_price==current_price:
            print(f"old curent price {old_current_price} = curent price {current_price} ")
            return
        parser = ConfigParser()
        parser.read('settings.ini')
        wne_allowed = parser.get('setting_menu','win_notification_engine')
        alertonly_pricedown=parser.get('setting_menu','alert_only_if_price_down')
        price_when_added=int(price_when_added)
        current_price=int(current_price)
        if wne_allowed=="1":
            global mssg
            if custompriceset!=False and custompriceset!=None:
                custompriceset= int(custompriceset)
                if (current_price<=custompriceset):
                    mssg= f"The Price of Product : \n{name_product}\nis decreased beyond your custom set price ₹{custompriceset} to ₹{current_price}\nWith difference of -₹{custompriceset-current_price}"
                    notification.notify(
                    title = "Its the Best Time to Buy!!🤩👍",
                    message = (f"{mssg}"),
                    app_icon = "BABP-transparentico.ico",
                    timeout=5
                    )
                    store_notifications(mssg,notify_tree)
                return
                
            if (price_when_added>current_price):
                mssg= f"The Price of Product : \n{name_product}\nis decreased from ₹{price_when_added} to ₹{current_price}\nWith difference of -₹{price_when_added-current_price}"
                notification.notify(
                title = "Its a Best Time to Buy!!🤩👍",
                message = (f"{mssg}"),
                app_icon = "BABP-transparentico.ico",
                timeout=5
                )
                store_notifications(mssg,notify_tree)
                
            elif ((price_when_added<current_price)and(alertonly_pricedown=='0')):
                mssg= f"The Price of Product : \n{name_product}\nis increased from ₹{price_when_added} to ₹{current_price}\nWith increase of +₹{current_price-price_when_added}"
                notification.notify(
                title = "Buy At Best Price!",
                message = (f"{mssg}"),
                app_icon = "BABP-transparentico.ico",
                timeout=5
                )
                store_notifications(mssg,notify_tree)
            else:
                pass
        else:
            print("Windows notification- not allowed by settings!")    
    except:
        print('An exception occurred in notification engine in background!')
        print(error)

##########Webscarpping - Product searching############################################################################################


def Amazon_Search(entered_url):
    price_list=[]

    req = urllib.request.Request(entered_url, data=None, 
    headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
    })
    sauce = urllib.request.urlopen(req).read()
    soup = bs4.BeautifulSoup(sauce,"html.parser")
    
    try:
        price_soup = soup.find_all('span', attrs={'class':'a-offscreen'})
        
        for span in price_soup:
            
            pr= span.getText()
            price_list.append(pr)
            
        prices=price_list[0]
        
        pr_name = soup.find("span", id="productTitle", attrs={'class':'a-size-large product-title-word-break'})
        for span in pr_name:
            product_name_indetail = span.getText()
        product_name= " ".join(product_name_indetail.split()[:8])+"..."
        
        return product_name,prices

    except:
        print("trying books code!")
        try:
            #######bookk code below
            price_soup = soup.find_all('span', attrs={'class':'a-size-medium a-color-price inlineBlock-display offer-price a-text-normal price3P'})

            for span in price_soup:

                pr= span.getText()
                price_list.append(pr)

            prices=price_list[8]
            #print(price_list)
            pr_name = soup.find("span", id="productTitle", attrs={'class':'a-size-extra-large'})
            
            for span in pr_name:
                product_name_indetail = span.getText()
            product_name= " ".join(product_name_indetail.split()[:8])+"..."
            
            return product_name,prices

        except:
             return False


def Flipkart_Search(entered_url):
    try:
        price_list=[]
        req = urllib.request.Request(entered_url, data=None, 
        headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        })
        sauce = urllib.request.urlopen(req).read()
        soup = bs4.BeautifulSoup(sauce,"html.parser")
        prices = soup.find('div', class_= "_30jeq3 _16Jk6d").getText()
        product_name_indetail = soup.find("span", attrs={'class':'B_NuCI'}).getText()
        product_name=" ".join(product_name_indetail.split()[:8])+"..."
        return product_name,prices
    except:
        return False

def check_price(txt,labe_lode,proname,proprice,frameforgif,p_name,p_price_added,p_url):
    exitgif(frameforgif)
    threading.Thread(target=lambda:play_gif("Spin.gif",frameforgif)).start()
    checkurl = txt
    checkurl.replace(" ", "")
    if len (checkurl)==0:
        labe_lode.config(text="Status: Enter a valid Url!")
        proname.config(text="")
        proprice.config(text="")
        exitgif(frameforgif)
        return False
    elif not ("www." in checkurl or "http://www." in checkurl or "https://www." in checkurl ):
        labe_lode.config(text="Status: Enter a valid Url!")
        proname.config(text="")
        proprice.config(text="")
        exitgif(frameforgif)
        return False
    elif not ("www.amazon." in checkurl) and not ( "www.flipkart." in checkurl):
        labe_lode.config(text="Status: Url not supported !")
        proname.config(text="")
        proprice.config(text="")
        exitgif(frameforgif)
        return False

    else:            
        try:
            entered_url=txt
            if "www.amazon." in entered_url:
                try:
                    product_name,prices=Amazon_Search(entered_url)
                    print(f"Price of {product_name} is : "+prices)
                    proname.config(text=product_name)
                    proprice.config(text=prices)
                    notification_engine(product_name,prices)
                    labe_lode.config(text="Sucess!")
                    #altering the price to str
                    price=prices
                    replace_this = ' ,₹'
                    for i in replace_this:
                        price = price.replace(i, '')
                    price= price.split(".")[0]

                    #checking if price obtained is int or float            
                    print(price)
                    price=eval(price)
                    
                    #inserting data to hidden data entry
                    p_name.insert(0, product_name)
                    p_price_added.insert(0, price)
                    p_url.insert(0, entered_url)                 
                    #threading.Thread(target=lambda:thumbs_up(frameforgif)).start()
                    return True
      
                except:
                    print("Code failed completly!") 
                    #print('An exception occurred')                
                    labe_lode.config(text="Status: An Error Occured")
                    exitgif(frameforgif)
                    proname.config(text="")
                    proprice.config(text="")
                    return False          
                
            elif "www.flipkart." in entered_url:
                try:
                    product_name,prices=Flipkart_Search(entered_url)
                    print(prices)                
                    print(product_name) 
                    proname.config(text=product_name)
                    proprice.config(text=prices)     
                    notification_engine(product_name,prices)
                    labe_lode.config(text="Sucess!")
                    #altering the price to str
                    price=prices
                    replace_this = ' ,₹'
                    price= price.split(".")[0]
                    for i in replace_this:
                        price = price.replace(i, '')
                    #inserting data to hidden data entry
                    p_name.insert(0, product_name)
                    print(price)
                    p_price_added.insert(0, price)
                    p_url.insert(0, entered_url)
                    #threading.Thread(target=lambda:thumbs_up(frameforgif)).start()
                    return True 
                except:
                    print("code failed completly!") 
                    #print('An exception occurred')                
                    labe_lode.config(text="Status: An Error Occured")
                    exitgif(frameforgif)
                    proname.config(text="")
                    proprice.config(text="")
                    return False

        except:
            print('An exception occurred')
            print(error)
            labe_lode.config(text="Status: An Error Occured")
            exitgif(frameforgif)
            proname.config(text="")
            proprice.config(text="")
            return False

############contionus updation#########################################################
#contionus updation
def continous_updation_returnprice(url):
    try:
        entered_url=url
        if "www.amazon." in entered_url:
            try:
                product_name,prices=Amazon_Search(entered_url)
                #altering the price to str
                price=prices
                replace_this = ' ,₹'
                price= price.split(".")[0]
                for i in replace_this:
                    price = price.replace(i, '')
                return price
            except:
                print("somthing failed while traciking price from amazon - contionus_updation")
        elif "www.flipkart." in entered_url:
            try:
                product_name,prices=Flipkart_Search(entered_url)
                #altering the price to str
                price=prices
                replace_this = ' ,₹'
                price= price.split(".")[0]
                for i in replace_this:
                    price = price.replace(i, '')
                return price
            except:
                print("somthing failed while traciking price from flipkart - contionus_updation")
        else:
            print("Wrong url - continous_updation")
    except:
        print("Somthing fired error while traciking price function - contionus_updation")


####################################################################
#Custom price setting

def altertable():
    try:
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # delete record
        c.execute("ALTER TABLE myProducts ADD set_price_limit text")

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
        print("Table altered!")
    except:pass

def addsetprice(rowid,entry_customprice,rootCP,labe_status):
    try:
        altertable()
        setprice=entry_customprice.get()
        if len(setprice)>0:
            setprice=eval(setprice)
        else:
            setprice='NULL'
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # delete record
        c.execute(f"UPDATE myProducts SET set_price_limit = {setprice} WHERE rowid = {rowid}")
        
        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
        print("done")
        labe_status.config(text="Status: Custom Price Alert set!")
        rootCP.destroy()
        time.sleep(3)
        labe_status.config(text="Status: Active")
    except:
        print("Error in adding setprice")

def show_setpriceofproduct(rowid):
    try:
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # query the db
        c.execute(f"SELECT set_price_limit FROM myProducts WHERE rowid = {rowid}")
        records = c.fetchone()
        
        #print(records)
        for record in records:
            set_price=record
        try:
            set_price=eval(set_price)
            return set_price
        except TypeError:
            return False
    except: return False
def customprice_toplevel(root,rowid,labe_status):
    #new toplevel window
    rootCP=Toplevel(root)
    rootCP.title("Set Custom Price Alert")
    #calculating center geometry
    soft_width=460
    soft_height=200
    screen_width=root.winfo_screenwidth()
    screen_height=root.winfo_screenheight()
    x= (screen_width/2)-(soft_width/2)
    y= (screen_height/2)-(soft_height/2)
    #root.geometry("900x645")
    rootCP.geometry(f'{soft_width}x{soft_height}+{int(x)}+{int(y)}')
    rootCP.iconbitmap("BABP-transparentico.ico")
    rootCP.resizable(height=False, width=False)

    # Adding frame as same size of main frame
    frame = Frame(rootCP, bg="#E3DFF9")
    frame.place(x=0, y=0, height=200, width=500)

    # Adding label for custom price alert
    CustomPriceLabel = Label(frame, text="Enter custom price at which you want to recieve an alert message!", bg=purple, font=(our_desired_font2, 11))
    CustomPriceLabel.grid(row=1, column=0, columnspan=10, ipady=10, padx=20, pady=20, sticky=W)

    # adding entry field for custom price alert
    entry_customprice = Entry(frame, font=(our_desired_font2,12), borderwidth=0, bg='White')
    entry_customprice.grid(row=2, column=0, columnspan=10,ipadx=25, ipady=10, padx=120, pady=1, sticky=W)

    submit_setprice=Button(frame,text="Submit", font=(our_desired_font2,12),bg=navyblue,fg='white',command=lambda:threading.Thread(target=lambda:addsetprice(rowid,entry_customprice,rootCP,labe_status)).start())
    submit_setprice.grid(row=3, column=0, columnspan=10,pady=15,ipadx=20,ipady=10)

    set_price=show_setpriceofproduct(rowid)
    if set_price!=None or set_price!=False:
        print(type(set_price))
        entry_customprice.insert(0,set_price)
    #Set the focus to Entry widget
    entry_customprice.focus_set()
    rootCP.mainloop() 

def open_customizeprice(root,my_tree,labe_status):
    try:
        # grab record number
        selected = my_tree.focus()
        
        # grab record values
        values = my_tree.item(selected, 'values')
        rowid=values[0]
        
        #open window for submiting custom price
        customprice_toplevel(root,rowid,labe_status)
        #threading.Thread(target=lambda:customprice_toplevel(root,rowid,labe_status)).start()
    except:
        print("None item from treeview is selected!")
    


#############price graph plotting ########################################################

#price graph plotting 

# mpl.rcParams['toolbar'] = 'None'
backend_bases.NavigationToolbar2.toolitems = ()
toolitems = (
    ('Home', 'Reset original view', 'home', 'home'),
    ('Back', 'Back to  previous view', 'back', 'back'),
    ('Forward', 'Forward to next view', 'forward', 'forward'),
    (None, None, None, None),
    ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
    ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
    ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
    (None, None, None, None),
    ('Save', 'Save the figure', 'filesave', 'save_figure'),
  )
def load_pricegraphtab(comboBox_graph,frameofgrid,Graph_navbar_container):
    try:
        csv_prodName=getvalues_forgraph()
        comboBox_graph['values']=list(csv_prodName.values())
        comboBox_graph.current(0)
        csv_filename=list(csv_prodName.keys())[list(csv_prodName.values()).index(comboBox_graph.get())]
        plot_graph(csv_filename,frameofgrid,Graph_navbar_container)
    except:
        print("Error in load pricegraph tab func in price graph")
def getvalues_forgraph():
    try:
        csv_prodName=dict()
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()
        #select rowid,url colum
        c.execute("SELECT rowid, pro_name FROM myProducts")
        #fetch result
        items= c.fetchall()
        #iterate result
        for item in items:
            rowid=str(item[0])+'.csv'
            pname=item[1]
            csv_prodName[rowid] =pname

        conn.close()
        #print(list(csv_prodName.values()))
        return  csv_prodName
    except:
        print("Error in getvalue for graph func in price graph")

def plot_graph(csv_filename,frameofgrid,Graph_navbar_container):
    try:
        for item in frameofgrid.winfo_children():
          item.destroy()
        for item in Graph_navbar_container.winfo_children():
          item.destroy()
        
        x = []
        y = []
        pname=''
        tempvar=0
        with open(csv_filename,'r') as csvfile:
            #reader = csv.reader(csvfile)
            #firstline = next(reader)
            #print(firstline[])
            lines = csv.reader(csvfile, delimiter=',')
            for row in lines:
                try:
                    row0=row[0]
                    row0=row0.split(' ')[0] 
                    #print(row0)
                    int(row[1])
                    row1=row[1]
                    if tempvar!=row1:
                        tempvar=row1
                    elif tempvar==row1:
                        continue
                    #print(row0,'\t',row1)
                    x.append(row0)
                    y.append(int(row1))
                except:
                    try:
                        pname=row[2].replace('Product Name = ', '')
                    except:
                        continue
                    #print("pname ",pname)
                    continue

        fig = Figure(figsize = (5, 5),dpi = 100)
        plt = fig.add_subplot(111)
        plt.ticklabel_format(useOffset=False)
        plt.plot(x, y, color = 'g', linestyle = 'dashed',
                marker = 'o',label = '')

        fig.subplots_adjust(bottom=0.21,right=0.97,top=0.938,left=0.112)

        plt.tick_params(labelrotation=45)
        plt.set_xlabel('Dates')
        plt.set_ylabel('Prices ₹')
        plt.set_title(pname)
        plt.grid()

        canvas = FigureCanvasTkAgg(fig,master = frameofgrid)  
        canvas.draw()

        # placing the canvas on the Tkinter window
        canvas.get_tk_widget().pack()

        ## creating the Matplotlib toolbar
        toolbar = NavigationToolbar2Tk(canvas,
                                        frameofgrid)
        toolbar.update()

        # placing the toolbar on the Tkinter window
        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

        cursor=mplcursors.cursor(plt,hover=True)
        @cursor.connect("add")
        def _(sel):
            sel.annotation.get_bbox_patch().set(fc="white")
            sel.annotation.arrow_patch.set(arrowstyle="simple", fc="white", alpha=.5)
            x= sel.annotation.get_text().replace("x=", "").replace('y=', "").replace('\n', ";").split(';')
            date="Date= "+ str(x[0])
            price=str(int(float((x[1]))))
            #print(type(price))
            price="Price= "+price
            sel.annotation.set(text=f"{date}\n{price}")
            #window.mainloop()
        
    except:
        print("Error in plotgraph func in price graph")

##########signup Section Functions############################################################################################

#signup section

def signup(root_given):

    try:
        root_given.withdraw()
    except:
        print("Failed hiding the main root window")
    #root_given=root_given

    def save_info(root_given):
        try:
            username_=logNameEntry.get()
            useremail_=logEmailEntry.get().replace(" ","")
            userphn_=int(logPhnnoEntry.get().replace(" ",""))
            userphn_=str(userphn_)
            print(username_,useremail_,userphn_)
            parser = ConfigParser()
            parser.read('settings.ini')
            if (len(username_) > 0) and (len(useremail_) > 0) and ((len(userphn_) > 0) and (len(userphn_) == 10)):
                parser.set('user_profile','user_name',username_) 
                parser.set('user_profile','user_email',useremail_) 
                parser.set('user_profile','user_phnno',userphn_) 
                parser.set('signup','signup_required','0') 
                with open('settings.ini','w') as configsetting:
                    parser.write(configsetting)
                print("Details saved.")
                messagebox.showinfo("Resart", "Information Saved!\n\nPlease restart the Software.")
                try:
                     root_given.deiconify()
                except:
                     print("Failed restoring the main root window")                
                signup_root.destroy()
                root_given.destroy()
                
                return True
            else:
                messagebox.showerror("Error in signup.","Enter a vaild name, email and phone no.")
        except:
            print("error in saving info")
            messagebox.showerror("Error in signup.","Something went wrong!\nMake sure you enter vaild details.")


    def load_signup():
        render =  ImageTk.PhotoImage(Image.open('loginscreen_img.jpg'))
        lbl.configure(image=render)
        lbl.image=render
        print("placing elements")
        logEntryframe.place(x=50, y=150, width=800, height=250)
        logButtonframe.place(x=250, y=410, width=300, height=800)
        logName.grid(row=1, column=0, columnspan=10, ipadx=10, padx=50, pady=15, sticky=W)
        logNameEntry.grid(row=1, column=1, columnspan=10, ipady=10, padx=220, pady=15, sticky=W)
        logEmail.grid(row=2, column=0, columnspan=10, ipadx=10, padx=50, pady=15, sticky=W)
        logEmailEntry.grid(row=2, column=1, columnspan=10, ipady=10, padx=220, pady=15, sticky=W)
        logPhnno.grid(row=3, column=0, columnspan=10, ipadx=10, padx=50, pady=15, sticky=W)
        logPhnnoEntry.grid(row=3, column=1, columnspan=10, ipady=10, padx=220, pady=15, sticky=W)
        Signup.grid(row=1, column=0, columnspan=10, padx=150, pady=20, ipadx=10, sticky=W)

    def play_signup():
        global img, render
        img= Image.open('Babp-login_screen.gif')
        play=1
        try:
            for img in ImageSequence.Iterator(img):
                    if play==1:
                        img = ImageTk.PhotoImage(img)
                        lbl.config(image=img,borderwidth=0)
                        signup_root.update()
                        time.sleep(0.03)
                    else: break
            print("End of signup-gif")
            load_signup()
        except:
            print('An error in status_gif- image sequence iteration!')
            print('Force loading signup page without gif playing...')
            load_signup()
    def on_closing():
        messagebox.showerror('Signup',"Please signup first.")

    signup_root = Toplevel(root_given)
    signup_root.title("Buy at best price signup")

    soft_width=900
    soft_height=645
    screen_width=signup_root.winfo_screenwidth()
    screen_height=signup_root.winfo_screenheight()
    x= (screen_width/2)-(soft_width/2)
    y= (screen_height/2)-(soft_height/2)
    #signup_root.geometry("900x645")
    signup_root.geometry(f'{soft_width}x{soft_height}+{int(x)}+{int(y)}')
    signup_root.iconbitmap("BABP-transparentico.ico")
    signup_root.resizable(height=False, width=False)


    load= Image.open("loginscreen_img.jpg")
    render = ImageTk.PhotoImage(load)
    '''
    imagelabe = Label(signup_root,image=render)
    imagelabe.place(x=0, y=0, height=645, width=900)
    '''
    lbl = Label(signup_root)
    lbl.place(x=0, y=0, height=645, width=900)

    # adding frame for label n entry boxes
    logEntryframe = Frame(signup_root, bg="#FFFFFF")

    logName = Label(logEntryframe, text="Name :", bg="#FFFFFF", font=("Georgia", 20))
    # adding entry field for name
    logNameEntry = Entry(logEntryframe, font=("Calibri",18),width=42, borderwidth=0, bg="#E1E0E0")

    logEmail = Label(logEntryframe, text="Email id :", bg="#FFFFFF", font=("Georgia", 20))
    # adding entry field for email
    logEmailEntry = Entry(logEntryframe, font=("Calibri",18),width=42, borderwidth=0, bg="#E1E0E0")

    logPhnno = Label(logEntryframe, text="Phone No :", bg="#FFFFFF", font=("Georgia", 20))
    # adding entry field for email
    logPhnnoEntry = Entry(logEntryframe, font=("Calibri",18),width=42, borderwidth=0, bg="#E1E0E0")

    # adding frame for buttons n note
    logButtonframe = Frame(signup_root, bg="#E3DFF9")
    #adding modify button
    Signup = Button(logButtonframe, text="Signup", bg="#24305E", font=("Georgia", 20), foreground="white", padx=5, pady=5,command=lambda:save_info(root_given))

    signup_root.protocol("WM_DELETE_WINDOW", on_closing)
    #main loop
    play_signup()
    
    signup_root.mainloop()


###########help and faq section working############################################################################################



def show_ans_Q1(A1):
    A1.config(state=NORMAL)
    if len(A1.get("1.0", "end-1c"))==0:
        A1.grid(row=2,column=0,padx=50,pady=10)
        A1.insert("1.0", 'Ans. This application tracks the price of the product the time we add in to it.It gives us details of that product through the price graph. It also notifies us the price drop of that product through notifications. When we paste the link of product in the linkbar this application start tracking that product continuously. By setting the price limit according to our convenient, it gives us the alerts of price is drop. By showing the user price graph it helps to buy them their wished product in the best limited price.')
        A1.config(state=DISABLED)
    elif len(A1.get("1.0", "end-1c"))>0:
        A1.grid_forget()
        A1.delete("1.0","end")
        A1.config(state=DISABLED)
        

def show_ans_Q2(A2):
    A2.config(state=NORMAL)
    if len(A2.get("1.0", "end-1c"))==0:
        A2.grid(row=4,column=0,padx=50,pady=10)
        A2.insert("1.0", 'Ans. To use this application, you simply need to login by using your username and password or also you can login through your google account. You have to paste the link of the product that you wish to track price. Then click on the search button and Boom! It starts tracking the price of that product in the background on dashboard. It shows you the price graph so you can make a decision of buying product. It also notifies you if the price is drop within a certain limit through notifications. If you want the alert to be in the Email , you can choose those options under settings menu. For that you have to provide further necessary information like email address and phone number, etc. You can also add the multiple links of products which you wish to track price. A price tracker is a technical solution that helps (online) Buyers, track prices of competitors of online websites and dealers. It makes the process of tracking prices easier and less painful, and it also gives information to make pricing decisions.')
        A2.config(state=DISABLED)
    elif len(A2.get("1.0", "end-1c"))>0:
        A2.grid_forget()
        A2.delete("1.0","end")
        A2.config(state=DISABLED)


def show_ans_Q3(A3):
    A3.config(state=NORMAL)
    if len(A3.get("1.0", "end-1c"))==0:
        A3.grid(row=6,column=0,padx=50,pady=10)
        A3.insert("1.0", 'Ans. The current version of this software is only supports urls from Amazon and Flipkart.')
        A3.config(state=DISABLED)
    elif len(A3.get("1.0", "end-1c"))>0:
        A3.grid_forget()
        A3.delete("1.0","end")
        A3.config(state=DISABLED)


def show_ans_Q4(A4):
    A4.config(state=NORMAL)
    if len(A4.get("1.0", "end-1c"))==0:
        A4.grid(row=8,column=0,padx=50,pady=10)
        A4.insert("1.0", 'Ans. The main function of this software is to track the product price and tell you about changes occurred in the price of product.')
        A4.config(state=DISABLED)
    elif len(A4.get("1.0", "end-1c"))>0:
        A4.grid_forget()
        A4.delete("1.0","end")
        A4.config(state=DISABLED)

    

        
            
      
    
    
