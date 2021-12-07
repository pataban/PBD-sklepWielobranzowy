import tkinter as tk
from tkinter import ttk
from DocEditFrame import DocEditFrame
from DataFrame.DataFrame import DataFrame

class RachunkiFrame(DataFrame):
    def __init__(self,master):
        super().__init__(master,recomendedKeys={"kod":0,"nazwa":"","cena":12.5})
        
        columns=("nrR","data","nrP")
        self.rachunkiSheet=ttk.Treeview(self,column=columns,show="headings")
        self.rachunkiSheet.heading("nrR", text="NrR")
        self.rachunkiSheet.heading("data", text="Data")
        self.rachunkiSheet.heading("nrP", text="NrP")
        self.rachunkiSheet.grid(row=2)
        self.rachunkiSheet.insert("","end",values=("123","dzisiejszaData",789))                   #test data
        
        
    def validateObligatoryKeys(self,dict):
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


