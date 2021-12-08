from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from models.Worker import Worker

class PracownicyFrame(DataFrame):
    def __init__(self,master,shopService):
        super().__init__(master,shopService)
        
        columns=("id","imie","nazwisko","nrP","sprzedawca","menager","wlasciciel")
        self.pracownicySheet=ttk.Treeview(self,column=columns,show="headings")
        self.pracownicySheet["displaycolumns"]=columns[1:]
        self.pracownicySheet.heading("imie", text="Imie")
        self.pracownicySheet.heading("nazwisko", text="Nazwisko")
        self.pracownicySheet.heading("nrP", text="NrP")
        self.pracownicySheet.heading("sprzedawca", text="Sprzedawca")
        self.pracownicySheet.heading("menager", text="Menager")
        self.pracownicySheet.heading("wlasciciel", text="Wlasciciel")
        self.pracownicySheet.grid(row=2)
        self.pracownicySheet.insert("","end",values=("id158631","testname","testsurname",147,"false","false","false"))    
                 #test data
        
        self.fillSheet(self.shopService.findWorkers())

    def fillSheet(self,workers):
        for w in workers:
            self.pracownicySheet.insert("","end",values=(w.id,w.firstName,w.secondName,w.nrP ,w.isSeller,w.isManager,w.isOwner))
        
    def getRecomendedKeys(self):
        keys={"nrP":0,"imie":"","nazwisko":"","login":"","haslo":""
            ,"isSprzedawca":"false","isMenager":"false","isWlasciciel":"false"}       ###TODO use generate nrP
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
        if not super().createNewDocument(dict):
            return False

        if(dict["isSprzedawca"]=="true"):
            dict["isSprzedawca"]=True
        else:
            dict["isSprzedawca"]=False

        if(dict["isMenager"]=="true"):
            dict["isMenager"]=True
        else:
            dict["isMenager"]=False

        if(dict["isWlasciciel"]=="true"):
            dict["isWlasciciel"]=True
        else:
            dict["isWlasciciel"]=False

        worker=Worker(dict["nrP"],dict["imie"],dict["nazwisko"],dict["login"],dict["haslo"],dict["isSprzedawca"],dict["isMenager"],dict["isWlasciciel"])
        if(self.shopService.insertWorker(worker)):
            self.pracownicySheet.insert("","end",values=(worker.id,worker.firstName,worker.secondName,worker.workerNr ,worker.isSeller,worker.isManager,worker.isOwner))

    def updateDocument(self,dict):  ###TODO
        super().updateDocument(dict)
        print(dict)


