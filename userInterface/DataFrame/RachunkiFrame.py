from tkinter import ttk
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
        self.rachunkiSheet.heading("nrR", text="NrR")
        self.rachunkiSheet.heading("data", text="Data")
        self.rachunkiSheet.heading("nrP", text="NrP")
        self.rachunkiSheet.heading("metodaPlatnosci", text="etoda Platnosci")
        self.rachunkiSheet.heading("czyZaplacony", text="Czy Zaplacony")
        self.rachunkiSheet.grid(row=2)
        #self.rachunkiSheet.insert("","end",values=("123","dzisiejszaData",789))                   #test data
        
        self.fillSheet(self.shopService.findBills())

    def fillSheet(self,bills):
        for b in bills:
            self.rachunkiSheet.insert("","end",values=(b.client_id,b.billNr,b.dateTime,b.workerNr,b.paymentMethod,b.isAlreadyPaid))
        

    def getRecomendedKeys(self):
        keys={"nrR":0,"nrK":0,"NIP":"","data":getTime(),"metodaPlatnosci":"gotowka","zaplacony":"false"}    #ustawic dobry nrR
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
        articles=self.artykulyFrame.getList()
        if articles==None:
            return False
        tmp=dict["data"]
        tmp=tmp.split(" ")
        tmp[0]=tmp[0].split(".")
        tmp[1]=tmp[1].split(":")
        print(tmp)
        dict["data"]=datetime.datetime(int(tmp[0][2]),int(tmp[0][1]),int(tmp[0][0]),int(tmp[1][0]),int(tmp[1][1]),int(tmp[1][2]))
        
        if(dict["metodaPlatnosci"]=="gotowka"):
            dict["metodaPlatnosci"]=PaymentMethod.CASH
        elif(dict["metodaPlatnosci"]=="przelew"):
            dict["metodaPlatnosci"]=PaymentMethod.BANK_TRANSFER
        else:
            dict["metodaPlatnosci"]=None

        if(dict["zaplacony"]=="true"):
            dict["zaplacony"]=True
        else:
            dict["zaplacony"]=False

        clientId=""
        clients=self.shopService.findClients()
        if "nrK" in dict:
            for c in clients:
                if c.clientNr==dict["nrK"]:
                    clientId=c.object_id
        else:
            for c in clients:
                if c.vatId==dict["NIP"]:
                    clientId=c.object_id

        bill=Bill(dict["nrR"],self.user,dict["metodaPlatnosci"],articles,dict["zaplacony"],dict["data"])
        if(self.shopService.insertBill(clientId,bill)):
            self.rachunkiSheet.insert("","end",values=(clientId,bill.billNr,bill.dateTime,self.user.nrP,bill.paymentMethod,bill.isAlreadyPaid))        #sprawdzic dodawanie i wczytywanie



    def updateDocument(self,dict):      #TODO
        super().updateDocument(dict)
        print(dict)


    def newButtonListener(self):
        super().newButtonListener()
        self.artykulyFrame=TowaryWRachunkuFrame(self,self.shopService)
        self.artykulyFrame.grid(row=6)


