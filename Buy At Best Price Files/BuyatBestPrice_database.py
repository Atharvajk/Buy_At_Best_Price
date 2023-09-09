from tkinter import *
from PIL import ImageTk, Image
from tkinter import ttk
import sqlite3
import webbrowser
import csv
import datetime
import os
import pandas as pd
import time
import threading
from winsound import *

######################################################################################################

#personal imports
from BuyatBestPrice_backend import *

######################################################################################################

#global 
global override
override = False

######################################################################################################

# Database
def connect():
        
    # Create a db or connect to one
    conn = sqlite3.connect('MY_Products.db')

    # Create cursor
    c = conn.cursor()

    # Create table
    c.execute("""CREATE TABLE if not exists myProducts(
            pro_name text,
            pro_price_when_added text,
            pro_price_current_price text,
            pro_url text)""")



    conn.commit()
    conn.close()


#######################functions##########################################################
#play bell
def bell():
    return PlaySound("click_one.wav", SND_FILENAME)

#changing status
def disappearing_status(message,labe_lode):
    labe_lode.config(text = message)
    time.sleep(3)
    labe_lode.config(text = "Status: Active")

######################################################################################################

# Create function to delete record
def delete(p_id,my_tree,labe_lode):
    try:
        #delete csv
        file_to_delete = p_id.get()
        print(file_to_delete,type(file_to_delete))
        delete_csv(file_to_delete)

        # Create a db or connect to one
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # delete record
        c.execute("DELETE from myProducts WHERE oid = " + p_id.get())

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
        query(my_tree)
        bell()
        threading.Thread(target=(lambda:disappearing_status("Status: Product deleted!",labe_lode))).start()
    except: 
        print("Error in product deletion.")

##################################################################################################################

internetcheck=False
def internet_popup():
    try:
        urlopen('https://www.google.com', timeout=1)
        return True
        
    except urllib.error.URLError as Error:
        return False

################################################################################################################

#csv file creation 
def create_csv(name,p_name):
    ct = datetime.datetime.now()
    file = f'{name}.csv'
    try:
        os.remove(file)

    except IOError:
        Product_n="Product Name = "+p_name
        with open(file,"a") as file:
            writer = csv.writer(file,lineterminator ="\n")
            fields = ["Timestamp","Price",Product_n]
            writer.writerow(fields)
            print("Created csv & its default fields")

def update_csv(name,price):
    ct = datetime.datetime.now()
    file = f'{name}.csv'
    if os.path.exists(file)==True:
        with open(file,"a") as file:
                writer = csv.writer(file,lineterminator ="\n")
                fields = [ct,price]
                writer.writerow(fields)
    else:
        print("csv files doesnt exist or may be deleted!")

#csv file deletion
def delete_csv(name):
    file = f'{name}.csv'
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")
##########################################################################################

def check(p_name,p_price_added,p_price_current,p_url):
    if (len(p_name.get())==0)and(len(p_price_added.get())==0)and (len(p_price_current.get())==0)and (len(p_url.get())==0):
        return False
    return True

##########################################################################################


# Create submit function for db
def submit(p_name,p_price_added,p_url,my_tree,labe_lode):
    p_price_current=p_price_added
    if check(p_name,p_price_added,p_price_current,p_url)==True:
        altertable()
        # Create a db or connect to one
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # Insert into table
        c.execute("INSERT INTO myProducts VALUES ( :p_name, :p_price_added, :p_price_current, :p_url, Null)",
                {
                    'p_name': p_name.get(),
                    'p_price_added': p_price_added.get(),
                    'p_price_current': p_price_current.get(),
                    'p_url': p_url.get(),
                })

        # Commit changes
        conn.commit()

        #create a csv file of submitted entry
        rowid_submited_now=str(c.lastrowid)
        #print(rowid_submited_now,type(rowid_submited_now))
        create_csv(rowid_submited_now,p_name.get())
        update_csv(rowid_submited_now,p_price_added.get())


        # Close connection
        conn.close()

        # Clear the text boxes
        p_name.delete(0, END)
        p_price_added.delete(0, END)
        p_price_current.delete(0, END)
        p_url.delete(0, END)
        query(my_tree)
        bell()
        threading.Thread(target=(lambda:disappearing_status("Status: Added to My Products!",labe_lode))).start()

        

##########################################################################################

# Create query function for My product
def query(my_tree):
    
        try:
            #delete existing data in treeview
            for record in my_tree.get_children():
                my_tree.delete(record)
        except:
            print("Eror in erasing previous treeview data")
        # connect to database
        conn = sqlite3.connect('MY_Products.db')
        # Create cursor
        c = conn.cursor()

        # query the db
        c.execute("SELECT rowid, * FROM myProducts")
        records = c.fetchall()
        
        #print(records)
        #for record in records:
        #    print(record)
        #my_tree=ttk.Treeview
        my_tree.tag_configure('oddrow', foreground="black", background="white")
        my_tree.tag_configure('evenrow', foreground="black", background="lightblue")    
        
        # Adding style
        style = ttk.Style()

        # adding theme
        style.theme_use('xpnative')

        # configure treeview clr
        style.configure("Treeview",
            bg="#DEE6ED",
            fg="black",
            rowheight=30,
            fieldbackground="#9fc5e8")

        
        # Add our data to the screen
        global count
        count = 0
        for record in records:
            if count % 2 == 0:
                my_tree.insert(parent='', index='end', text='',iid=count, values=(record[0], record[1], record[2], record[3], record[4]), tags=('evenrow',))
            else:
                my_tree.insert(parent='', index='end', text='', iid=count,values=(record[0], record[1], record[2], record[3], record[4]), tags=('oddrow',))
            # increment counter
            count += 1

        # Commit changes
        conn.commit()

        # Close connection
        conn.close()
    
        #print("Error occured in query!")

##########################################################################################

##clear entry boxes if entry boxes contains something
def clear_entry(p_name,p_price_added,p_price_current,p_url,p_id):
    if (check (p_name,p_price_added,p_price_current,p_url)==True):
        # clear entry boxes
        p_name.delete(0, END)
        p_price_added.delete(0, END)
        p_price_current.delete(0, END)
        p_url.delete(0, END)
        p_id.delete(0, END)


# select record
def select_record(p_name,p_price_added,p_price_current,p_url,p_id,my_tree):
    clear_entry(p_name,p_price_added,p_price_current,p_url,p_id)

    # grab record number
    selected = my_tree.focus()
    
    # grab record values
    values = my_tree.item(selected, 'values')
     # output to entry boxes
    p_name.insert(0, values[1])
    p_price_added.insert(0, values[2])
    p_price_current.insert(0, values[3])
    p_url.insert(0, values[4])
    p_id.insert(0, values[0])


##########################################################################################

def openurl_database(p_url):
    if len(p_url.get()) >0:
        bell()
        url=p_url.get()
        webbrowser.open_new(url)

##########################################################################################
def updating_price(c_price,r_id):
    print(c_price,type(c_price))
    print(r_id,type(r_id))
    conn = sqlite3.connect('MY_Products.db')
    # Create cursor
    c = conn.cursor()
    c.execute("UPDATE myProducts SET pro_price_current_price = ? WHERE rowid = ? ",(c_price,r_id,))
    conn.commit()
    #print("updation done!")


################################################################################################################

#contionous updation
def grab_rowid_url(notify_tree,override=False,my_tree=False):
    parser = ConfigParser()
    parser.read('settings.ini')
    cptbg_allowed = parser.get('setting_menu','continous_price_tracking_bg')
    if override==True:                
        print("override is true")
    else:
        print("override is false")
        pass
    if (cptbg_allowed=="1") or (override ==True):
        global internetcheck
        internetcheck=internet_popup()
        if internetcheck==True:
            print("Internet Connected! - starting updation...")
            conn = sqlite3.connect('MY_Products.db')
            # Create cursor
            c = conn.cursor()
            #select rowid,url colum
            c.execute("SELECT rowid, pro_url,pro_price_current_price FROM myProducts")
            #fetch result
            items= c.fetchall()
            #iterate result
            for item in items:
                #item[0]=rowid ,item[1]= urls,item[2]= pro_price_current_price
                print(item[0]," \t",item[1])
                curent_rowid= item[0]
                curent_url= item[1]
                old_current_price= item[2]
                
                try:
                    #run function that tracks price of product using url
                    current_price=continous_updation_returnprice(curent_url)
                    if (current_price == None):
                        print("None type object found! -interation skipped.")
                        continue

                    current_price=eval(current_price)
                    #update price in the database
                    updating_price(current_price,curent_rowid)
                    #update csv file 
                    update_csv(curent_rowid,current_price)

                    #checking old price                    
                    old_current_price=int(old_current_price)

                    #check if there is change in current price and previous price
                    t=conn.cursor()
                    t.execute("SELECT pro_name, pro_price_when_added,set_price_limit FROM myProducts WHERE rowid=?",(curent_rowid,))
                    records = t.fetchmany()
                    strlist = []
                    for record in records:
                        for item in record:
                            strlist.append(item)
                    #strlist[0]=name,strlist[1]=pricewhenadded,strlist[2]=custompriceset, strlist[3]=
                    name_product=strlist[0]
                    price_when_added=int(strlist[1])
                    #old_current_price=int(strlist[2])
                    print("name of product iterating= ",name_product)
                    print("price of product added iterating= ",price_when_added)
                    current_price=int(current_price)
                    #notify if changes in price
                    
                    custompriceset=strlist[2]
                    if custompriceset!=None:
                        custompriceset=eval(custompriceset)
                    else:
                        print("Eror in eval custom price - None type") 
                        custompriceset=False

                    threading.Thread(target=(lambda:notification_engine_ifchagneinprice(name_product,price_when_added,current_price,notify_tree,custompriceset,old_current_price))).start()
                    threading.Thread(target=(lambda:email_notification(name_product,price_when_added,current_price,custompriceset,old_current_price))).start()
                    
                                      
                    if my_tree==False:
                        pass                            
                        #threading.Thread(target=(lambda:notification_engine_ifchagneinprice(name_product,price_when_added,current_price,arg))).start()                                                                      
                        # run to pull data from database / refresh treeview
                    else:
                        threading.Thread(target=(lambda:query(my_tree))).start()                
                    #print("Error in refresing treeview during iteration.")
                    
                except:
                    print("contionus updation iteration aborted due to errors")
                    print("switching to next iteration")
                    continue
            print("Updation cycle 1 completed sucessfully!")
        else: print("no internet connection! - updation failed")
    else:
        print("Continous tracking in bg- not allowed by settings!")

##########################################################################################
# Connect to MyProduct Database (create if not present)
connect()

########## Database for notification#######################################################

# Database for notification
def notification_database():
        
    # Create a db or connect to one
    conn1 = sqlite3.connect('Notification.db')

    # Create cursor
    c1 = conn1.cursor()

    # Create table
    c1.execute("""CREATE TABLE if not exists notification(
            datetime text,
            main_notify BLOB)""")



    conn1.commit()
    conn1.close()



# Create query function for notification
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
    
    '''
    for Notif_record in Notify_records:
        print(Notif_record)
    '''
    # Add our data to the screen
    global count1
    count1 = 0
    #rowID = my_tree.identify('item', event.x, event.y)
    for Notif_record in Notify_records:
        
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
    notify_msg= str(notify_msg)
    notify_msg = notify_msg.replace('\n'," ")
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


# Create function to delete all notifications
def delete_all_notify(notify_tree):
    try:
        # Create a db or connect to one
        conn1 = sqlite3.connect('Notification.db')
        # Create cursor
        c1 = conn1.cursor()

        # delete record
        c1.execute("DELETE FROM notification")


        # Commit changes
        conn1.commit()

        # delete record
        c1.execute("DROP TABLE notification")

        # Commit changes
        conn1.commit()  


        # Close connection
        conn1.close()
        print("All notifications deleted")
        query_notify(notify_tree)
    except:
        # Close connection
        conn1.close()
        print("error in deleting notifications")

####################################################################################################
# Connect to Notification Database (create if not present)
notification_database()

####################################################################################################



