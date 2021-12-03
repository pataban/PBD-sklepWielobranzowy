from DataHandler import DataHandler
import tkinter as tk
from tkinter import ttk
from DataFrame import DataFrame

class Gui(tk.Frame):
    def __init__(self, master=tk.Tk()):
        super().__init__(master)
        self.data=DataHandler()
        master.title("sklep wielobranzowy")
        self.pack()
        self.loginFrame=None
        self.menuFrame=None
        self.towaryFrame=None
        self.klienciFrame=None
        self.rachunkiFrame=None
        self.pracownicyFrame=None
        self.userLogin=""
        self.userPasss=""
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

        self.loginLabel=tk.Label(self.menuFrame,text="User: "+self.userLogin)
        self.loginLabel.grid(row=0,column=0)
        logoutButton=tk.Button(self.menuFrame,text="Logout",command=self.logoutUser)
        logoutButton.grid(row=0,column=1)

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
        self.towaryFrame=DataFrame(self)
        self.towaryFrame.pack(side="top")
        self.towaryFrame.backButton["command"]=self.showMenuFrame
        
        self.towarySheet=ttk.Treeview(self.towaryFrame,column=("nazwa","kod","cena"),show="headings")
        #self.dataSheet.column("nazwa")
        self.towarySheet.heading("nazwa", text="Nazwa")
        self.towarySheet.heading("kod", text="Kod")
        self.towarySheet.heading("cena", text="Cena")
        self.towarySheet.grid(row=2)
        self.towarySheet.insert("","end",values=("testname",123,12.56))                   #test data

        towary=self.data.getData("towary")
        for t in towary:
            self.towarySheet.insert("","end",values=(t["nazwa"],t["kod"],t["cena"]))
        
        self.towaryFrame.editButton["command"]=lambda:print(self.towarySheet.item(self.towarySheet.selection()[0])["values"])



    def showKlienciFrame(self):
        self.hideAllFrames()
        if(self.klienciFrame!=None):
            self.klienciFrame.pack(side="top")
            return
        self.klienciFrame=DataFrame(self)
        self.klienciFrame.pack(side="top")
        self.klienciFrame.backButton["command"]=self.showMenuFrame

        self.klienciSheet=ttk.Treeview(self.klienciFrame,column=("imie","nazwisko","nrK","nazwa","NIP"),show="headings")
        #self.klienciSheet.column("nazwa")
        self.klienciSheet.heading("imie", text="Imie")
        self.klienciSheet.heading("nazwisko", text="Nazwisko")
        self.klienciSheet.heading("nrK", text="NrK")
        self.klienciSheet.heading("nazwa", text="Nazwa")
        self.klienciSheet.heading("NIP", text="NIP")
        self.klienciSheet.grid(row=2)
        self.klienciSheet.insert("","end",values=("testname","testsurname",456))                   #test data
        self.klienciSheet.insert("","end",values=("","","","testname","12345678"))                   #test data
        
        klienci=self.data.getData("klienci")
        for k in klienci:
            values=None
            if("NIP" in k.keys()):
                values=("","","",k["nazwa"],k["NIP"])
            else:
                values=(k["imie"],k["nazwisko"],k["nrK"],"","")
            self.klienciSheet.insert("","end",values=values)
        
        self.klienciFrame.editButton["command"]=lambda:print(self.klienciSheet.item(self.klienciSheet.selection()[0])["values"])



    def showRachunkiFrame(self):
        self.hideAllFrames()
        if(self.rachunkiFrame!=None):
            self.rachunkiFrame.pack(side="top")
            return
        self.rachunkiFrame=DataFrame(self)
        self.rachunkiFrame.pack(side="top")
        self.rachunkiFrame.backButton["command"]=self.showMenuFrame

        self.rachunkiSheet=ttk.Treeview(self.rachunkiFrame,column=("nrR","data","nrP"),show="headings")
        #self.rachunkiSheet.column("nazwa")
        self.rachunkiSheet.heading("nrR", text="NrR")
        self.rachunkiSheet.heading("data", text="Data")
        self.rachunkiSheet.heading("nrP", text="NrP")
        self.rachunkiSheet.grid(row=2)
        self.rachunkiSheet.insert("","end",values=("123","dzisiejszaData",789))                   #test data
        
        rachunki=self.data.getData("klienci","rachunki")        #####trzeba napisac osobna funkcje z dobrym querry 
        """for r in rachunki:
            values=(r["nrR"],r["data"],r["nrP"])
            self.rachunkiSheet.insert("","end",values=values)
        
        self.rachunkiFrame.editButton["command"]=lambda:print(self.rachunkiSheet.item(self.rachunkiSheet.selection()[0])["values"])"""

    def showPracownicyFrame(self):
        self.hideAllFrames()
        if(self.pracownicyFrame!=None):
            self.pracownicyFrame.pack(side="top")
            return
        self.pracownicyFrame=DataFrame(self)
        self.pracownicyFrame.pack(side="top")
        self.pracownicyFrame.backButton["command"]=self.showMenuFrame

        self.pracownicySheet=ttk.Treeview(self.pracownicyFrame,column=("imie","nazwisko","nrP","login","haslo"),show="headings")
        #self.pracownicySheet.column("nazwa")
        self.pracownicySheet.heading("imie", text="Imie")
        self.pracownicySheet.heading("nazwisko", text="Nazwisko")
        self.pracownicySheet.heading("nrP", text="NrP")
        self.pracownicySheet.heading("login", text="Login")
        self.pracownicySheet.heading("haslo", text="Haslo")
        self.pracownicySheet.grid(row=2)
        self.pracownicySheet.insert("","end",values=("testname","testsurname",147,"testLogin","testPass"))                   #test data
        
        pracownicy=self.data.getData("pracownicy")
        for p in pracownicy:
            print(p)
            values=(p["imie"],p["nazwisko"],p["nrP"],p["login"],p["haslo"])
            self.pracownicySheet.insert("","end",values=values)
        
        self.pracownicyFrame.editButton["command"]=lambda:print(self.pracownicySheet.item(self.pracownicySheet.selection()[0])["values"])



    def loginUser(self):
        if((self.loginInput.get()=="")or(self.passInput.get()=="")):
            self.loginResultLabel["text"]="no id or password provided"
            self.update()
            return

        if(self.data.login(self.loginInput.get(),self.passInput.get())):
            self.userLogin=self.loginInput.get()
            self.loginInput.delete(0,1000)
            self.userPass=self.passInput.get()
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
        self.userLogin=""
        self.userPasss=""


gui=Gui()
gui.mainloop()