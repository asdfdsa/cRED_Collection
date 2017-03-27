from Tkinter import *
import threading
import os
import cRED_Main

class cREDGUI(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.start()
        
        self.master=master
        master.title("cRED Data Collection")
        
        self.label=Label(master,text="Please input the directory where you want to save the files")
        self.label.pack()
        
        self.e1=Entry(master,width=50)
        self.e1.pack()
        
        self.label=Label(master,text="Please indicate exposure time")
        self.label.pack()
        
        self.e2=Entry(master,width=50)
        self.e2.pack()
        
        self.warn1=Label(master,text="Invalid path! Please re-enter the path.")
        self.warn1.pack_forget()
        
        self.warn2=Label(master,text="Log file created, do the preparation work, and click collect when ready, stop when done collection")
        self.warn2.pack_forget()
        self.confirm=Button(master,text="Confirm",command=self.ReadDir)
        self.confirm.pack()
        
        self.collect=Button(master,text="Collect",command=self.DataCollection)
        self.collect.pack_forget()
        self.stop=Button(master,text="Stop",command=self.stopCollection)
        self.stop.pack_forget()
        
        self.stopEvent=threading.Event()
        
        self.done=Label(master,text="Data collection Done.")
        self.done.pack_forget()
        
    def ReadDir(self):
        path=r"{}".format(self.e1.get())
        if not os.path.exists(path):
            self.warn2.pack_forget()
            self.collect.pack_forget()
            self.stop.pack_forget()
            self.warn1.pack()
        else:
            self.warn1.pack_forget()
            self.warn2.pack()
            self.collect.pack()
            self.stop.pack()
    
    def DataCollection(self):
        path=r"{}".format(self.e1.get())
        expt=float(self.e2.get())
        cRED_Main.main(path,self.stopEvent,expt)
        
    
    def stopCollection(self):
        self.stopEvent.set()
        self.done.pack()
        
root=Tk()
myGui=cREDGUI(root)
root.mainloop()