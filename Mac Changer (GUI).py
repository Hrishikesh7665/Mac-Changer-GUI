from getmac import get_mac_address as gma
from generate_mac import generate_mac
from tkinter import ttk, font, messagebox
import os, re, uuid, sys, signal
from tkinter import *
import webbrowser
import subprocess
from datetime import date, datetime
import sqlite3

#For Create Button ToolTip
class ToolTip(object):
    def __init__(self, widget):
        self.widget = widget
        self.tipwindow = None
        self.id = None
        self.x = self.y = 0

    def showtip(self, text):
        "Display text in tooltip window"
        self.text = text
        if self.tipwindow or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 57
        y = y + cy + self.widget.winfo_rooty() +27
        self.tipwindow = tw = Toplevel(self.widget)
        tw.wm_overrideredirect(1)
        tw.wm_geometry("+%d+%d" % (x, y))
        label = Label(tw, text=self.text, justify=LEFT,background="#ffffe0", relief=SOLID, borderwidth=1,font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tipwindow
        self.tipwindow = None
        if tw:
            tw.destroy()

def CreateToolTip(widget, text):
    toolTip = ToolTip(widget)
    def enter(event):
        x = (widget['state'])
        if x == "disabled":
            toolTip.showtip("Button Will Enable After First\nSuccessful MAC Address Change")
        else:
            toolTip.showtip(text)
    def leave(event):
        toolTip.hidetip()
    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

#------------------------------------------



e_port_all = (os.listdir('/sys/class/net/'))
e_port_all.remove('lo')
e_port_final = e_port_all[0]
old_mac_V = (':'.join(re.findall('..', '%012x' % uuid.getnode())))


def resource_path(location):
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    spriteFolderPath = os.path.join(CurrentPath,location)
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath+"/"
Assets_path = resource_path('Assets')
Log_path = resource_path('Log')



file_path = Assets_path+'vendors'


mainwindow = Tk()


def fixed_map(option):
    return [elm for elm in style.map('Treeview', query_opt=option) if elm[:2] != ('!disabled', '!selected')]


style = ttk.Style(mainwindow)
style.theme_use("clam")
style.configure("Treeview.Heading",font=("arial",12, "bold"))
style.configure("Treeview",font=("arial",12),rowheight=25)
style.map('Treeview', foreground=fixed_map('foreground'),background=fixed_map('background'))


e_Port = StringVar(mainwindow)
cur_Mac = StringVar(mainwindow)
old_mac = StringVar(mainwindow)
svar = StringVar(mainwindow)
OP_var = IntVar(mainwindow)
OP_var.set(0)
Check_Box1=IntVar(mainwindow)
Check_Box2=IntVar(mainwindow)
Check_Box1.set(0)
Check_Box2.set(0)
Company_var = StringVar(mainwindow)
e_mac_var = StringVar(mainwindow)
e_mac_var.set("Enter Your Mac Address Here")
e_Port.set("Ethernet Port Name\n"+e_port_final)
old_mac.set("Old Mac Address Is\n"+str(old_mac_V))
cur_Mac.set("Current Mac Address Is\n"+str(old_mac_V))

reset_b_path = PhotoImage(file = Assets_path+ "recover.png")
reset_b_photoimage = reset_b_path.subsample(1, 1)
git_b_path = PhotoImage(file = Assets_path+ "/G.png")
git_b_photoimage = git_b_path.subsample(1, 1)
H_b_path = PhotoImage(file = Assets_path+ "/H.png")
H_b_photoimage = H_b_path.subsample(1, 1)
fb_b_path = PhotoImage(file = Assets_path+ "/fb.png")
fb_b_photoimage = fb_b_path.subsample(1, 1)
company_names = generate_mac.list_vendors(file_path)

company_names = sorted(company_names)
company_names.insert(0,"Not Selected")


Glb = ""
Glb2 = ""
e_mac2 = ""
background_Col = "#dce5ff"
ButtonBack_Col = "#d7ffff"
ButtonBack_Col_active = "#b5ffff"
#"#ffeadc"
#dcffed"


Database_Path_With_Name = Log_path+"Mac Change History.db"


def mainscreen():
    global Glb, Glb2, e_mac2, old_mac_V
    mainwindow.config(bg=background_Col)
    
    for i in mainwindow.winfo_children():
        i.destroy()
    
    TOPFRAME = Frame(mainwindow,bg=background_Col)
    TOPFRAME.pack(side=TOP)

    Label(TOPFRAME,textvariable=e_Port,font=("URW Bookman L",13,"bold"),bg=background_Col,fg="#4b4b6d").pack(side=LEFT)
    Label(TOPFRAME,text="    ",bg=background_Col).pack(side=LEFT)
    Label(TOPFRAME,textvariable=old_mac,font=("URW Bookman L",13,"bold"),bg=background_Col,fg="#4b4b6d").pack(side=LEFT)
    Label(TOPFRAME,text="    ",bg=background_Col).pack(side=LEFT)
    Label(TOPFRAME,textvariable=cur_Mac,font=("URW Bookman L",13,"bold"),bg=background_Col,fg="#4b4b6d").pack(side=LEFT)

    def Update_label (o,n):
        old_mac.set("Old Mac Address Is\n"+str(o))
        cur_Mac.set("Current Mac Address Is\n"+str(n))
        e_mac_var.set("Enter Your Mac Address Here")
        restore_b.config(state=NORMAL)
        OP_Reset_fun()

    def create_log_db(t,o,n):
        status = (os.path.isdir(Log_path))
        if status ==  False:
            os.mkdir(Log_path)
        if os.path.exists(Database_Path_With_Name) != True:
            database = sqlite3.connect(Database_Path_With_Name)
            database.execute('''CREATE TABLE Mac_History
                            (C_No           INTEGER PRIMARY KEY AUTOINCREMENT,
                            C_Date          TEXT,
                            C_Time          TEXT,
                            Port_Name       TEXT,
                            Old_mac         TEXT,
                            New_Mac         TEXT)''')
            database.commit()
            database.close()
        database = sqlite3.connect(Database_Path_With_Name)
        c = database.cursor()
        Date = str(date.today())
        c.execute("INSERT INTO Mac_History (C_Date, C_Time, Port_Name, Old_mac, New_Mac) values(?,?,?,?,?)",(Date, t, e_port_final, o, n))
        database.commit()
        database.close()
    
    
    def mac_gen(new_mac_address):
        global old_mac_V
        new_mac_address = new_mac_address.lower()
        str_mac = cur_Mac.get()
        mac = str_mac[-17:]
        if mac == new_mac_address:
            messagebox.showwarning("Duplicate MAC", "Your Entered MAC Address Is\nAlready Applied")
        elif mac != new_mac_address:
            old_mac_V = gma(interface=e_port_final)
            subprocess.call(["sudo", "ifconfig", e_port_final,"down"])
            subprocess.call(["sudo", "ifconfig", e_port_final,"hw", "ether", new_mac_address])
            subprocess.call(["sudo", "ifconfig", e_port_final,"up"])
            now = datetime.now()
            current_time = now.strftime("%H-%M-%S")
            messagebox.showinfo("MAC Changed Successfully", "Your New MAC Id Is \n"+new_mac_address)
            Update_label(old_mac_V,new_mac_address)
            create_log_db(current_time, old_mac_V, new_mac_address)


    def check_mac():
        str = e_mac_var.get()
        if str == "Enter Your Mac Address Here":
            messagebox.showerror("Invalid Mac","Please Enter Mac Address")
        else:
            x = generate_mac.is_mac_address(str)
            if x == True:
                mac_gen(str)
            else:
                messagebox.showerror("Invalid Mac","Please Enter A Valid\nMac Address")

    def check_mac_1 (e):
        check_mac()
    
    def restore_old_mac():
        str = old_mac_V
        x = generate_mac.is_mac_address(str)
        if x == True:
            msg = messagebox.askyesno("Conformation","Dow You Want To Restore\nYour Old Mac:-\n"+old_mac_V)
            if msg == True:
                mac_gen(str)
        else:
            messagebox.showerror("Invalid Mac","It's Seemes Like Your Old\nMAc Address Is Invalid")

    def random_gen_mac():
        x= generate_mac.vid_file_random(file_path)
        e_mac_var.set(x)
        Glb.config(text="Re-Genarate Mac")
        Glb2.config(state=NORMAL)
        e_mac2.config(font=("Century Schoolbook L",12,"bold"))


    def Specific_Vendor():
        if Company_var.get()=="Not Selected":
            messagebox.showerror("Invalid Vendor","Please Select A Vendor")
        else:
            m = Company_var.get()
            z = generate_mac.vid_file_vendor(file_path,m)
            mac_gen(z)


    OP_Frame = Frame(mainwindow,bg=background_Col)
    Label(OP_Frame,text=" ",font=("URW Bookman L",1),bg=background_Col).pack(side=TOP)
    OP_Frame.pack(side=TOP)

    Button_Frame1 = Frame(mainwindow,bg=background_Col)
    Button_Frame1.pack(side=TOP)

    BodyFrame = Frame(mainwindow,bg=background_Col)
    BodyFrame.pack(side=TOP)

    BodyFrame2 = Frame(mainwindow,bg=background_Col)
    BodyFrame2.pack(side=TOP)




    def OP_select_fun():
        
        
        if OP_var.get() == 0:
            messagebox.showwarning("Error!","Please Select A\nOPtion First")
        elif OP_var.get() == 1:
            SeB.config(text="Selected",state=DISABLED)
            R1.config(state=DISABLED)
            R2.config(state=DISABLED)
            Reset_B.config(state=NORMAL)
            Label(BodyFrame,text=" ",font=("C059",2,"bold"),bg=background_Col).pack()
            Label(BodyFrame,text="Enter Mac Address",font=("C059",12,"bold"),bg=background_Col).pack()
            Label(BodyFrame,text=" ",font=("C059",2,"bold"),bg=background_Col).pack()
            e_mac=Entry(BodyFrame,width=36,justify=CENTER,textvariable=e_mac_var,font=("Century Schoolbook L",11,"italic"),fg="grey")
            e_mac.config(highlightbackground="blue", highlightcolor="blue",highlightthickness=1)
            e_mac.pack()
            e_mac.bind('<Return>',check_mac_1)
            Label(BodyFrame,text=" ",font=("C059",11,"bold"),bg=background_Col).pack()
            Button(BodyFrame,fg="darkorchid4",text="Genarate",activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,command=check_mac,font=("P052",12,"bold")).pack()

            def on_e_mac_click(e):
                if e_mac_var.get() == 'Enter Your Mac Address Here':
                    e_mac.delete(0, "end")
                    e_mac.insert(0, '')
                    e_mac.config(fg = 'black',width=29,font=("Droid Sans Fallback",11,"bold"))

            def on_e_mac_focusout(e):
                if e_mac_var.get () != 'Enter Your Mac Address Here':
                    e_mac.config(fg = 'black',width=29,font=("Droid Sans Fallback",11,"bold"))
                if e_mac_var.get() == '':
                    e_mac_var.set('Enter Your Mac Address Here')
                    e_mac.config(font=("Century Schoolbook L",11,"italic"),width=36,fg="grey")

            e_mac.bind('<FocusIn>', on_e_mac_click)
            e_mac.bind('<FocusOut>', on_e_mac_focusout)


        elif OP_var.get() == 2:
            SeB.config(text="Selected",state=DISABLED)
            R1.config(state=DISABLED)
            R2.config(state=DISABLED)
            Reset_B.config(state=NORMAL)
            for i in BodyFrame.winfo_children():
                i.destroy()

            def CH_Selected (e):
                global Glb, Glb2, e_mac2
                if e == 1:
                    if Check_Box1.get() == 1:
                        Ch_B2.config(state=DISABLED)
                        Check_Box2.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
                    Label(BodyFrame2,text=" ",font=("C059",3,"bold"),bg=background_Col).pack()
                    e_mac2 = Entry(BodyFrame2,state=DISABLED,width=36,justify=CENTER,textvariable=e_mac_var,font=("Century Schoolbook L",12,"bold","italic"))
                    e_mac2.config(disabledforeground="black",disabledbackground="white")
                    e_mac2.config(highlightbackground="blue", highlightcolor="blue",highlightthickness=1)
                    e_mac2.pack()
                    #Label(BodyFrame2,text=" ",font=("C059",3,"bold")).pack()
                    Glb = Button(BodyFrame2,activebackground=ButtonBack_Col_active,fg="darkorchid4",bg = ButtonBack_Col,text="Genarate Mac",font=("P052",12,"bold"),command=random_gen_mac)
                    Glb.pack(side=LEFT,anchor=W)
                    Glb2 = Button(BodyFrame2,activebackground=ButtonBack_Col_active,fg="darkorchid4",bg = ButtonBack_Col,text="Apply Mac",state=DISABLED,font=("P052",12,"bold"),command=check_mac)
                    Glb2.pack(side=RIGHT,anchor=E)
                    Label(BodyFrame2,text="\n\n\n",font=("C059",10,"bold"),bg=background_Col).pack(side=BOTTOM)
                    e_mac_var.set('Click On Genarate Mac')
                    if Check_Box1.get() == 0:
                        Ch_B2.config(state=NORMAL)
                        Check_Box2.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
                        e_mac_var.set('Enter Your Mac Address Here')

                elif e == 2:
                    if Check_Box2.get() == 1:
                        Ch_B1.config(state=DISABLED)
                        Check_Box1.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()
                        Label(BodyFrame2,text="\n",font=("C059",2,"bold"),bg=background_Col).pack()
                        combo = ttk.Combobox(BodyFrame2,textvariable=Company_var,state='readonly',values=company_names,width=16,justify=CENTER,font=("Bitstream Vera Serif",12,"italic"))
                        combo.pack()
                        combo.current(0)
                        Label(BodyFrame2,text="\n",font=("C059",4,"bold"),bg=background_Col).pack()
                        Button(BodyFrame2,fg="darkorchid4",text="Genarate",activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,font=("P052",12,"bold"),command=Specific_Vendor).pack()
                        Label(BodyFrame2,text="\n",font=("C059",5,"bold"),bg=background_Col).pack()

                    if Check_Box2.get() == 0:
                        Ch_B1.config(state=NORMAL)
                        Check_Box1.set(0)
                        for i in BodyFrame2.winfo_children():
                            i.destroy()

            Ch_B1 = Checkbutton(BodyFrame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(1),text="Randomly Genarate MAC",variable=Check_Box1,onvalue=1,offvalue=0)
            Ch_B1.pack()
            Ch_B2 = Checkbutton(BodyFrame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,font=("Cantarell",11,"bold"),command=lambda:CH_Selected(2),text="Genarate MAC With Specific Vendor Byte",variable=Check_Box2,onvalue=1,offvalue=0)
            Ch_B2.pack()
            
            
    def OP_Reset_fun ():
        SeB.config(text="Select",state=NORMAL)
        Reset_B.config(state=DISABLED)
        OP_var.set(0)
        R1.config(state=NORMAL)
        R2.config(state=NORMAL)
        e_mac_var.set("Enter Your Mac Address Here")
        for i in BodyFrame.winfo_children():
            i.destroy()
        for i in BodyFrame2.winfo_children():
            i.destroy()
        Check_Box1.set(0)
        Check_Box2.set(0)

    R1 = Radiobutton(OP_Frame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,text="Enter Mac Address Manually",font=("Quicksand Light",12,"bold"),padx = 20,variable=OP_var,value=1)
    R1.pack(side=LEFT)
    R2 = Radiobutton(OP_Frame,bg=background_Col,highlightbackground=background_Col,activebackground=background_Col,activeforeground="blue",justify=CENTER,text="Generate New Mac Address",font=("Quicksand Light",12,"bold"),padx = 20,variable=OP_var,value=2)
    R2.pack(side=RIGHT)



    SeB = Button(Button_Frame1,text="Select",fg="darkorchid4",font=("Courier 10 Pitch",11,"bold"),activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,command=OP_select_fun)
    Label(Button_Frame1,text="\n",font=("URW Bookman L",1),bg=background_Col).pack(side=TOP)
    SeB.pack(side=LEFT)
    Label(Button_Frame1,text=" "*55,bg=background_Col).pack(side=LEFT)
    Reset_B = Button(Button_Frame1,fg="darkorchid4",font=("Courier 10 Pitch",11,"bold"),activebackground=ButtonBack_Col_active,bg = ButtonBack_Col,text="Reset",state=DISABLED,command=OP_Reset_fun)
    Reset_B.pack(side=RIGHT)


    restore_b = Button(mainwindow,width=30,height=30,bd = 3,image = reset_b_photoimage, state=DISABLED, compound = RIGHT,command=restore_old_mac)
    CreateToolTip(restore_b, text = "Restore Your Old MAC Address\n(If Available)")
    restore_b.place(x=573,y=230)

    OP_Reset_fun()
    create_menu("Home")

image_path = Assets_path+"mac_address.png"
mainwindow.tk.call('wm', 'iconphoto', mainwindow._w, PhotoImage(file=image_path))
mainwindow.title("Mac Addres Changer Linux")

w = 616
h = 273

ws = mainwindow.winfo_screenwidth()
hs = mainwindow.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/3) - (h/2)
mainwindow.geometry('%dx%d+%d+%d' % (w, h, x, y))

mainwindow.resizable(False,False)

def ask_quit():
    x = messagebox.askyesno("Quit Conformation", "Do you want to exit now ?")
    if x==True:
        mainwindow.destroy()


def create_menu(data):
    menubar = Menu(mainwindow)
    if data == "Home":
        menubar.add_command(label="Home",command=mainscreen,state=DISABLED)
        menubar.add_command(label="History",command=openL,state=NORMAL)
        menubar.add_command(label="About", command=aboutWindow,state=NORMAL)

    elif data == "History":
        menubar.add_command(label="Home",command=mainscreen,state=NORMAL)
        menubar.add_command(label="History",command=openL,state=DISABLED)
        menubar.add_command(label="About", command=aboutWindow,state=NORMAL)

    elif data == "About":
        menubar.add_command(label="Home",command=mainscreen,state=NORMAL)
        menubar.add_command(label="History",command=openL,state=NORMAL)
        menubar.add_command(label="About", command=aboutWindow,state=DISABLED)

    menubar.add_command(label="Exit", command=ask_quit,state=NORMAL)
    mainwindow.config(menu=menubar)



def openL():
    for i in mainwindow.winfo_children():
        i.destroy()
    table_frame = Frame(mainwindow,bg=background_Col)
    table_frame.pack(fill=BOTH,expand=1)
    scrollbar_x = Scrollbar(table_frame,orient=HORIZONTAL)
    scrollbar_y = Scrollbar(table_frame,orient=VERTICAL)
    table = ttk.Treeview(table_frame,style = "Treeview",
                columns =("No","Date","Time","Port_Name","O_mac","N_mac"),xscrollcommand=scrollbar_x.set,
                yscrollcommand=scrollbar_y.set)
    table.heading("No",text="No.")
    table.heading("Date",text="Date")
    table.heading("Time",text="Time")
    table.heading("Port_Name",text="Port")
    table.heading("O_mac",text="Old Mac")
    table.heading("N_mac",text="New Mac")
    table["displaycolumns"]=("No", "Date", "Time", "Port_Name","O_mac","N_mac")
    table["show"] = "headings"
    table.column("No",anchor='center',width=35)
    table.column("Date",anchor='center',width=90)
    table.column("Time",anchor='center',width=80)
    table.column("Port_Name",anchor='center',width=75)
    table.column("O_mac",anchor='center',width=150)
    table.column("N_mac",anchor='center',width=150)

    scrollbar_x.pack(side=BOTTOM,fill=X)
    scrollbar_y.pack(side=RIGHT,fill=Y)

    scrollbar_x.configure(command=table.xview)
    scrollbar_y.configure(command=table.yview)

    table.pack(fill=BOTH,expand=1)

    table.tag_configure("col_1",background='#c1e1ec',foreground="#323232")
    table.tag_configure('col_2', background='#add8e6',foreground="#323232")
    
    
    conn = sqlite3.connect(Database_Path_With_Name)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Mac_History")
    rows = cur.fetchall()
    col_ID = 0
    for row in rows:
        number = (row[0])
        date = (row[1]) #Sell Price
        time = (row[2])
        port = (row[3])
        old_m = (row[4])
        new_m = (row[5])
        if (col_ID % 2) == 0:
            table.insert('',END,values=[number,date,time,port,old_m,new_m],tags=('col_1',))
        else:
            table.insert('',END,values=[number,date,time,port,old_m,new_m],tags=('col_2',))
        col_ID = col_ID+1
    create_menu("History")

def aboutWindow():
    for i in mainwindow.winfo_children():
        i.destroy()
    show_Frame = Frame(mainwindow,bg=background_Col)
    show_Frame.pack(side=TOP)
    
    deli = 260           # milliseconds of delay per character
    labl = Label(show_Frame, textvariable=svar,width=80,bg="#666666",fg="white")

    def shif():
        shif.msg = shif.msg[1:] + shif.msg[0]
        svar.set(shif.msg)
        show_Frame.after(deli, shif)

    shif.msg = '            For Any Quarry, Problem, Issue, Or Bug Contact Me On Github Or Facebook.                '
    shif()
    
    labl.pack(fill=X)    
    
    Label(mainwindow,text=" ",font=("URW Bookman L",1),bg=background_Col).pack()
    Label(mainwindow,text="Linux Mac Changer (GUI) Tool",font=("MathJax_AMS",21,"bold"),bg=background_Col).pack()
    Label(mainwindow,text=" ",font=("URW Bookman L",1),bg=background_Col).pack()
    Label(mainwindow,text="Developed By :",font=("GentiumAlt",14,"bold","underline","italic"),bg=background_Col).pack()
    Label(mainwindow,text=" ",font=("URW Bookman L",1),bg=background_Col).pack()
    Label(mainwindow,text="Hrishikesh Patra",font=("MathJax_Math",20,"bold","italic"),bg=background_Col).pack()
    Label(mainwindow,text="Version :- 2.1",font=("GentiumAlt",18,"bold","underline","italic"),bg=background_Col).pack()
    Label(mainwindow,text=" ",font=("URW Bookman L",1),bg=background_Col).pack()
    
    Button_Frame = Frame(mainwindow,bg=background_Col)
    Button_Frame.pack(side=BOTTOM)
    Label(Button_Frame,text="If You Want To Contact Me :- ",font=("GentiumAlt",14,"bold","underline","italic"),bg=background_Col).pack(side=TOP)
    Label(Button_Frame,text=" ",font=("URW Bookman L",1),bg=background_Col).pack(side=TOP)
    def git_b_click():
        webbrowser.open_new_tab('https://github.com/Hrishikesh7665')
    def H_b_click():
        webbrowser.open_new_tab('https://www.hackerrank.com/Hrishikesh7665')
    def fb_b_click():
        webbrowser.open_new_tab('https://www.facebook.com/Isjtijlfti.patra')    

    Label(Button_Frame,text="    ",font=("URW Bookman L",10),bg=background_Col).pack(side=LEFT)
    Button(Button_Frame,width=40,height=40,bd = 3,image = git_b_photoimage, command = git_b_click, compound = RIGHT).pack(side=LEFT)
    Label(Button_Frame,text="     ",font=("URW Bookman L",10),bg=background_Col).pack(side=LEFT)
    Button(Button_Frame,width=40,height=40,bd = 3,image = H_b_photoimage,command = H_b_click, compound = RIGHT).pack(side=LEFT)
    Label(Button_Frame,text="     ",font=("URW Bookman L",10),bg=background_Col).pack(side=LEFT)
    Button(Button_Frame,width=40,height=40,bd = 3,image = fb_b_photoimage,command = fb_b_click, compound = RIGHT).pack(side=LEFT)
    
    Label(Button_Frame,text="\n\n",font=("URW Bookman L",10),bg=background_Col).pack(side=BOTTOM)
    
    
    create_menu("About")


mainwindow.protocol("WM_DELETE_WINDOW", ask_quit)

def start_fun ():
    n = len(sys.argv)
    x = 0
    for i in range(1, n):
        x=(sys.argv[i])
    y=(os.getuid())

    if x == "14378" and y == 0:
        mainscreen()
        mainwindow.mainloop()
    else:
        print("Please run 'main.py'")

if __name__ == '__main__':
    start_fun()
