from __future__ import division
from Tkinter import *
from PIL import Image, ImageTk
import threading
import os
import cRED_Main
import numpy as np
import videoStream
from instamatic.camera import Camera

class cREDGUI(threading.Thread):
    def __init__(self,master):
        threading.Thread.__init__(self)
        self.start()

        self.master=master
        try:
            self.cam = Camera(kind="timepix")
        except RuntimeError:
            self.cam = Camera(kind="simulate")
        
        master.title("cRED Data Collection")
        
        self.label=Label(master,text="Please input the directory where you want to save the files")
        self.label.pack()
        
        self.e1=Entry(master,width=50)
        self.e1.pack()
        
        self.label=Label(master,text="Please indicate exposure time")
        self.label.pack()
        
        self.e2=Entry(master,width=50)
        self.e2.pack()
        
        self.label=Label(master,text="Indicate the exposure time for live stream")
        self.label.pack()
        
        self.e3=Entry(master,width=25)
        self.e3.insert(0,0.5)
        self.e3.pack()
        
        self.label=Label(master,text="Max intensity for image scaling")
        self.label.pack()
        
        self.e4=Entry(master,width=25)
        self.e4.insert(0,10000)
        self.e4.pack()
        
        self.warn1=Label(master,text="Invalid path! Please re-enter the path.")
        self.warn1.pack_forget()
        
        self.warn2=Label(master,text="Log file created, do the preparation work, and click collect when ready, stop when done collection")
        self.warn2.pack_forget()
        self.confirm=Button(master,text="Confirm",command=self.ReadDir)
        self.confirm.pack()
        
        self.stopEvent=threading.Event()
                
        self.collect=Button(master,text="Collect",command=self.DataCollection)
        self.collect.pack_forget()
        self.stop=Button(master,text="Stop",command=self.callback)
        self.stop.pack_forget()
        
        streaminit=Image.fromarray(np.zeros((512,512)))
        streaminit=ImageTk.PhotoImage(streaminit)
        self.livestream=Label(master,image=streaminit)
        self.livestream.streaminit=streaminit
        self.livestream.pack()
        
        self.thread=threading.Thread(target=None,args=())
        self.thread.start()

        self.done=Label(master,text="Data collection Done.")
        self.done.pack_forget()
    
    def videoloop(self):
        while not self.stopEvent.is_set():
            expt=self.e3.get()
            sc=self.e4.get()
            try:
                expt=float(expt)
                sc=float(sc)
                #frame=self.cam.getImage(expt,1,fastmode=True)
                frame=np.random.randint(2,size=(512,512))
                ind=np.where(frame>sc)
                frame[ind]=sc
                frame=frame/sc*512
                image=Image.fromarray(frame)
                image=ImageTk.PhotoImage(image)
                self.livestream.configure(image=image)
                self.livestream.image=image
                
            except:
                pass
            
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
        
    
    def callback(self):
        self.stopEvent.set()
        self.done.pack()

root=Tk()
myGui=cREDGUI(root)
root.geometry('800x800')
stream = videoStream.VideoViewer(cam="simulate")
root.mainloop()
stream.close()
