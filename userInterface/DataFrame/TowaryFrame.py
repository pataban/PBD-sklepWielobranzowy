from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from decimal import Decimal
from models.Article import Article

class TowaryFrame(DataFrame):
    def __init__(self,master,shopService):
        super().__init__(master,shopService)
        
        columns=("id","nazwa","kod","cena")
        self.towarySheet=ttk.Treeview(self,column=columns,show="headings")
        self.towarySheet["displaycolumns"]=columns[1:]
        self.towarySheet.heading("nazwa", text="Nazwa")
        self.towarySheet.heading("kod", text="Kod")
        self.towarySheet.heading("cena", text="Cena")
        self.towarySheet.grid(row=2)
        self.towarySheet.insert("","end",values=("468844","testname",123,12.56))                   #test data

        self.fillSheet(self.shopService.findArticle())
        
    def fillSheet(self,articles):
        for a in articles:
            self.towarySheet.insert("","end",values=(a.id,a.name,a.code,a.actualPrice))

    def getRecomendedKeys(self):
        keys={"kod":0,"nazwa":"","cena":Decimal("0.00")}       ###TODO use GenerateKod
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
        article=Article(dict["kod"],dict["nazwa"],dict["cena"])
        if(self.shopService.insertArticle(article)):
            self.towarySheet.insert("","end",values=(article.id,article.name,article.code,article.actualPrice))

    def updateDocument(self,dict):       #TODO
        super().updateDocument(dict)
        print(dict)


