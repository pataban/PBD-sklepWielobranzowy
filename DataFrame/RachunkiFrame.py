import tkinter as tk
from tkinter import ttk
from DataFrame.DataFrame import DataFrame
import datetime

def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class RachunkiFrame(DataFrame):
    def __init__(self,master):
        super().__init__(master)
        
        columns=("nrR","data","nrP")
        self.rachunkiSheet=ttk.Treeview(self,column=columns,show="headings")
        self.rachunkiSheet.heading("nrR", text="NrR")
        self.rachunkiSheet.heading("data", text="Data")
        self.rachunkiSheet.heading("nrP", text="NrP")
        self.rachunkiSheet.grid(row=2)
        self.rachunkiSheet.insert("","end",values=("123","dzisiejszaData",789))                   #test data
        
        
    def getRecomendedKeys(self):
        keys={"nrR":0,"data":getTime(),"nrP":0,"sposPlatnosci":"gotowka","zaplacony":"false"}    #ustawic dobry nrR
        return keys

    def validateObligatoryKeys(self,dict):
        for key in self.recomendedKeys.keys():
            if not key in dict.keys():
                self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
                return False
        return True

    def createNewDocument(self,dict):
        super().createNewDocument(dict)
        tmp=dict["data"]
        tmp=tmp.split(" ")
        tmp[0]=tmp[0].split(".")
        tmp[1]=tmp[1].split(":")
        print(tmp)
        dict["data"]=datetime.datetime(int(tmp[0][2]),int(tmp[0][1]),int(tmp[0][0]),int(tmp[1][0]),int(tmp[1][1]),int(tmp[1][2]))
        print(dict)

    def updateDocument(self,dict):
        super().updateDocument(dict)
        print(dict)


