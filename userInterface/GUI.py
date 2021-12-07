from dbConnectivity.MongoConnector import MongoConnector
import tkinter as tk
from tkinter import ttk
from userInterface.DataFrame import DataFrame
from userInterface.DataFrame.TowaryFrame import TowaryFrame
from userInterface.DataFrame.KlienciFrame import KlienciFrame
from userInterface.DataFrame.RachunkiFrame import RachunkiFrame
from userInterface.DataFrame.PracownicyFrame import PracownicyFrame

class GUI(tk.Frame):
    def __init__(self, shopService, master=tk.Tk()):
        super().__init__(master)
        self.shopService = shopService
        master.title("sklep wielobranzowy")
        self.pack()
        self.loginFrame=None
        self.menuFrame=None
        self.towaryFrame=None
        self.klienciFrame=None
        self.rachunkiFrame=None
        self.pracownicyFrame=None
        self.user=None
        self.showLoginFrame()

    def showLoginFrame(self):
        self.hideAllFrames()
        if(self.loginFrame!=None):
            self.loginFrame.pack(side="top")
            return

        self.loginFrame=tk.Frame(self)
        self.loginFrame.pack(side="top")

        loginLabel=tk.Label(self.loginFrame,text="Login:")
        loginLabel.grid(row=0,column=0)
        self.loginInput=tk.Entry(self.loginFrame)
        self.loginInput.insert(0,"aaa")                           #test defoult data
        self.loginInput.grid(row=0,column=1)
        
        passLabel=tk.Label(self.loginFrame,text="Password:")
        passLabel.grid(row=1,column=0)
        self.passInput=tk.Entry(self.loginFrame)
        self.passInput.insert(0,"aaa")                           #test defoult data
        self.passInput.grid(row=1,column=1)

        self.loginButton=tk.Button(self.loginFrame,text="login",command=self.loginUser)
        self.loginButton.grid(row=2,column=0)
        
        self.loginResultLabel=tk.Label(self.loginFrame,text="")
        self.loginResultLabel.grid(row=2,column=1)
        
    def showMenuFrame(self):
        self.hideAllFrames()
        if(self.menuFrame!=None):
            self.menuFrame.pack(side="top")
            return
        
        self.menuFrame=tk.Frame(self)
        self.menuFrame.pack(side="top")

        tmp=self.user.firstName+" "+self.user.secondName+" ("+str(self.user.nrP)+")"
        self.loginLabel=tk.Label(self.menuFrame,text="User: "+tmp)
        self.loginLabel.grid(row=0,column=0,columnspan=3)
        logoutButton=tk.Button(self.menuFrame,text="Logout",command=self.logoutUser)
        logoutButton.grid(row=0,column=3)

        towaryButton=tk.Button(self.menuFrame,text="Towary",command=self.showTowaryFrame)
        towaryButton.grid(row=1,column=0)

        klienciButton=tk.Button(self.menuFrame,text="Klienci",command=self.showKlienciFrame)
        klienciButton.grid(row=1,column=1)

        rachunkiButton=tk.Button(self.menuFrame,text="Rachunki",command=self.showRachunkiFrame)
        rachunkiButton.grid(row=1,column=2)

        pracownicyButton=tk.Button(self.menuFrame,text="Pracownicy",command=self.showPracownicyFrame)
        pracownicyButton.grid(row=1,column=3)


    def showTowaryFrame(self):
        self.hideAllFrames()
        if(self.towaryFrame!=None):
            self.towaryFrame.pack(side="top")
            return
        self.towaryFrame=TowaryFrame(self,self.shopService)
        self.towaryFrame.pack(side="top")
        self.towaryFrame.backButton["command"]=self.showMenuFrame


    def showKlienciFrame(self):
        self.hideAllFrames()
        if(self.klienciFrame!=None):
            self.klienciFrame.pack(side="top")
            return
        self.klienciFrame=KlienciFrame(self,self.shopService)
        self.klienciFrame.pack(side="top")
        self.klienciFrame.backButton["command"]=self.showMenuFrame


    def showRachunkiFrame(self):
        self.hideAllFrames()
        if(self.rachunkiFrame!=None):
            self.rachunkiFrame.pack(side="top")
            return
        self.rachunkiFrame=RachunkiFrame(self,self.shopService)
        self.rachunkiFrame.pack(side="top")
        self.rachunkiFrame.backButton["command"]=self.showMenuFrame
        

    def showPracownicyFrame(self):
        self.hideAllFrames()
        if(self.pracownicyFrame!=None):
            self.pracownicyFrame.pack(side="top")
            return
        self.pracownicyFrame=PracownicyFrame(self,self.shopService)
        self.pracownicyFrame.pack(side="top")
        self.pracownicyFrame.backButton["command"]=self.showMenuFrame


    def loginUser(self):
        if((self.loginInput.get()=="")or(self.passInput.get()=="")):
            self.loginResultLabel["text"]="no id or password provided"
            self.update()
            return

        self.user=self.shopService.login(self.loginInput.get(),self.passInput.get())
        if(self.user!=None):
            self.loginInput.delete(0,1000)
            self.passInput.delete(0,1000)  
            self.loginResultLabel["text"]=""  
            return self.showMenuFrame()
        else:
            self.loginResultLabel["text"]="wrong id or password"
            self.update()
            return
    
    def logoutUser(self):
        self.clearSessionData()
        return self.showLoginFrame()

    def hideAllFrames(self):
        if(self.loginFrame!=None):   
            self.loginFrame.pack_forget()
            self.pack()
        if(self.menuFrame!=None):   
            self.menuFrame.pack_forget()
            self.pack()
        if(self.towaryFrame!=None):
            self.towaryFrame.pack_forget()
            self.pack() 
        if(self.klienciFrame!=None):
            self.klienciFrame.pack_forget()
            self.pack()
        if(self.rachunkiFrame!=None):
            self.rachunkiFrame.pack_forget()
            self.pack()
        if(self.pracownicyFrame!=None):
            self.pracownicyFrame.pack_forget()
            self.pack()
        return

    def clearSessionData(self):
        self.hideAllFrames()
        self.loginFrame=None
        self.menuFrame=None
        self.towaryFrame=None
        self.klienciFrame=None
        self.rachunkiFrame=None
        self.pracownicyFrame=None
        self.user=None
