from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from models.Worker import Worker
from models.WorkerSafeDto import WorkerSafeDto
from userInterface.DocEditFrame import DocEditFrame

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
        
        self.loadFullSheet()

    def loadFullSheet(self):
        self.pracownicySheet.delete(*self.pracownicySheet.get_children())
        self.fillSheet(self.shopService.findWorkers())

    def fillSheet(self,workers):
        for w in workers:
            self.pracownicySheet.insert("","end",values=(w.id,w.firstName,w.secondName,w.nrP ,w.isSeller,w.isManager,w.isOwner))
        
    def getRecomendedKeys(self):
        keys={"nrP":self.shopService.generateNewNrP(),"imie":"","nazwisko":"","login":"","haslo":""
            ,"isSprzedawca":"false","isMenager":"false","isWlasciciel":"false"}
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

    
    def editButtonListener(self):
        try:
            selectedId=self.pracownicySheet.item(self.pracownicySheet.selection()[0])["values"][0]
        except:
            return
        
        worker=self.shopService.findWorkerById(selectedId)
        keys={"nrP":worker.nrP,"imie":worker.firstName,"nazwisko":worker.secondName,"login":"","haslo":""
            ,"isSprzedawca":str(worker.isSeller),"isMenager":str(worker.isManager),"isWlasciciel":str(worker.isOwner),"id":selectedId}

        self.itemEditFrame=DocEditFrame(self,"Edytowanie elementu:",keys)
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.updateDocument(self.itemEditFrame.getItem())


    def updateDocument(self,dict):
        if not super().updateDocument(dict):
            return False
        print("hdfghshsdg")
        if(dict["isSprzedawca"]=="true" or dict["isSprzedawca"]=="True"):
            dict["isSprzedawca"]=True
        else:
            dict["isSprzedawca"]=False

        if(dict["isMenager"]=="true"or dict["isMenager"]=="True"):
            dict["isMenager"]=True
        else:
            dict["isMenager"]=False

        if(dict["isWlasciciel"]=="true"or dict["isWlasciciel"]=="True"):
            dict["isWlasciciel"]=True
        else:
            dict["isWlasciciel"]=False

        worker=self.shopService.findWorkerById(dict["id"])
        worker.nrP=dict["nrP"]
        worker.firstName =dict["imie"]
        worker.secondName =dict["nazwisko"]
        worker.isSeller =dict["isSprzedawca"]
        worker.isManager =dict["isMenager"]
        worker.isOwner =dict["isWlasciciel"]


        if(self.shopService.updateWorker(worker)):
            self.pracownicySheet.insert("","end",values=(worker.id,worker.firstName,worker.secondName,worker.nrP ,worker.isSeller,worker.isManager,worker.isOwner))

        self.loadFullSheet()


