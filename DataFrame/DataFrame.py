import tkinter as tk
from tkinter import ttk
from DocEditFrame import DocEditFrame
class DataFrame(tk.Frame):
    def __init__(self,master,recomendedKeys):
        super().__init__(master)
        self.recomendedKeys=recomendedKeys
        menuRow1=tk.Frame(self)
        menuRow1.grid(row=0)

        self.backButton=tk.Button(menuRow1,text="Back")
        self.backButton.grid(row=0,column=0)

        self.newButton=tk.Button(menuRow1,text="New",command=self.newButtonListener)
        self.newButton.grid(row=0,column=1)
        
        self.editButton=tk.Button(menuRow1,text="Edit",command=self.editButtonListener)
        self.editButton.grid(row=0,column=2)
        
        self.delButton=tk.Button(menuRow1,text="Delete")
        self.delButton.grid(row=0,column=3)

        menuRow2=tk.Frame(self)
        menuRow2.grid(row=1)

        categoryLabel=tk.Label(menuRow2,text="Category:")
        categoryLabel.grid(row=0,column=0)
        self.categoryInput=tk.Entry(menuRow2)
        self.categoryInput.insert(0,"name")                           #test defoult data
        self.categoryInput.grid(row=0,column=1)
        
        valueLabel=tk.Label(menuRow2,text="Value:")
        valueLabel.grid(row=0,column=2)
        self.valueInput=tk.Entry(menuRow2)
        self.valueInput.insert(0,"chleb")                           #test defoult data
        self.valueInput.grid(row=0,column=3)

        self.searchButton=tk.Button(menuRow2,text="Search")
        self.searchButton.grid(row=0,column=4)

    def newButtonListener(self):
        self.itemEditFrame=DocEditFrame(self,"Dodawanie nowego elementu:",self.recomendedKeys)
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.createNewDocument(self.itemEditFrame.getItem())

    def editButtonListener(self):
        selected=self.towarySheet.item(self.towarySheet.selection()[0])["values"]
        ###################odczytaz z bazy element 


        self.itemEditFrame=DocEditFrame(self,"Edytowanie elementu:","""""""""""")
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.updateDocument(self.itemEditFrame.getItem())


    def delButtonListener(self):
        selected=self.towarySheet.item(self.towarySheet.selection()[0])["values"]
        ###################odczytaz z bazy element 

    def searchButtonListener(self):
         return


    def createNewDocument(self,dict):
        if dict==None:
            return
        if(not self.validateObligatoryKeys(dict)):
            return
        self.itemEditFrame.grid_forget()

    def updateDocument(self,dict):
        if dict==None:
            return
        if(not self.validateObligatoryKeys(dict)):
            return
        self.itemEditFrame.grid_forget()
        
    def validateObligatoryKeys(self,dict):
        return False