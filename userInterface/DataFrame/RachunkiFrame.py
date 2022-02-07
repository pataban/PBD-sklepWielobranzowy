import tkinter as tk
from tkinter import ttk

from models.NewBillDto import NewBillDto
from userInterface.DataFrame.DataFrame import DataFrame
import datetime
from models.Bill import Bill
from models.PaymentMethod import PaymentMethod
from userInterface.TowaryWRachunkuFrame import TowaryWRachunkuFrame

def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")

class RachunkiFrame(DataFrame):
    def __init__(self,master,shopService,user):
        super().__init__(master,shopService)
        self.user=user

        columns=("clientId","nrR","data","nrP","metodaPlatnosci","czyZaplacony")
        self.rachunkiSheet=ttk.Treeview(self,column=columns,show="headings")
        self.rachunkiSheet["displaycolumns"]=columns[1:]
        self.rachunkiSheet.column("nrR", width=150,anchor=tk.E)
        self.rachunkiSheet.column("data", width=150,anchor=tk.W)
        self.rachunkiSheet.column("nrP", width=100,anchor=tk.E)
        self.rachunkiSheet.column("metodaPlatnosci", width=200,anchor=tk.W)
        self.rachunkiSheet.column("czyZaplacony", width=100,anchor=tk.W)
        self.rachunkiSheet.heading("nrR", text="NrR")
        self.rachunkiSheet.heading("data", text="Data")
        self.rachunkiSheet.heading("nrP", text="NrP")
        self.rachunkiSheet.heading("metodaPlatnosci", text="Metoda platnosci")
        self.rachunkiSheet.heading("czyZaplacony", text="Czy zaplacony")
        self.rachunkiSheet.grid(row=2)
        
        self.fillSheet(self.shopService.findBills())

    def fillSheet(self,bills):
        for b in bills:
            metoda_platnosci_slownie = "Brak danych"
            if b.paymentMethod == PaymentMethod.CASH:
                metoda_platnosci_slownie = "gotówka"
            elif b.paymentMethod == PaymentMethod.BANK_TRANSFER:
                metoda_platnosci_slownie = "przelew"
            self.rachunkiSheet.insert("","end", values=(b.client_id, b.billNr, b.dateTime, b.worker_id, metoda_platnosci_slownie, b.isAlreadyPaid))
        

    def getRecomendedKeys(self):
        keys={"nrR":self.shopService.generateNewNrR(),"nrK":0,"NIP":"","data":getTime(),"metodaPlatnosci":"gotowka","zaplacony":"false"}
        return keys

    def validateObligatoryKeys(self,dict):
        for key in self.recomendedKeys.keys():
            if (key!="nrK") and (key!="NIP") and (not key in dict.keys()):
                self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
                return False
        if(not "nrK" in dict) and (not "NIP" in dict):
            self.itemEditFrame.statusLabel["text"]="Error: missing obligatory fields"
            return False
        return True

    def createNewDocument(self,dict):                   #sprawdzic czy dziala z artykulami
        if not super().createNewDocument(dict):
            return False
        articleInBillsDtos=self.artykulyFrame.getArticleInBillDtos()
        if articleInBillsDtos==None:
            return False
        self.artykulyFrame.grid_forget()
        tmp=dict["data"]
        tmp=tmp.split(" ")
        tmp[0]=tmp[0].split(".")
        tmp[1]=tmp[1].split(":")
        print(tmp)
        dict["data"]=datetime.datetime(int(tmp[0][2]),int(tmp[0][1]),int(tmp[0][0]),int(tmp[1][0]),int(tmp[1][1]),int(tmp[1][2]))

        metoda_platnosci_enum = None
        if(dict["metodaPlatnosci"]=="gotowka"):
            metoda_platnosci_enum=PaymentMethod.CASH
        elif(dict["metodaPlatnosci"]=="przelew"):
            metoda_platnosci_enum=PaymentMethod.BANK_TRANSFER
        else:
            metoda_platnosci_enum=None

        if(dict["zaplacony"]=="true"):
            dict["zaplacony"]=True
        else:
            dict["zaplacony"]=False

        client_number = None
        clients=self.shopService.findClients()
        try:
            if "nrK" in dict:
                for c in clients:
                    if c.clientNr==dict["nrK"]:
                        client_number=c.clientNr
            else:
                for c in clients:
                    if c.vatId==dict["NIP"]:
                        client_number=c.clientNr
        except:
            pass
        if client_number is None:
            return False

        newBillDtos=NewBillDto(
            self.user.nrP,
            metoda_platnosci_enum,
            dict["zaplacony"],
            dict["data"],
            client_number
        )

        inserted_bill_number = self.shopService.insertBill(newBillDtos, articleInBillsDtos)
        if inserted_bill_number is not None:
            self.rachunkiSheet.insert("", "end", values=(
                dict["nrK"],
                inserted_bill_number,
                dict["data"],
                self.user.nrP,
                dict["metodaPlatnosci"],
                dict["zaplacony"]
            ))


    def updateDocument(self,dict):      #TODO
        super().updateDocument(dict)
        print(dict)


    def newButtonListener(self):
        super().newButtonListener()
        self.artykulyFrame=TowaryWRachunkuFrame(self,self.shopService)
        self.artykulyFrame.grid(row=6)


