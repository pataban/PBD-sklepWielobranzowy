from tkinter import ttk
from userInterface.DataFrame.DataFrame import DataFrame
from decimal import Decimal
from models.Article import Article
from userInterface.DocEditFrame import DocEditFrame

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

        self.loadFullSheet()

    def loadFullSheet(self):
        self.towarySheet.delete(*self.towarySheet.get_children())
        self.fillSheet(self.shopService.findArticle())        

    def fillSheet(self,articles):
        for a in articles:
            self.towarySheet.insert("","end",values=(a.id,a.name,a.code,a.actualPrice))

    def getRecomendedKeys(self):
        keys={"kod":self.shopService.generateNewKodTowaru(),"nazwa":"","cena":Decimal("0.00")}
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

    def editButtonListener(self):
        try:
            selectedId=self.towarySheet.item(self.towarySheet.selection()[0])["values"][0]
        except:
            return
        
        article=self.shopService.findArticleById(selectedId)

        self.itemEditFrame=DocEditFrame(self,"Edytowanie elementu:",{"kod":article.code,"nazwa":article.name,"cena":article.actualPrice,"id":selectedId})
        self.itemEditFrame.grid(row=5)
        self.itemEditFrame.confirmButton["command"]=lambda:self.updateDocument(self.itemEditFrame.getItem())


    def updateDocument(self,dict):
        if not super().updateDocument(dict):
            return False
        article=Article(dict["kod"],dict["nazwa"],dict["cena"],dict["id"])
        if(self.shopService.updateArticle(article)):
            self.towarySheet.insert("","end",values=(article.id,article.name,article.code,article.actualPrice))

        self.loadFullSheet()


