from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from models.Client import Client

class KlienciFrame(DataFrame):
    def __init__(self,master,shopService):
        super().__init__(master,shopService)
        
        columns=("id","imie","nazwisko","nrK","nazwa","NIP","tel","adres")
        self.klienciSheet=ttk.Treeview(self,column=columns,show="headings")
        self.klienciSheet["displaycolumns"]=columns[1:]
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

        self.fillSheet(self.shopService.findClients())

    def fillSheet(self,clients):
        for c in clients:
            self.klienciSheet.insert("","end",values=(c.object_id,c.firstName,c.secondName,c.clientNr,c.name,c.vatId,c.telephone,c.address))
        
        
    def getRecomendedKeys(self):
        keys={"imie":"","nazwisko":"","nrK":0,"nazwa":"","NIP":"","tel":"","adres":""}   #ustawic dobry nrK
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

    def updateDocument(self,dict):  ###TODO
        super().updateDocument(dict)
        print(dict)


