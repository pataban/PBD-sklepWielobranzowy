import tkinter as tk
from userInterface.DocEditFrame import DocEditFrame
class DataFrame(tk.Frame):
    def __init__(self,master,shopService):
        super().__init__(master)
        self.shopService=shopService
        self.recomendedKeys=self.getRecomendedKeys()
        menuRow1=tk.Frame(self)
        menuRow1.grid(row=0)

        self.backButton=tk.Button(menuRow1,text="Back")
        self.backButton.grid(row=0,column=0)

        self.newButton=tk.Button(menuRow1,text="New",command=self.newButtonListener)
        self.newButton.grid(row=0,column=1)
        
        self.editButton=tk.Button(menuRow1,text="Edit",command=self.editButtonListener)
        self.editButton.grid(row=0,column=2)
        
        self.delButton=tk.Button(menuRow1,text="Delete",command=self.delButtonListener)
        self.delButton.grid(row=0,column=3)

        menuRow2=tk.Frame(self)
        menuRow2.grid(row=1)

        categoryLabel=tk.Label(menuRow2,text="Category:")
        categoryLabel.grid(row=0,column=0)
        self.categoryInput=tk.Entry(menuRow2)
        self.categoryInput.grid(row=0,column=1)
        
        valueLabel=tk.Label(menuRow2,text="Value:")
        valueLabel.grid(row=0,column=2)
        self.valueInput=tk.Entry(menuRow2)
        self.valueInput.grid(row=0,column=3)

        self.searchButton=tk.Button(menuRow2,text="Search",command=self.searchButtonListener)
        self.searchButton.grid(row=0,column=4)

    def loadFullSheet(self):
        pass

    def fillSheet(self,documents):
        pass

    def newButtonListener(self):
        self.itemEditFrame=DocEditFrame(self,"Dodawanie nowego elementu:",self.recomendedKeys)
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.createNewDocument(self.itemEditFrame.getItem())

    def editButtonListener(self):
        pass

    def delButtonListener(self):
        pass

    def searchButtonListener(self):
        pass


    def createNewDocument(self,dict):
        if dict==None:
            return False
        if(not self.validateObligatoryKeys(dict)):
            return False
        self.itemEditFrame.grid_forget()
        return True

    def updateDocument(self,dict):
        if dict==None:
            return False
        if(not self.validateObligatoryKeys(dict)):
            return False
        self.itemEditFrame.grid_forget()
        return True
        
    def validateObligatoryKeys(self,dict):
        for key in self.recomendedKeys.keys():
            if key in dict.keys() and (type(dict[key])!=type(self.recomendedKeys[key])):
                self.itemEditFrame.statusLabel["text"]="Error: obligatory/recomended field wrong type"
                return False
        return True
    
    def getRecomendedKeys(self):
        return {}