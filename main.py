from tkinter import *
from tkinter import messagebox
import os,sys,signal
from typing import Sized
import subprocess



#Root Password Verification Section

def resource_path2():
    CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    spriteFolderPath = os.path.join(CurrentPath,"Assets")
    path = os.path.join(spriteFolderPath)
    newPath = path.replace(os.sep, '/')
    return newPath+"/"
path2 = resource_path2()

backgroundCol = "lightyellow"

pass_win = Tk()

w = 725
h = 186

ws = pass_win.winfo_screenwidth()
hs = pass_win.winfo_screenheight()
x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
pass_win.geometry('%dx%d+%d+%d' % (w, h, x, y))
pass_win.resizable(False,False)
pass_win.config(bg=backgroundCol)
pass_win.title("Authentication")

pass_var = StringVar(pass_win)


ImgFrame = Frame(pass_win,bg=backgroundCol)
ImgFrame.pack(side=LEFT,anchor=N,expand=False)


L_IMG=PhotoImage(file = path2+'Lock.png')

Label(ImgFrame,image=L_IMG,bg=backgroundCol).pack(anchor=N)


Frame2=Frame(pass_win,bg=backgroundCol)
Frame2.pack()
Label(Frame2,bg=backgroundCol,text="Authentication is need to run 'Mac Changer' as the super user",font=("URW Bookman",14,"bold"),justify=LEFT).pack(anchor=N)
Label(Frame2,bg=backgroundCol,text=" ",font=("Arial",1)).pack()
Label(Frame2,bg=backgroundCol,text="'Mac Changer' is attempting to performe an action that requires root privileges.  \nAuthentication is required to performed this action",font=("DejaVu Math TeX Gyre",11),justify=LEFT).pack(anchor=N)
Label(Frame2,text=" \n",font=("Arial",7),bg=backgroundCol).pack()
Label(Frame2,bg=backgroundCol,text="Password:  ",font=("DejaVu Math TeX Gyre",11)).pack(side=LEFT)
ebox =Entry(Frame2,textvariable=pass_var,width=48,show="⚫",font=("DejaVu Math TeX Gyre",13))
ebox.pack(side=LEFT)
ebox.config(relief="ridge",highlightthickness=1,highlightbackground = "blue", highlightcolor= "blue")



L1 = Label(pass_win,fg="#9E2107",text=" ",font=("DejaVu Math TeX Gyre",11),bg=backgroundCol)
L1.pack()

BottomFrame = Frame(pass_win,bg=backgroundCol)
BottomFrame.pack(side=RIGHT,anchor=E)

def authBTN_Fun (e):
    if pass_var.get() == "":
        L1.config(text="Please Input Sudo Password")
    else:
        command = 'sudo whoami'
        passw = pass_var.get()
        runme = os.system('echo %s|sudo -S %s' % (passw, command))
        subprocess.call("clear", shell=True)
        if runme != 0:
            L1.config(text="Wrong Password, Try Again!!")
            ebox.delete(0, "end")
            ebox.insert(0, '')
        else:
            CurrentPath = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
            spriteFolderPath = os.path.join(CurrentPath)
            path = os.path.join(spriteFolderPath)
            newPath = path.replace(os.sep, '/')
            path= newPath+"/Mac Changer (GUI).py"
            path="'"+path+"' 14378"
            pass_win.destroy()
            subprocess.call("sudo python3 "+path, shell=True)


def cancelBtn_fun ():
    msg = messagebox.askyesno("Exit Conformation","Are You Sure You To Exit ?")
    if msg == True:
        pid= os.getpid()
        os.kill(pid,signal.SIGTERM)

ebox.bind('<Return>',authBTN_Fun)


Label(BottomFrame,text="  ",font=("DejaVu Math TeX Gyre",11),bg=backgroundCol).pack(side=RIGHT)
Button(BottomFrame,bg="SlateGray1",font=("DejaVu Math TeX Gyre",10),text="Authenticate",command=lambda:authBTN_Fun(1)).pack(side=RIGHT)
Label(BottomFrame,text="   ",font=("DejaVu Math TeX Gyre",5),bg=backgroundCol).pack(side=RIGHT)
Button(BottomFrame,bg="SlateGray1",font=("DejaVu Math TeX Gyre",10),text="Cancel",command=cancelBtn_fun).pack(side=RIGHT)





pass_win.wm_protocol ("WM_DELETE_WINDOW",cancelBtn_fun )
ebox.focus()

image_path = path2+"auth.png"
pass_win.tk.call('wm', 'iconphoto', pass_win._w, PhotoImage(file=image_path))
pass_win.title("Mac Addres Changer Linux")

pass_win.mainloop()