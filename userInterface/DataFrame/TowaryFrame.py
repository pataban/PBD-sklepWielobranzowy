from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from decimal import Decimal

class TowaryFrame(DataFrame):
    def __init__(self,master):
        super().__init__(master)
        
        columns=("id","nazwa","kod","cena")
        self.towarySheet=ttk.Treeview(self,column=columns,show="headings")
        self.towarySheet["displaycolumns"]=columns[1:]
        self.towarySheet.heading("nazwa", text="Nazwa")
        self.towarySheet.heading("kod", text="Kod")
        self.towarySheet.heading("cena", text="Cena")
        self.towarySheet.grid(row=2)
        self.towarySheet.insert("","end",values=("468844","testname",123,12.56))                   #test data

        """towary=self.data.getData("towary")                                                  
        for t in towary:
            self.towarySheet.insert("","end",values=(t["nazwa"],t["kod"],t["cena"]))"""
        
    def getRecomendedKeys(self):
        keys={"kod":0,"nazwa":"","cena":Decimal("0.00")}       #ustawic dobry kod
        return keys

    def validateObligatoryKeys(self,dict):
        if not super().validateObligatoryKeys(dict):
            return False
        for key in self.recomendedKeys.keys():
            if not key in dict.keys():
                self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
                return False
        return True

    def createNewDocument(self,dict):       #TODO
        super().createNewDocument(dict)
        print(dict)

    def updateDocument(self,dict):
        super().updateDocument(dict)
        print(dict)


