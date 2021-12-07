from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame

class KlienciFrame(DataFrame):
    def __init__(self,master):
        super().__init__(master)
        
        columns=("id","imie","nazwisko","nrK","nazwa","NIP")
        self.klienciSheet=ttk.Treeview(self,column=columns,show="headings")
        self.klienciSheet["displaycolumns"]=columns[1:]
        self.klienciSheet.heading("imie", text="Imie")
        self.klienciSheet.heading("nazwisko", text="Nazwisko")
        self.klienciSheet.heading("nrK", text="NrK")
        self.klienciSheet.heading("nazwa", text="Nazwa")
        self.klienciSheet.heading("NIP", text="NIP")
        self.klienciSheet.grid(row=2)
        self.klienciSheet.insert("","end",values=("id4456","testname","testsurname",456))              #test data
        self.klienciSheet.insert("","end",values=("id87964","","","","testname","12345678"))            #test data
        
        """klienci=self.data.getData("klienci")
        for k in klienci:
            values=None
            if("NIP" in k.keys()):
                values=("","","",k["nazwa"],k["NIP"])
            else:
                values=(k["imie"],k["nazwisko"],k["nrK"],"","")
            self.klienciSheet.insert("","end",values=values)"""
        
    def getRecomendedKeys(self):
        keys={"imie":"","nazwisko":"","nrK":0,"nazwa":"","NIP":0}   #ustawic dobry nrK
        return keys
        
    def validateObligatoryKeys(self,dict):
        if not super().validateObligatoryKeys(dict):
            return False
        if (not "nrK" in dict) and (not "NIP" in dict):
            self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
            return False
        return True

    def createNewDocument(self,dict):
        super().createNewDocument(dict)
        print(dict)

    def updateDocument(self,dict):
        super().updateDocument(dict)
        print(dict)


