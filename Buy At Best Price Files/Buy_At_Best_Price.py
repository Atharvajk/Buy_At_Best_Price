######## main frontend ####### 

from tkinter import *
from tkinter.font import BOLD
#from turtle import width
from urllib import request
from PIL import ImageTk, Image ,  ImageSequence
from tkinter.ttk import Combobox, Notebook
from tkinter import ttk
from tkinter import messagebox
import webbrowser
import threading
from datetime import date
import sqlite3
import time
from tkinterweb import HtmlFrame #import the HTML browser
from tkinterweb import * #import the HTML browser
from dateutil import parser as timeparser

#Software File imports- backend & database
from BuyatBestPrice_backend import *
from BuyatBestPrice_database import *


###################### Internal Functions ##############################
global today
today=date.today()
def update_dashboard():
    frame3.config(bg=white)
    DashL1.grid(row=0, column=0, columnspan=10, padx=10, pady=1, sticky=W)
    DashL2.grid(row=0, column=1, columnspan=10, padx=200, pady=10, sticky=W)
    DashL3.grid(row=1, column=0, columnspan=10, padx=10, pady=10, sticky=W)
    DashL4.grid(row=1, column=1, columnspan=10, padx=200, pady=10, sticky=W)

    Compare_Prod_Button.grid(row=2, column=0, columnspan=5, padx=60, pady=20, sticky=W)
    addMyProB.grid(row=2, column=1, columnspan=5, padx=275, pady=20, sticky=W)
    openurl_indash.grid(row=2, column=2, columnspan=5, padx=535, pady=20, sticky=W)
    if validate_profile()==False:
        DashL5.grid(row=3, column=0, columnspan=10, padx=20, pady=10, sticky=W)
    space_d_down.grid(row=4, column=0, columnspan=10, padx=20, pady=100, sticky=W)

def update_delete_dashboard():
    frame3.config(bg=purple)
    DashL1.grid_forget()
    DashL2.grid_forget()
    DashL3.grid_forget()
    DashL4.grid_forget()
    Compare_Prod_Button.grid_forget()
    addMyProB.grid_forget()
    openurl_indash.grid_forget()
    DashL5.grid_forget()
    space_d_down.grid_forget()

def del_hidden_entry_data():
    p_name.delete(0, END)
    p_price_added.delete(0, END)
    p_price_current.delete(0, END)
    p_url.delete(0, END)
    p_id.delete(0, END)


def sendandtrack():
    sendinfo()
    threading.Thread(target=(lambda:submit(p_name,p_price_added,p_url,my_tree,labe_status))).start()
def compare_webpage(web_url):
    #on click event - wrapper functions
    def load_new_page(url):
        org_url=url
        r = request.urlopen(url) 
        url=r.url
        print("Athu print this- "+url)
        if "www.amazon." in url or "www.flipkart." in url:
            res=messagebox.askyesno("Compare this Product!","Do you want to add this product to comparison?")
            if res == True:
                threading.Thread(target=(lambda:submit(p_name,p_price_added,p_url,my_tree,labe_status))).start()
                messagebox.showinfo('Buy At Best Price!', 'This product will be added to MyProduct\n and will be compared to exisitng one!')
                print("Exiting........... compare window")
                inputtxt.delete(0, END)
                inputtxt.insert(0, url)
                threading.Thread(target=sendandtrack).start()


                rootC.destroy()
            elif res == False:
                res=messagebox.askyesno("Open in Browser","Do you want to open this product in browser?")
                if res == True:
                    webbrowser.open_new(url)
                
                elif res == False:
                    pass
        else:
            res=messagebox.askyesno("Link not supported!","The link you have clicked is not yet supported! \n\nWe currently only supporting Amazon & Flipkart Products.\n\nStill you want to open link in webbrowser?")
            if res == True:
                messagebox.showinfo('Buy At Best Price!', 'Opening this product in Webrowser.\n\n Sorry for inconvenience!')
                webbrowser.open_new(url)
                time.sleep(3)
                print("Exiting...........compare window")
                rootC.destroy()
            elif res == False:
                pass


    def func_stop(frameC):
      frameC.stop()
      print("frame loading stoped")
    def loaded():
      print("Fully loaded!")
    #########################

    rootC=Toplevel(root)

    rootC.geometry("700x500")
    rootC.iconbitmap("BABP-transparentico.ico")
    frameC = HtmlFrame(rootC,messages_enabled = False) #create HTML browser
    frameC.pack(fill="both", expand=True) #attach the HtmlFrame widget to the parent window
    frameC.enable_images(isenabled=True)
    frameC.enable_crash_prevention(isenabled=True)   
    frameC.load_website(web_url)


    
    #frameC.on_link_click(load_new_page)
    threading.Thread(target=frameC.on_link_click(load_new_page)).start()
    frameC.on_done_loading(loaded)
    rootC.mainloop() 


def compare_products():
    product_name=DashL2.cget("text")
    product_url=DashL4.cget("text")
    print("compare printing -> "+product_name+"\n"+product_url)
    gshopstart= 'https://www.google.com/search?tbm=shop&hl=en-US&psb=1&ved=2ahUKEwjY8Yelgr73AhU7sksFHXbUASwQu-kFegQIABAL&q='
    gshopend= '&gs_lcp=Cgtwcm9kdWN0cy1jYxADUABYAGAAaABwAHgAgAEAiAEAkgEAmAEA&sclient=products-cc'
    tosearch="+".join( product_name.split() )
    weburl=gshopstart+tosearch+'&oq='+tosearch+gshopend

    
    compare_webpage(weburl)
    #webbrowser.open(flipkweburl)
    

def sendinfo():
    if (internet_popup() == True):
        
        entr_txt=inputtxt.get()
        labe_status.config(text = "Status: Retrieving Data ! Please wait.")
        update_dashboard()
        del_hidden_entry_data()
        #threading.Thread(target=(check_price(entr_txt,labe_status,DashL2,DashL4))).start()
        if (check_price(entr_txt,labe_status,DashL2,DashL4,frameforgif,p_name,p_price_added,p_url)== True):
            threading.Thread(target=lambda:thumbs_up(frameforgif)).start()
        else:
            del_hidden_entry_data()
            root.bell()
            update_delete_dashboard()
        #print(p_name.get(),p_price_added.get(), p_url.get())            

def suggestion_timer():
    try:
        parser = ConfigParser()
        parser.read('settings.ini')
        timer= parser.get('suggestion_sent_time','sent_time')
        if timer=='Null':
            send["state"] = "normal"
            send_status['text'] = ''
            return
        timer=timeparser.parse(timer)
        ct = datetime.datetime.now()
        #print(ct)
        if timer>=ct:
            print("Sending Suggestion not allowed")
            send["state"] = "disabled"
            send_status['text'] = '(You can send a new suggestion only after 24hrs)'
        else:
            #allowed
            send_status['text'] = ''
            send["state"] = "normal"
    except:
        print("Error in Suggestion Timer")

def activate_suggestion_sent_timer():
    ct = datetime.datetime.now()
    add=datetime.timedelta(hours=24)
    timer=ct+add
    timer=str(timer)
    print("Timer will end at "+timer)
    parser = ConfigParser()
    parser.read('settings.ini')

    parser.set('suggestion_sent_time','sent_time',timer) 

    with open('settings.ini','w') as configsetting:
        parser.write(configsetting)

def sendsuggestion(): 
    if (internet_popup() == True): 
        root.bell()
        res = messagebox.askquestion('Send Suggestion Email?', 
                            'Do you want to send this suggestion to developers? \n\nNote: You can send only  1 suggestion per day!')
        if res == 'yes' :
            send["state"] = DISABLED
            resp=send_suggestion_email(suggestInputtxt.get("1.0", "end-1c"),labe_status)
            if resp==True:
                activate_suggestion_sent_timer()
                send_status['text'] = '(You can send a new suggestion only after 24hrs)'
                suggestInputtxt.delete(0, END)
            else:
                send_status['text'] = ''
                send["state"] = "normal"
        else :
            labe_status.config(text = "Status: Suggestion canceled!")


def openurl():
    if len(inputtxt.get()) >0:
        if (internet_popup() == True):
            url=inputtxt.get()
            webbrowser.open_new(url)

def internet_popup():
    global internetcheck
    try:
        urlopen('https://www.google.com', timeout=2)
        labe_status.config(text="Status: Online")
        exitgif(frameforgif)
        internetcheck=True        
        return True
        
    except urllib.error.URLError as Error:
        labe_status.config(text="Status: No Internet Connection!")
        res=messagebox.askretrycancel("Warning - No Internet Connection detected!","You need an active internet connection to use this software.")
        if res==True:
            internet_popup()
        exitgif(frameforgif)
        play_gif("wifig.gif",frameforgif)
        internetcheck=False
        return False


def validate_profile():
    try:
        parser = ConfigParser()
        parser.read('settings.ini')
        n= parser.get('user_profile','user_name')
        em= parser.get('user_profile','user_email')
        phn= parser.get('user_profile','user_phnno')
        
        if (n!="null") and (em!="null") and (phn!="null"):
            nameEntry.insert(0,n)
            emailEntry.insert(0,em)
            phnnoEntry.insert(0,phn)
            nameEntry.config(state= "disabled")
            emailEntry.config(state= "disabled")
            phnnoEntry.config(state= "disabled")
            saveB.config(state= "disabled")
            cancelProf.config(state= "disabled")
            return True
        else:
            print("user name,email,phnno missing!!")
            is_signup_required('True')
            return False
    except:
        print("Error in Validating Profile!")


def autostart_winstartup():
    switch(on_button5,'autostart_on_windows_startup',on,off)
    parser = ConfigParser()
    parser.read('settings.ini')
    auto= parser.get('setting_menu','autostart_on_windows_startup')
    if auto=="1":
        auto_start()
    elif auto=="0":
        delete_autostart()
    pass

def is_signup_required(*args):
    forced_flag=None
    for arg in args:
        forced_flag=arg
    parser = ConfigParser()
    parser.read('settings.ini')
    flag= parser.get('signup','signup_required')
    if (flag =='1') or (forced_flag=='True'):
        signup(root)
        return True
    else: return False

def refresh_all():
    refreshB['text'] = 'Refreshing'
    labe_text=labe_status.cget("text")
    labe_status.config(text = "Status: Updating data please wait!")
    threading.Thread(target=(lambda:play_gif("Rolling-2.gif",frameforgif))).start()
    refreshB["state"] = DISABLED
    update_details_live=threading.Thread(target=(lambda:grab_rowid_url(notify_tree,True,my_tree)))
    update_details_live.start()
    update_details_live.join()
    #time.sleep(5)
    print("End of update_details_live")
    refreshB["state"] = 'normal'
    refreshB['text'] = 'Refresh'
    labe_status.config(text = labe_text)
    exitgif(frameforgif)

################################################################

########Colour Pallet##########
purple = "#E3DFF9"
darkblue = "#232430"
darkgray = "#4A4A4F"
white = "#FFFFFF"
navyblue = "#24305E"
bluishgray = "#8EAEBD"
grey = "#E1E0E0"

########Font Pallet##########
our_desired_font = "Georgia"
#our_desired_font = "Comic Sans MS"
#our_desired_font = "bold"
our_desired_font2 = "Calibri"
#################################

#########################################################################################
# Main frame

root = Tk()
root.title("Buy at best price")

soft_width=900
soft_height=645
screen_width=root.winfo_screenwidth()
screen_height=root.winfo_screenheight()
x= (screen_width/2)-(soft_width/2)
y= (screen_height/2)-(soft_height/2)
#root.geometry("900x645")
root.geometry(f'{soft_width}x{soft_height}+{int(x)}+{int(y)}')

root.resizable(height=False, width=False)

# Adding logo into root
root.iconbitmap("BABP-transparentico.ico")

# Adding frame as same size of main frame
frame = Frame(root, bg=purple)
frame.place(x=0, y=0, height=645, width=900)

# adding tabs
Tabs = Notebook(frame)
Tabs.place(x=150, y=45, width=750, height=605)

tab1 = Frame(Tabs, bg=purple)
Tabs.add(tab1, text="Dashboard")
tab2 = Frame(Tabs, bg=purple)
Tabs.add(tab2, text="My Products")
tab3 = Frame(Tabs, bg=purple)
Tabs.add(tab3, text="Price Graph")
tab4 = Frame(Tabs, bg=purple)
Tabs.add(tab4, text="Suggestions")
tab5 = Frame(Tabs, bg=purple)
Tabs.add(tab5, text="Help")
tab6 = Frame(Tabs, bg=purple)
Tabs.add(tab6, text="Settings")
tab7 = Frame(Tabs, bg=purple)
Tabs.add(tab7, text="Notifications")
tab8 = Frame(Tabs, bg=purple)
Tabs.add(tab8, text="Profile")
tab9 = Frame(Tabs, bg=purple)
Tabs.add(tab9, text="Open Guide")
tab10 = Frame(Tabs, bg=purple)
Tabs.add(tab10, text="FAQs")

#Software sidebar Button Frame
# vertical rectangle
frame1 = Frame(frame, bg=darkblue)
frame1.place(x=0, y=0, height=645, width=150)

########## Dashboard Section############################################################################################


# adding dashboard logo in button 
dashlogo = PhotoImage(file="dashboard.png")
dashlogo.subsample(3, 3)

#button in Sidebar
dashboard = Button(frame1, text="Dashboard", bg=darkblue, borderwidth=0, image=dashlogo, compound=TOP, command=lambda: Tabs.select(tab1) )
dashboard.config(font=(our_desired_font, 12), foreground="white")
dashboard.place(x=25, y=110, height=60, width=100)

dashboard.bind("<Enter>",lambda e: dashboard.config(bg=darkgray))
dashboard.bind("<Leave>",lambda e: dashboard.config(bg=darkblue))

#setting tabpane n scrolllbar for dashboard button-->
dashframe = Frame(tab1, bg=purple)

dashcanvas = Canvas(dashframe, bg=purple, width=730, height=570)
dashcanvas.pack(side="left")

dashscrollbar = ttk.Scrollbar(dashframe, orient ="vertical", command = dashcanvas.yview)
dashscrollbar.pack(side=RIGHT, fill="y")

dashcanvas.configure(yscrollcommand=dashscrollbar.set)

dashcanvas.bind('<Configure>',lambda e: dashcanvas.configure(scrollregion=dashcanvas.bbox('all')))

dashmain = Frame(dashcanvas, bg=purple)
dashcanvas.create_window((0,0), window=dashmain, anchor="nw")

dashframe.place(x=1, y=1, width=750, height=575)

#adding label, input textfield & search butten in dashtab
# adding frame for label, entry box & button
framedash = Frame(dashmain, bg=purple, height=200, width=750,borderwidth=0)
framedash.grid(row=0, column=0,  padx=20, pady=30,  sticky=W)


#adding label
l = Label(framedash, text="Enter link of the product", bg=purple)
l.config(font=(our_desired_font, 18, BOLD))
l.grid(row=0, column=0, columnspan=1, padx=30, pady=5, sticky=W)

l1 = Label(framedash, text="you wish to track price!", bg=purple)
l1.config(font=(our_desired_font, 15))
l1.grid(row=1, column=0, columnspan=1, padx=40, pady=5, sticky=W)

#adding input textfield
inputtxt = Entry(framedash, font=(our_desired_font2,15),width=55, bg=white)
inputtxt.grid(row=2, column=0, columnspan=20, ipady=10, padx=30, pady=20, sticky=W)


inputtxt.bind('<Return>',lambda e:threading.Thread(target=sendinfo).start())

#adding search logo in button
searchLogo = PhotoImage(file = "search.png")
searchLogo.subsample(30, 30)

search = Button(framedash, text="Search", bg=navyblue, image=searchLogo, compound=RIGHT, padx=10, pady=5,command=lambda: threading.Thread(target=sendinfo).start())
search.config(font=(our_desired_font, 18), foreground="white")
search.grid(row=3, column=0, columnspan=20, padx=530, pady=10, sticky=W)


# Adding frame below dashboard
frame3 = Frame(dashmain, bg=purple, height=300, width=10)
frame3.grid(row=1, column=0,  padx=0, pady=30,  sticky=W)

# Adding label into frame3
DashL1 = Label(frame3, text="Product Name : ", bg=white)
DashL1.config(font=(our_desired_font, 12))


DashL2 = Label(frame3, text="", bg=white,font=(our_desired_font, 12))


DashL3 = Label(frame3, text="Current price of product : ", bg=white)
DashL3.config(font=(our_desired_font, 12))


DashL4 = Label(frame3, text="", bg=white,font=(our_desired_font, 12))


#adding buttons
Compare_Prod_Button = Button(frame3, text="Compare", bg=navyblue, padx=35, pady=5,command=compare_products)
Compare_Prod_Button.config(font=(our_desired_font, 15), foreground="white")


addMyProB = Button(frame3, text="Add to My Products", bg=navyblue, padx=10, pady=5,command=lambda:threading.Thread(target=(lambda:submit(p_name,p_price_added,p_url,my_tree,labe_status))).start())
addMyProB.config(font=(our_desired_font, 15), foreground="white")


openurl_indash = Button(frame3, text="Open Url", bg=navyblue, padx=25, pady=5,command=openurl)
openurl_indash.config(font=(our_desired_font, 15), foreground="white")


DashL5 = Label(frame3, text="*Note: Please add email & other details in profile section to activate notification system !", bg=white)
DashL5.config(font=(our_desired_font, 10))
space_d_down = Label(frame3,bg=white)


########## My Product Section############################################################################################
# my product tab6
# adding myProducts logo in button
myProLogo = PhotoImage(file="myProducts.png")
myProLogo.subsample(3, 3)

myProducts = Button(frame1, text="My Products", bg=darkblue,borderwidth=0, image=myProLogo, compound=TOP, command=lambda: Tabs.select(tab2))
myProducts.config(font=(our_desired_font, 12), foreground="white")
myProducts.place(x=25, y=190, height=60, width=100)

myProducts.bind("<Enter>",lambda e: myProducts.config(bg=darkgray))
myProducts.bind("<Leave>",lambda e: myProducts.config(bg=darkblue))

# Setting frame for my products
myPromain = Frame(tab2, bg=purple)
myPromain.place(x=0, y=0, width=750, height=605)

# adding frame for label in my products
myProTitleFrame = Frame(myPromain, bg=purple)
myProTitleFrame.place(x=0, y=0, width=750, height=55)

# adding label into frame
myProTitle = Label(myProTitleFrame, text="My Products", bg=purple)
myProTitle.config(font=(our_desired_font, 27, BOLD))
myProTitle.grid(row=0, column=0, columnspan=30, padx=30, pady=10, sticky=W)

# Adding frame for buttons in my products
button_frame = LabelFrame(myPromain, bg=purple)
button_frame.place(x=10, y=68, width=728, height=70)

# Adding Refresh button
refreshB = Button(button_frame, text="Refresh", bg=navyblue, font=(our_desired_font, 15), foreground="white",  command=lambda:threading.Thread(target=refresh_all).start())
refreshB.grid(row=1, column=1, padx=10, pady=12, ipadx=30, sticky=W)

# Adding Delete button
deleteB = Button(button_frame, text="Delete", bg=navyblue, font=(our_desired_font, 15), foreground="white",  command=lambda:threading.Thread(target=(lambda: delete(p_id,my_tree,labe_status))).start())
deleteB.grid(row=1, column=2, padx=10, pady=12, ipadx=30, sticky=W)

# Adding open url button
openurlB = Button(button_frame, text="Open Url", bg=navyblue, font=(our_desired_font, 15), foreground="white",  command=lambda:threading.Thread(target=(lambda: openurl_database(p_url))).start())
openurlB.grid(row=1, column=3,  padx=10, pady=12, ipadx=30, sticky=W)

# Adding open url button
CustomPrice = Button(button_frame, text="Custom Price Alert", bg=navyblue, font=(our_desired_font, 15), foreground="white",command=lambda:threading.Thread(target=(lambda:open_customizeprice(root,my_tree,labe_status))).start())
CustomPrice.grid(row=1, column=4,  padx=10, pady=12, ipadx=5, sticky=W)


#frame holding treeview
frame_tree = Frame(myPromain,bg=purple)
frame_tree.place(x=10, y=150, width=730, height=400)

frametree = Frame(frame_tree, width=730, height=400,bg=purple)
frametree.pack(pady=20)
frametree.pack_propagate(0)
# adding scrollbar
tree_scroll = Scrollbar(frametree,bd=2)
#tree_scroll.place(x=725,y=1,width=5, height=500)
tree_scroll.pack(side=RIGHT, fill=Y)

# create treeview
my_tree = ttk.Treeview(frametree, yscrollcommand=tree_scroll.set, selectmode="extended")
#my_tree.place(x=1, y=1, width=724, height=498)
my_tree.pack(ipadx=730,ipady=400)

#config scrollbar
tree_scroll.config(command=my_tree.yview)

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

# chanfe selected clr
style.map('Treeview',bg=[('selected',"#347083")])


# define columns
my_tree['columns'] = ("RI","Product Name","Product Price(When added)", "Product Price(Current Price)", "Product URL")

# format colums
my_tree.column("#0", width=0, stretch=NO)
my_tree.column("RI", width=0, stretch=NO)
my_tree.column("Product Name",anchor=CENTER, width=160)
my_tree.column("Product Price(When added)", anchor=CENTER, width=180)
my_tree.column("Product Price(Current Price)", anchor=CENTER, width=180)
my_tree.column("Product URL", anchor=CENTER, width=160)

# create headings
my_tree.heading("#0", text="", anchor=W)
my_tree.heading("RI", text="S.R", anchor=W)
my_tree.heading("Product Name", text="Product Name", anchor=CENTER)
my_tree.heading("Product Price(When added)", text="Product Price(When added)", anchor=CENTER)
my_tree.heading("Product Price(Current Price)", text="Product Price(Current Price)", anchor=CENTER)
my_tree.heading("Product URL", text="Product URL", anchor=CENTER)

# Create Striped Row Tags
my_tree.tag_configure('oddrow', background="white")
my_tree.tag_configure('evenrow', background="lightblue")

#empty labels fr storing value
p_name=Entry(myPromain)
p_price_added=Entry(myPromain)
p_price_current=Entry(myPromain)
p_url=Entry(myPromain)
p_id=Entry(myPromain)


# bind treeview
my_tree.bind("<Double-1>", lambda e:select_record(p_name,p_price_added,p_price_current,p_url,p_id,my_tree))

##########Price Graph Section############################################################################################


# adding price graph logo in button
priceGraghLogo = PhotoImage(file="priceGraph.png")
priceGraghLogo.subsample(3, 3)

priceGraph = Button(frame1, text="Price Graph", bg=darkblue,borderwidth=0, image=priceGraghLogo, compound=TOP, command=lambda:[Tabs.select(tab3),load_pricegraphtab(comboBox_graph,priceGraph_container,Graph_navbar_container)] )
priceGraph.config(font=(our_desired_font, 12), foreground="white")
priceGraph.place(x=25, y=270, height=60, width=100)

priceGraph.bind("<Enter>",lambda e: priceGraph.config(bg=darkgray))
priceGraph.bind("<Leave>",lambda e: priceGraph.config(bg=darkblue))

#setting tabpane n scrolllbar for price graph button-->
priceGraphframe = Frame(tab3, bg=purple)

priceGraphframe.place(x=1, y=1, width=750, height=575)

# Adding label in price graph
priceGraphLabe = Label(priceGraphframe, text="Price Graph", bg=purple, font=(our_desired_font, 27, BOLD))
priceGraphLabe.place(x=25,y=10)


#initializing dictionary
csv_prodName=dict()

#dropdown in price graph
comboBox_graph = Combobox(priceGraphframe,state="readonly")
comboBox_graph.place(x=400,y=15,width=300,height=40)

#frame containing graph
priceGraph_container = Frame(priceGraphframe, bg=white, width=710, height=500)
priceGraph_container.place(x=20,y=80,width=710,height=490)

# frame containing navigationbar matplotlib
Graph_navbar_container = Frame(priceGraphframe, bg=white, width=170, height=50)
Graph_navbar_container.place(x=560,y=550,width=170,height=20)

#get values from graph event from combobox
def callbackFunc(event):
    try:
        csv_prodName=getvalues_forgraph()
        print(comboBox_graph.get())
        plot_graph(list(csv_prodName.keys())[comboBox_graph.current()],priceGraph_container,Graph_navbar_container)
    except:
        print("Error in callbackevent func in price graph")

#adding event to dropdown
comboBox_graph.bind("<<ComboboxSelected>>",callbackFunc)

##########Suggestion Section############################################################################################

# adding suggestions logo in button
suggestLogo = PhotoImage(file="suggestion.png")
suggestLogo.subsample(3, 3)

suggestions = Button(frame1, text="Suggestions", bg=darkblue,borderwidth=0, image=suggestLogo, compound=TOP, command=lambda: Tabs.select(tab4))
suggestions.config(font=(our_desired_font, 12), foreground="white")
suggestions.place(x=25, y=350, height=60, width=100)

suggestions.bind("<Enter>",lambda e: suggestions.config(bg=darkgray))
suggestions.bind("<Leave>",lambda e: suggestions.config(bg=darkblue))

#setting tabpane n scrolllbar for suggestions button-->
suggestmain = Frame(tab4, bg=purple)

suggestmain.place(x=1, y=1, width=750, height=575)

#send feedback label
suggestL = Label(suggestmain, text="Send Feedback", bg=purple)
suggestL.config(font=(our_desired_font, 30))
suggestL.grid(row=0, column=0, columnspan=30, padx=240, pady=30, sticky=W)

#adding info label 
suggestL1 = Label(suggestmain, text="''Have feedback? We would love to hear your thoughts, suggestions, concerns or problems with", bg=purple)
suggestL1.config(font=(our_desired_font, 12))
suggestL1.grid(row=1, column=0, columnspan=1, padx=30, pady=1, sticky=W)

suggestL2 = Label(suggestmain, text="anything so, we can improve! Type your feedback in the above box & click on the send buttton.''", bg=purple)
suggestL2.config(font=(our_desired_font, 12))
suggestL2.grid(row=2, column=0, columnspan=1, padx=30, pady=1, sticky=W)

suggestL3 = Label(suggestmain, text="**Please don't share any sensitive information.**", bg=purple)
suggestL3.config(font=(our_desired_font, 12))
suggestL3.grid(row=3, column=0, columnspan=1, padx=30, pady=1, sticky=W)

#adding input textfield for feedback
suggestInputtxt = Text(suggestmain, height=10, width=70, bg=white)
suggestInputtxt.grid(row=4, column=0, columnspan=20, padx=85, pady=25, sticky=W)

#adding send logo in button
sendLogo = PhotoImage(file = "send.png")
sendLogo.subsample(30, 30)

send = Button(suggestmain, text="Send", bg=navyblue, image=sendLogo, compound=RIGHT, padx=5, pady=5, command= lambda: threading.Thread(target=sendsuggestion).start()) #threading.Thread(target=sendsuggestion).start()
send.config(font=(our_desired_font, 18), foreground="white")
send.grid(row=6, column=0, padx=320, pady=15, sticky=W)

#label for suggestion status
send_status = Label(suggestmain, text="", bg=purple)
send_status.config(font=(our_desired_font, 10))
send_status.grid(row=7, column=0, padx=230, pady=15, sticky=W)


##########Help Section############################################################################################

# adding help logo in button
helpLogo = PhotoImage(file="help.png")
helpLogo.subsample(3, 3)

help = Button(frame1, text="Help", bg=darkblue, borderwidth=0, image=helpLogo, compound=TOP, command=lambda: Tabs.select(tab5))
help.config(font=(our_desired_font, 12), foreground="white")
help.place(x=25, y=430, height=60, width=100)


help.bind("<Enter>",lambda e: help.config(bg=darkgray))
help.bind("<Leave>",lambda e: help.config(bg=darkblue))

#setting tabpane n scrolllbar for help button-->
helpframe = Frame(tab5, bg=purple)

helpcanvas = Canvas(helpframe, bg=purple, width=730, height=570)
helpcanvas.pack(side="left")

helpscrollbar = ttk.Scrollbar(helpframe, orient ="vertical", command = helpcanvas.yview)
helpscrollbar.pack(side=RIGHT, fill="y")

helpcanvas.configure(yscrollcommand=helpscrollbar.set)

helpcanvas.bind('<Configure>',lambda e: helpcanvas.configure(scrollregion=helpcanvas.bbox('all')))

helpmain = Frame(helpcanvas, bg=purple)
helpcanvas.create_window((0,0), window=helpmain, anchor="nw")

helpframe.place(x=1, y=1, width=750, height=575)

#mousewhell to scroll event
def bound_to_mousewheel_help(event):
    helpcanvas.bind_all("<MouseWheel>", _on_mousewheel_help)

def _on_mousewheel_help(event):
    helpcanvas.yview_scroll(int(-1*(event.delta/120)), "units")


helpframe.bind('<Enter>', bound_to_mousewheel_help)

# Adding label in help
helpLabe = Label(helpmain, text="Help and Support", bg=purple, font=(our_desired_font, 25, BOLD))
helpLabe.grid(row=0, column=0, columnspan=10, padx=230, pady=10, sticky=W)

helpLabe1 = Label(helpmain, text="Hi, how can we help you?", bg=purple, font=(our_desired_font, 15,'bold'))
helpLabe1.grid(row=1, column=0, columnspan=10, padx=40, pady=10, sticky=W)

helpF = Frame(helpmain, bg=white, height=200, width=300)
helpF.grid(row=2, column=0, columnspan=10, padx=30, pady=20,  sticky=W)

guideLogo = PhotoImage(file="user_guide.png")
guideLogo.subsample(30, 30)

userGuide = Label(helpF, text="User Guide", bg=white, font=(our_desired_font, 15), image=guideLogo, compound=TOP)
userGuide.grid(row=0, column=0, columnspan=10, padx=100, pady=10, sticky=W)

guideNote = Label(helpF, text="Everything you need to know about this software.", bg=white, font=(our_desired_font2, 10))
guideNote.grid(row=1, column=0, columnspan=10, padx=20, pady=0, sticky=W)

guideNote1 = Label(helpF, text="Learn about working and use of this software.", bg=white, font=(our_desired_font2, 10))
guideNote1.grid(row=2, column=0, columnspan=10, padx=25, pady=0, sticky=W)

#adding open guide button
openGuide = Button(helpF, text="Open Guide", bg=navyblue, font=(our_desired_font, 12), foreground="white", padx=5, pady=5, command=lambda:[Tabs.select(tab9), userguidepdfopen(frameuserguide)] )
openGuide.grid(row=3, column=0, columnspan=10, padx=100, pady=10, sticky=W)

helpF1 = Frame(helpmain, bg=white, height=200, width=300)
helpF1.grid(row=2, column=1, columnspan=10, padx=390, pady=20,  sticky=W)

faqLogo = PhotoImage(file="faq.png")
faqLogo.subsample(30, 30)

faqL = Label(helpF1, text="FAQs", bg=white, font=(our_desired_font, 15), image=faqLogo, compound=TOP)
faqL.grid(row=0, column=0, columnspan=10, padx=120, pady=10, sticky=W)

faqNote = Label(helpF1, text="Here are some frequently asked questions,", bg=white, font=(our_desired_font2, 10))
faqNote.grid(row=1, column=0, columnspan=10, padx=20, pady=0, sticky=W)

faqNote1 = Label(helpF1, text="with the best solusions.", bg=white, font=(our_desired_font2, 10))
faqNote1.grid(row=2, column=0, columnspan=10, padx=75, pady=0, sticky=W)

#adding faq button
faqSection = Button(helpF1, text="Go to FAQs", bg=navyblue, font=(our_desired_font, 12), foreground="white", padx=5, pady=5, command=lambda: Tabs.select(tab10))
faqSection.grid(row=3, column=0, columnspan=10, padx=100, pady=10, sticky=W)

#setting tabpane n scrolllbar for faq button-->
faqframe = Frame(tab10, bg=purple)

faqcanvas = Canvas(faqframe, bg=purple, width=730, height=570)
faqcanvas.pack(side="left")

faqscrollbar = ttk.Scrollbar(faqframe, orient ="vertical", command = faqcanvas.yview)
faqscrollbar.pack(side=RIGHT, fill="y")

faqcanvas.configure(yscrollcommand=faqscrollbar.set)

faqcanvas.bind('<Configure>',lambda e: faqcanvas.configure(scrollregion=faqcanvas.bbox('all')))

faqmain = Frame(faqcanvas, bg=purple)
faqcanvas.create_window((0,0), window=faqmain, anchor="nw")

faqframe.place(x=1, y=1, width=750, height=575)

#faqframe.bind('<Enter>', bound_to_mousewheel_faq)
faqframe.bind('<Enter>', lambda e:(faqcanvas.bind_all("<MouseWheel>", lambda e:(faqcanvas.yview_scroll(int(-1*(e.delta/120)), "units")))))

#adding return button for open guide & faq
returnImg = PhotoImage(file="return.png")
returnImg.subsample(3, 3)

###########Open guide Section############################################################################################

#open guide 
returnB1 = Button(tab9, text="Return to Help", bg=purple, font=(our_desired_font, 12), image=returnImg, compound=LEFT,borderwidth=0, command=lambda: Tabs.select(tab5) )
returnB1.grid(row=0, column=0, padx=15, pady=10, ipadx=5, ipady=5, sticky=W)

frameuserguide=Frame(tab9, bg=purple,width=740,height=500)
frameuserguide.grid(row=1, column=0, padx=5, pady=10)

##########FAQ Section############################################################################################

#faq
returnB2 = Button(faqmain, text="Return to Help", bg=purple, font=(our_desired_font, 12), image=returnImg, compound=LEFT, borderwidth=0, command=lambda: Tabs.select(tab5))
returnB2.grid(row=0, column=0, padx=15, pady=10, ipadx=5, ipady=5, sticky=W)

# adding faqs-->
faqLable = Label(faqmain, text="FAQs", bg=purple, font=(our_desired_font, 25))
faqLable.grid(row=1, column=0, columnspan=10, padx=20, pady=10, sticky=W)

# Adding Q & A 1
helpfaq = Frame(faqmain, bg=white, height=1000, width=640)
helpfaq.grid(row=2, column=0, columnspan=10, padx=1, pady=10, ipadx=210, sticky=W)

dropdown1 = PhotoImage(file="dropdown.png")
dropdown1.subsample(3, 3)

###Labels for answers
A1 = Text(helpfaq, height=6, width=70, bg=white, font=(our_desired_font2, 13), borderwidth=0,wrap=WORD)
A2 = Text(helpfaq, height=10, width=70, bg=white, font=(our_desired_font2, 13), borderwidth=0,wrap=WORD)
A3 = Text(helpfaq, height=1, width=70, bg=white, font=(our_desired_font2, 13), borderwidth=0,wrap=WORD)
A4 = Text(helpfaq, height=4, width=70, bg=white, font=(our_desired_font2, 13), borderwidth=0,wrap=WORD)


Q1 = Button(helpfaq, text="Q1. How it works?                                                                 ", bg=white, font=(our_desired_font, 15), image=dropdown1,anchor=W, compound=RIGHT, command= lambda:show_ans_Q1(A1), borderwidth=0)
Q1.grid(row=1, column=0, padx=15, pady=10,ipadx=30, sticky=W)

# Adding Q & A 2
Q2 = Button(helpfaq, text="Q2. How to Use?                                                                   ", bg=white, font=(our_desired_font, 15), image=dropdown1,anchor=W, compound=RIGHT, command=lambda:show_ans_Q2(A2), borderwidth=0)
Q2.grid(row=3, column=0, padx=15, pady=10,ipadx=30, sticky=W)

# Adding Q & A 3
Q3 = Button(helpfaq, text="Q3. This software is currently supports which websites?     ", bg=white, font=(our_desired_font, 15), image=dropdown1,anchor=W, compound=RIGHT, command=lambda:show_ans_Q3(A3), borderwidth=0)
Q3.grid(row=5, column=0, padx=15, pady=10,ipadx=30, sticky=W)

# Adding Q & A 4
Q4 = Button(helpfaq, text="Q4. What is the main function of this software?                   ", bg=white, font=(our_desired_font, 15), image=dropdown1,anchor=W, compound=RIGHT, command=lambda:show_ans_Q4(A4), borderwidth=0)
Q4.grid(row=7, column=0, padx=15, pady=10,ipadx=30, sticky=W)

##########Help n Support Developer Section############################################################################################

helpF2 = Frame(helpmain, bg=white, height=1000, width=670)
helpF2.grid(row=3, column=0, columnspan=10, padx=30, pady=20,  sticky=W)

imgcom= Image.open("BABP-circle non transparent.png")
imgcom= imgcom.resize((70,70), Image.ANTIALIAS)
imgcom = ImageTk.PhotoImage(imgcom)

comL = Label(helpF2, bg=white, image=imgcom, compound=LEFT)
comL.place(x=110, y=30, height=70, width=70)

comL1 = Label(helpF2, text="Buy At Best Price Creators Community", bg=white, font=(our_desired_font, 15))
comL1.place(x=180, y=38, height=40, width=360)

devLab = Label(helpF2, text="Developers and Creators", bg=white, font=(our_desired_font, 15))
devLab.place(x=220, y=90, height=30, width=250)

devProf1 = Frame(helpF2, bg=white)
devProf1.place(x=100, y=170, height=150, width=150)

dev1img= Image.open("dev1.jpg")
dev1img= dev1img.resize((121,150), Image.ANTIALIAS)
dev1img = ImageTk.PhotoImage(dev1img)
lbl1 =Label(devProf1,bg=darkblue,image=dev1img,borderwidth=0)
lbl1.pack()

prof1N = Label(helpF2, text="Atharva J. Khodke (2191841) -", bg=white, font=(our_desired_font, 15))
prof1N.place(x=280, y=200, height=30, width=320)

prof1W1 = Label(helpF2, text="Team-Lead, Project Manager, Software", bg=white, font=(our_desired_font, 13))
prof1W1.place(x=280, y=240, height=30, width=320)

prof1W2 = Label(helpF2, text="Architect, Full-Stack Software Developer.", bg=white, font=(our_desired_font, 13))
prof1W2.place(x=280, y=270, height=30, width=320)


devProf2 = Frame(helpF2, bg=white)
devProf2.place(x=100, y=370, height=150, width=150)

dev2img= Image.open("dev2.jpeg")
dev2img= dev2img.resize((113,150), Image.ANTIALIAS)
dev2img = ImageTk.PhotoImage(dev2img)
lbl2 =Label(devProf2,bg=darkblue,image=dev2img,borderwidth=0)
lbl2.pack()

prof2N = Label(helpF2, text="Swarangi V. Waikar (2191873) -", bg=white, font=(our_desired_font, 15))
prof2N.place(x=280, y=400, height=30, width=320)

prof2W1 = Label(helpF2, text="Front-End Developer, Database ", bg=white, font=(our_desired_font, 13))
prof2W1.place(x=280, y=440, height=30, width=320)

prof2W2 = Label(helpF2, text="Administrator, Analysist, Documentation.", bg=white, font=(our_desired_font, 13))
prof2W2.place(x=280, y=470, height=30, width=320)

devProf3 = Frame(helpF2, bg=white)
devProf3.place(x=100, y=570, height=150, width=150)

dev3img= Image.open("dev3.jpg")
dev3img= dev3img.resize((136,150), Image.ANTIALIAS)
dev3img = ImageTk.PhotoImage(dev3img)
lbl3 =Label(devProf3,bg=darkblue,image=dev3img,borderwidth=0)
lbl3.pack()

prof3N = Label(helpF2, text="Srushti K. More (2191852) -", bg=white, font=(our_desired_font, 15))
prof3N.place(x=280, y=600, height=30, width=320)

prof3W = Label(helpF2, text="Documentation.", bg=white, font=(our_desired_font, 13))
prof3W.place(x=280, y=640, height=30, width=320)

devProf4 = Frame(helpF2, bg=white)
devProf4.place(x=100, y=770, height=150, width=150)

dev4img= Image.open("dev4.png")
dev4img= dev4img.resize((119,150), Image.ANTIALIAS)
dev4img = ImageTk.PhotoImage(dev4img)
lbl4 =Label(devProf4,bg=darkblue,image=dev4img,borderwidth=0)
lbl4.pack()

prof4N = Label(helpF2, text="Diksha R. Tharwal (2191870) -", bg=white, font=(our_desired_font, 15))
prof4N.place(x=280, y=800, height=30, width=320)

prof4W1 = Label(helpF2, text="UI Designer, Documentation,", bg=white, font=(our_desired_font, 13))
prof4W1.place(x=280, y=840, height=30, width=320)

prof4W2 = Label(helpF2, text="Software Tester.", bg=white, font=(our_desired_font, 13))
prof4W2.place(x=280, y=870, height=30, width=320)

separator = ttk.Separator(frame1, orient='horizontal')
separator.place(x=1, y=540,  height=0.5, width=145)

##########Settings Section############################################################################################

# adding setting logo in button
setLogo = PhotoImage(file="settings.png")
setLogo.subsample(30, 30)

settings = Button(frame1, text="Settings", bg=darkblue,borderwidth=0, image=setLogo, compound=TOP, command=lambda: Tabs.select(tab6))
settings.config(font=(our_desired_font, 12), foreground="white")
settings.place(x=25, y=550, height=60, width=100)

settings.bind("<Enter>",lambda e: settings.config(bg=darkgray))
settings.bind("<Leave>",lambda e: settings.config(bg=darkblue))

#setting tabpane n scrolllbar for settings button-->
setframe = Frame(tab6, bg=purple)

setcanvas = Canvas(setframe, bg=purple, width=730, height=570)
setcanvas.pack(side="left")

setscrollbar = ttk.Scrollbar(setframe, orient ="vertical", command = setcanvas.yview)
setscrollbar.pack(side=RIGHT, fill="y")

setcanvas.configure(yscrollcommand=setscrollbar.set)

setcanvas.bind('<Configure>',lambda e: setcanvas.configure(scrollregion=setcanvas.bbox('all')))

setmain = Frame(setcanvas, bg=purple)
setcanvas.create_window((0,0), window=setmain, anchor="nw")

setframe.place(x=1, y=1, width=750, height=575)

# adding label into setting
setTitle = Label(setmain, text="Settings", bg=purple)
setTitle.config(font=(our_desired_font, 25, BOLD))
setTitle.grid(row=0, column=0, columnspan=30, padx=30, pady=5, ipady=10, sticky=W)

# Define Our Images
#on = PhotoImage(file = "on-button.png")
on = Image.open("on-button.png")
on= on.resize((40,40), Image.ANTIALIAS)
on = ImageTk.PhotoImage(on)
#off = PhotoImage(file = "off-button.png")
off = Image.open("off-button.png")
off= off.resize((40,40), Image.ANTIALIAS)
off = ImageTk.PhotoImage(off)

# adding frame for toggle button1
toggleBframe1 = Frame(setmain, bg=purple, height=50, width=500)
toggleBframe1.grid(row=1, column=0, columnspan=10, padx=10, pady=5, sticky=W)

setL1 = Label(toggleBframe1, text="Windows notifications about changes in prices :", bg=purple)
setL1.config(font=(our_desired_font, 15))
setL1.grid(row=0, column=0, columnspan=10, padx=30, pady=5, sticky=W)

# Create A Button Windows notifications
on_button1 = Button(toggleBframe1, image=on, borderwidth=0, bg=purple, activebackground=purple, command = lambda:switch(on_button1,'win_notification_engine',on,off))
on_button1.grid(row=0, column=1, columnspan=10, padx=640, pady=5, sticky=W)

separator = ttk.Separator(toggleBframe1, orient='horizontal')
separator.place(relx=0, rely=0.97, relwidth=5, relheight=1)


# adding frame for toggle button2
toggleBframe2 = Frame(setmain, bg=purple, height=50, width=500)
toggleBframe2.grid(row=2, column=0, columnspan=10, padx=10, pady=5, sticky=W)


setL2 = Label(toggleBframe2, text="Email notifications :", bg=purple)
setL2.config(font=(our_desired_font, 15))
setL2.grid(row=0, column=0, columnspan=10, padx=30, pady=5, sticky=W)


# Create A Button Email notifications
on_button2 = Button(toggleBframe2, image=on, borderwidth=0, bg=purple, activebackground=purple, command = lambda:switch(on_button2,'email_notification_engine',on,off))
on_button2.grid(row=0, column=1, columnspan=10, padx=640, pady=5, sticky=W)

separator = ttk.Separator(toggleBframe2, orient='horizontal')
separator.place(relx=0, rely=0.97, relwidth=5, relheight=1)


# adding frame for toggle button3
toggleBframe3 = Frame(setmain, bg=purple, height=50, width=500)
toggleBframe3.grid(row=3, column=0, columnspan=10, padx=10, pady=5, sticky=W)


setL3 = Label(toggleBframe3, text="Continous price tracking in background :", bg=purple)
setL3.config(font=(our_desired_font, 15))
setL3.grid(row=0, column=0, columnspan=10, padx=30, pady=5, sticky=W)


# Create A Button Continous price tracking in background
on_button3 = Button(toggleBframe3, image=on, borderwidth=0, bg=purple, activebackground=purple, command = lambda:switch(on_button3,'continous_price_tracking_bg',on,off))
on_button3.grid(row=0, column=1, columnspan=10, padx=640, pady=5, sticky=W)

separator = ttk.Separator(toggleBframe3, orient='horizontal')
separator.place(relx=0, rely=0.97, relwidth=5, relheight=1)


# adding frame for toggle button4
toggleBframe4 = Frame(setmain, bg=purple, height=50, width=500)
toggleBframe4.grid(row=4, column=0, columnspan=10, padx=10, pady=5, sticky=W)


setL4 = Label(toggleBframe4, text="Alert only if the price goes down :", bg=purple)
setL4.config(font=(our_desired_font, 15))
setL4.grid(row=0, column=0, columnspan=10, padx=30, pady=5, sticky=W)


# Create A Button Alert only if the price goes down
on_button4 = Button(toggleBframe4, image=on, borderwidth=0, bg=purple, activebackground=purple, command = lambda:switch(on_button4,'alert_only_if_price_down',on,off))
on_button4.grid(row=0, column=1, columnspan=10, padx=640, pady=5, sticky=W)

separator = ttk.Separator(toggleBframe4, orient='horizontal')
separator.place(relx=0, rely=0.97, relwidth=5, relheight=1)



# adding frame for toggle button5
toggleBframe5 = Frame(setmain, bg=purple, height=50, width=500)
toggleBframe5.grid(row=5, column=0, columnspan=10, padx=10, pady=5, sticky=W)


setL5 = Label(toggleBframe5, text="Autostart program on windows startup :", bg=purple)
setL5.config(font=(our_desired_font, 15))
setL5.grid(row=0, column=0, columnspan=10, padx=30, pady=5, sticky=W)


# Create A Button Autostart program on windows startup
on_button5 = Button(toggleBframe5, image=on, borderwidth=0, bg=purple, activebackground=purple, command = autostart_winstartup)
on_button5.grid(row=0, column=1, columnspan=10, padx=640, pady=5, sticky=W)

separator = ttk.Separator(toggleBframe5, orient='horizontal')
separator.place(relx=0, rely=0.97, relwidth=5, relheight=1)


# adding reset button in settings
#resetB = Button(setmain, text="RESET ALL", bg=navyblue)
#resetB.config(font=(our_desired_font, 18), foreground="white")
#resetB.grid(row=6, column=0, padx=280, pady=15, sticky=W)


###########App TopSection############################################################################################

# horizontal rect top

frame2 = Frame(frame, bg=darkblue)
frame2.place(x=150, y=0, height=70, width=750)

##########Notification Section############################################################################################

# adding notification logo in button
notifLogo = Image.open("notification.png")
notifLogo= notifLogo.resize((42,42), Image.ANTIALIAS)
notifLogo = ImageTk.PhotoImage(notifLogo)


#adding notification button
notification = Button(frame2, bg=darkblue, borderwidth=0, image=notifLogo, compound=TOP, command=lambda: Tabs.select(tab7))
notification.place(x=630, y=14, height=42, width=42)


notification.bind("<Enter>",lambda e: notification.config(bg=darkgray))
notification.bind("<Leave>",lambda e: notification.config(bg=darkblue))


notifmain = Frame(tab7, bg=purple)
#notifmain.create_window((0,0), window=notifmain, anchor="nw")
notifmain.place(x=1, y=1, width=750, height=575)

# adding frame for label in notifications
notifTitleFrame = Frame(notifmain, bg=purple)
notifTitleFrame.place(x=1, y=1, width=500, height=55)


# adding label to notification
notifLabe = Label(notifTitleFrame, text="Notifications", bg=purple, font=(our_desired_font, 27, BOLD))
notifLabe.grid(row=0, column=0, columnspan=30, padx=30, pady=10, sticky=W)

# adding frame for del in notifications
notifDelFrame = Frame(notifmain, bg=purple)
notifDelFrame.place(x=600, y=1, width=150, height=55)

# adding delete to notification
notify_delete = Button(notifDelFrame, text="Delete All", bg=navyblue,fg="White", font=(our_desired_font, 10, BOLD),command=lambda:delete_all_notify(notify_tree))
notify_delete.grid(row=0, column=0,columnspan=30,padx=10, pady=10, sticky=W, ipady=8)


########

#frame holding treeview
notif_frame_tree = Frame(notifmain,bg=purple)
notif_frame_tree.place(x=10, y=60, width=730, height=500)

notifFrameTree = Frame(notif_frame_tree, width=730, height=500,bg=purple)
notifFrameTree.pack(pady=20)
notifFrameTree.pack_propagate(0)

# adding scrollbar y
notify_tree_scroll = Scrollbar(notifFrameTree,bd=2)
#tree_scroll.place(x=725,y=1,width=5, height=500)
notify_tree_scroll.pack(side=RIGHT, fill=Y)

# adding horizontal scrollbar x
notify_tree_scrollx = Scrollbar(notifFrameTree,bd=2,orient="horizontal")
#tree_scroll.place(x=725,y=1,width=5, height=500)
notify_tree_scrollx.pack(side=BOTTOM, fill=X)

# create treeview
notify_tree = ttk.Treeview(notifFrameTree,yscrollcommand=notify_tree_scroll.set, selectmode="extended")
notify_tree.config(xscrollcommand=notify_tree_scrollx)
#my_tree.place(x=1, y=1, width=724, height=498)
notify_tree.pack(ipadx=730,ipady=600)

#config scrollbar y
notify_tree_scroll.config(command=notify_tree.yview)
#config scrollbar x
notify_tree_scrollx.config(command=notify_tree.xview)

# define columns
notify_tree['columns'] = ("RI","datetime","main_notify")

# format colums
notify_tree.column("#0", width=0, stretch=NO,minwidth=10)
notify_tree.column("RI", width=0, stretch=NO,minwidth=10)
notify_tree.column("datetime",anchor=W, width=50, minwidth=130)
notify_tree.column("main_notify",anchor=W, width=490, minwidth=800)

# create headings
notify_tree.heading("#0", text="", anchor=W)
notify_tree.heading("RI", text="S.R", anchor=W)
notify_tree.heading("datetime", text="Date-Time", anchor=CENTER)
notify_tree.heading("main_notify", text="Notifications", anchor=CENTER)


# Create Striped Row Tags
notify_tree.tag_configure('oddrow', background="white")
notify_tree.tag_configure('evenrow', background="lightblue")


##########Profile Section############################################################################################

# adding profile logo in button
profLogo = PhotoImage(file="profile.png")
profLogo.subsample(30, 30)

#adding profile button
profile = Button(frame2, bg=darkblue, borderwidth=0, image=profLogo, compound=TOP, command=lambda: Tabs.select(tab8))
profile.place(x=693, y=14, height=42, width=42)

profile.bind("<Enter>",lambda e: profile.config(bg=darkgray))
profile.bind("<Leave>",lambda e: profile.config(bg=darkblue))

#setting tabpane to profile
profframe = Frame(tab8, bg=purple)
profframe.place(x=1, y=1, width=750, height=110)

# adding label to profile
profL = Label(profframe, text="Profile", bg=purple, font=(our_desired_font, 32))
profL.grid(row=0, column=0, columnspan=10, padx=50, pady=5, sticky=W)

profL1 = Label(profframe, text="Make changes in your profile", bg=purple, font=(our_desired_font, 15))
profL1.grid(row=1, column=0, columnspan=10, padx=50, pady=10, sticky=W)

# adding frame for label n entry boxes
profEntryframe = Frame(tab8, bg=white)
profEntryframe.place(x=25, y=120, width=700, height=230)

name = Label(profEntryframe, text="Name :", bg=white, font=(our_desired_font, 15))
name.grid(row=1, column=0, columnspan=10, ipadx=10, padx=30, pady=15, sticky=W)

# declaring string variable
# for storing name and password
username_var=StringVar()
useremail_var=StringVar()
userphnno_var=StringVar()

# adding entry field for name
nameEntry = Entry(profEntryframe,textvariable = username_var, font=(our_desired_font2,15),width=40, borderwidth=0, bg=grey)
nameEntry.grid(row=1, column=1, columnspan=10, ipady=10, padx=170, pady=15, sticky=W)

email = Label(profEntryframe, text="Email id :", bg=white, font=(our_desired_font, 15))
email.grid(row=2, column=0, columnspan=10, ipadx=10, padx=30, pady=15, sticky=W)

# adding entry field for email
emailEntry = Entry(profEntryframe,textvariable = useremail_var, font=(our_desired_font2,15),width=40, borderwidth=0, bg=grey)
emailEntry.grid(row=2, column=1, columnspan=10, ipady=10, padx=170, pady=15, sticky=W)

phnno = Label(profEntryframe, text="Phone No :", bg=white, font=(our_desired_font, 15))
phnno.grid(row=3, column=0, columnspan=10, ipadx=10, padx=30, pady=15, sticky=W)

# adding entry field for email
phnnoEntry = Entry(profEntryframe,textvariable = userphnno_var, font=(our_desired_font2,15),width=40, borderwidth=0, bg=grey)
phnnoEntry.grid(row=3, column=1, columnspan=10, ipady=10, padx=170, pady=15, sticky=W)

# adding frame for buttons n note
profButtonframe = Frame(tab8, bg=purple)
profButtonframe.place(x=25, y=360, width=700, height=200)

#adding modify button
modify = Button(profButtonframe, text="Modify", bg=navyblue, font=(our_desired_font, 18), foreground="white", padx=5, pady=5,command=lambda:profile_modify(nameEntry,emailEntry,phnnoEntry,saveB,cancelProf))
modify.grid(row=1, column=0, columnspan=10, padx=130, pady=30, sticky=W)

#adding cancel button
cancelProf = Button(profButtonframe, text="Cancel", bg=navyblue, font=(our_desired_font, 18), foreground="white", padx=5, pady=5,command=lambda:profile_cancel(nameEntry,emailEntry,phnnoEntry))
cancelProf.grid(row=1, column=1, columnspan=10, padx=305, pady=30, sticky=W)

#adding save button
saveB = Button(profButtonframe, text="Save", bg=navyblue, font=(our_desired_font, 18), foreground="white", padx=5, pady=5,command=lambda:profile_save(username_var,useremail_var,userphnno_var,nameEntry,emailEntry,phnnoEntry,saveB,cancelProf,labe_status,Tabs,tab1))
saveB.grid(row=1, column=2, columnspan=10, ipadx=10, padx=480, pady=10, sticky=W)

# adding note* label
note = Label(profButtonframe, text="*Note: Notifications are currently only supported for Emails !", bg=purple, font=(our_desired_font, 12))
note.grid(row=2, column=0, columnspan=10, padx=135, pady=50, sticky=W)

#status frame for label n gif
Status_frame = Frame(frame, bg=darkblue)
Status_frame.place(x=20, y=25, height=40, width=500)

#adding status label
labe_status = Label(Status_frame, text="Status: Active", bg=darkblue ,font=(our_desired_font, 10),foreground="white",anchor=W,justify=LEFT)
labe_status.grid(row=0,column=0)

#adding gif_status
frameforgif =Frame (Status_frame, bg=darkblue)



########## end ###############################################################################

#check if signup is required
is_signup_required()


try:
    #checking profile
    validate_profile()
    
    #updating profile

    s1,b1,b2,b3,b4,b5=validate_buttons(on,off,on_button1,on_button2,on_button3,on_button4,on_button5)

    #check if sending suggestion is allowed
    suggestion_timer()

    #updating treeview from database
    query(my_tree)
    query_notify(notify_tree)

    #checking if internet is connected
    internetcheck=False
    ip_t=threading.Thread(target=(internet_popup))
    ip_t.start()

    #start contionos updation-cycle1
    bg_updation_t=threading.Thread(target=(lambda:grab_rowid_url(notify_tree,my_tree=my_tree)))
    bg_updation_t.start()
except:print("Errors in after root functions")
#main loop
root.mainloop()
