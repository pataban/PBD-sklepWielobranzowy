from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame

class PracownicyFrame(DataFrame):
    def __init__(self,master,shopService):
        super().__init__(master,shopService)
        
        columns=("id","imie","nazwisko","nrP","login","haslo")
        self.pracownicySheet=ttk.Treeview(self,column=columns,show="headings")
        self.pracownicySheet["displaycolumns"]=columns[1:]
        self.pracownicySheet.heading("imie", text="Imie")
        self.pracownicySheet.heading("nazwisko", text="Nazwisko")
        self.pracownicySheet.heading("nrP", text="NrP")
        self.pracownicySheet.heading("login", text="Login")
        self.pracownicySheet.heading("haslo", text="Haslo")
        self.pracownicySheet.grid(row=2)
        self.pracownicySheet.insert("","end",values=("id158631","testname","testsurname",147,"testLogin","testPass"))    
                 #test data
        
        """pracownicy=self.data.getData("pracownicy")
        for p in pracownicy:
            print(p)
            values=(p["imie"],p["nazwisko"],p["nrP"],p["login"],p["haslo"])
            self.pracownicySheet.insert("","end",values=values)"""
        
    def getRecomendedKeys(self):
        keys={"nrP":0,"imie":"","nazwisko":"","login":"","haslo":""
            ,"isSprzedawca":"false","isMenager":"false","isWlasciciel":"false"}       #ustawic dobry nrP
        return keys

    def validateObligatoryKeys(self,dict):
        if not super().validateObligatoryKeys(dict):
            return False
        for key in self.recomendedKeys.keys():
            if not key in dict.keys():
                self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
                return False
        return True

    def createNewDocument(self,dict):
        super().createNewDocument(dict)
        print(dict)

    def updateDocument(self,dict):
        super().updateDocument(dict)
        print(dict)


