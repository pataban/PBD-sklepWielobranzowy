import tkinter as tk
from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from models.Client import Client
from userInterface.DocEditFrame import DocEditFrame

class KlienciFrame(DataFrame):
    def __init__(self,master,shopService):
        super().__init__(master,shopService)
        
        columns=("id","imie","nazwisko","nrK","nazwa","NIP","tel","adres")
        self.klienciSheet=ttk.Treeview(self,column=columns,show="headings")
        self.klienciSheet["displaycolumns"]=columns[1:]
        self.klienciSheet.column("imie", width=100,anchor=tk.W)
        self.klienciSheet.column("nazwisko", width=100,anchor=tk.W)
        self.klienciSheet.column("nrK", width=100,anchor=tk.E)
        self.klienciSheet.column("nazwa", width=100,anchor=tk.W)
        self.klienciSheet.column("NIP", width=100,anchor=tk.E)
        self.klienciSheet.column("tel", width=100,anchor=tk.E)
        self.klienciSheet.column("adres", width=200,anchor=tk.W)
        self.klienciSheet.heading("imie", text="Imie")
        self.klienciSheet.heading("nazwisko", text="Nazwisko")
        self.klienciSheet.heading("nrK", text="NrK")
        self.klienciSheet.heading("nazwa", text="Nazwa")
        self.klienciSheet.heading("NIP", text="NIP")
        self.klienciSheet.heading("tel", text="Tel")
        self.klienciSheet.heading("adres", text="Adres")
        self.klienciSheet.grid(row=2)
        self.klienciSheet.insert("","end",values=("id4456","testname","testsurname",456))              #test data
        self.klienciSheet.insert("","end",values=("id87964","","","","testname","12345678"))            #test data

        self.loadFullSheet()

    def loadFullSheet(self):
        self.klienciSheet.delete(*self.klienciSheet.get_children())
        self.fillSheet(self.shopService.findClients())

    def fillSheet(self,clients):
        for c in clients:
            self.klienciSheet.insert("","end",values=(c.object_id,c.firstName,c.secondName,c.clientNr,c.name,c.vatId,c.telephone,c.address))
        
        
    def searchButtonListener(self):
        category=self.categoryInput.get()
        value=self.valueInput.get()
        if(category=="nrK")or(category=="nrk"):
            try:
                value=int(value)
            except:
                return
            self.klienciSheet.delete(*self.klienciSheet.get_children())
            res=self.shopService.findClientByClientNr(value)
            if(res==None):
                res=[]
            else:
                res=[res]
            self.fillSheet(res)
        elif(category=="NIP" or category=="nip" or category=="Nip"):
            self.klienciSheet.delete(*self.klienciSheet.get_children())
            res=self.shopService.findClientByVatId(value)
            if(res==None):
                res=[]
            else:
                res=[res]
            self.fillSheet(res)
        elif(category=="" and value==""):
            self.loadFullSheet()


    def getRecomendedKeys(self):
        keys={"imie":"","nazwisko":"","nrK":self.shopService.generateNewNrK(),"nazwa":"","NIP":"","tel":"","adres":""}
        return keys
        
    def validateObligatoryKeys(self,dict):
        if not super().validateObligatoryKeys(dict):
            return False
        if (not "nrK" in dict) and (not "NIP" in dict):
            self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
            return False
        return True

    def createNewDocument(self,dict):
        if not super().createNewDocument(dict):
            return False
        for key in self.recomendedKeys:
            if not key in dict:
                dict[key]=None
        client=Client(dict["imie"],dict["nazwisko"],dict["nazwa"],dict["tel"],dict["NIP"],dict["adres"],dict["nrK"])
        if(self.shopService.insertClient(client)):
            self.klienciSheet.insert("","end",values=(client.object_id,client.firstName,client.secondName,client.clientNr,client.name,client.vatId,client.telephone,client.address))

    def editButtonListener(self):
        try:
            selected=self.klienciSheet.item(self.klienciSheet.selection()[0])["values"]
        except:
            return
        
        klient=None
        print(selected)
        if selected[3]!="None":
            klient=self.shopService.findClientByClientNr(selected[3])
        else:
            klient=self.shopService.findClientByVatId(str(selected[5]))

        keys={"imie":klient.firstName,"nazwisko":klient.secondName,"nrK":klient.clientNr,"nazwa":klient.name,"NIP":klient.vatId,"tel":klient.telephone,"adres":klient.address}
        self.itemEditFrame=DocEditFrame(self,"Edytowanie elementu:",keys)
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.updateDocument(self.itemEditFrame.getItem())


    def updateDocument(self,dict):
        if not super().updateDocument(dict):
            return False
        
        klient=None
        if "nrK" in dict.keys():
            klient=self.shopService.findClientByClientNr(dict["nrK"])
        if(klient==None):
            klient=self.shopService.findClientByVatId(dict["NIP"])
        
        if "imie" in dict.keys():
            klient.firstName =dict["imie"]
        if "nazwisko" in dict.keys():
            klient.secondName =dict["nazwisko"]
        if "nazwa" in dict.keys():
            klient.name =dict["nazwa"]
        if "telefon" in dict.keys():
            klient.telephone =dict["telefon"]
        if "NIP" in dict.keys():
            klient.vatId =dict["NIP"]
        if "adres" in dict.keys():
            klient.address =dict["adres"]
        if "nrK" in dict.keys():
            klient.clientNr =dict["nrK"]

        if(self.shopService.updateClient(klient)):
            self.klienciSheet.insert("","end",values=(klient.object_id,klient.firstName,klient.secondName,klient.clientNr,klient.name,klient.vatId,klient.telephone,klient.address))

        self.loadFullSheet()


    def delButtonListener(self):
        try:
            selectedId=self.klienciSheet.item(self.klienciSheet.selection()[0])["values"][0]
        except:
            return None
        self.shopService.removeClientById(selectedId)

        self.loadFullSheet()