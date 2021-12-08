import tkinter as tk
from decimal import Decimal
from userInterface.DocEditFrame import DocEditFrame
from models.ArticleInBill import ArticleInBill

class TowaryWRachunkuFrame(tk.Frame):
    def __init__(self,master,shopService):
        super().__init__(master)
        self.shopService=shopService
        titleLabel=tk.Label(self,text="artykuly")
        titleLabel.grid(row=0)

        self.docFrame=tk.Frame(self)
        self.docFrame.grid(row=1)
        self.fields=[]
        self.addField()

        self.addFieldButton=tk.Button(self,text="dodaj pole",command=self.addField)
        self.addFieldButton.grid(row=2)

        self.statusLabel=tk.Label(self,text="")
        self.statusLabel.grid(row=3)

    def addField(self):
        kodEntry=tk.Entry(self.docFrame)
        iloscEntry=tk.Entry(self.docFrame)
        cenaEntry=tk.Entry(self.docFrame)

        row=0
        if len(self.fields)>0:
            row=self.fields[-1][-1]+1
        kodEntry.grid(row=row,column=0)
        iloscEntry.grid(row=row,column=1)
        cenaEntry.grid(row=row,column=2)
        
        delButton=tk.Button(self.docFrame,text="del")
        delButton.grid(row=row,column=3)

        field=(kodEntry,iloscEntry,cenaEntry,delButton,row)
        self.fields.append(field)

        delButton["command"]=lambda:self.removeField(field)

    def removeField(self,field):
        field[0].grid_forget()
        field[1].grid_forget()
        field[2].grid_forget()
        field[3].grid_forget()
        self.fields.remove(field)
        self.update()

    def getList(self):
        articleList=[]
        for field in self.fields:
            kod=field[0].get()
            ilosc=field[1].get()
            cena=field[2].get()

            if(kod==""):
                self.statusLabel["text"]="Error: Missing kodE"
                return None
            if(ilosc==""):
                self.statusLabel["text"]="Error: Missing ilosc"
                return None
            if(cena==""):
                self.statusLabel["text"]="Error: Missing cena"
                return None
            
            try:
                kod=int(kod)
            except:
                self.statusLabel["text"]="Error: Wrong data type Expected int"
                return None
            if "." in ilosc:
                try:
                    ilosc=Decimal(ilosc)
                except:
                    self.statusLabel["text"]="Error: Wrong data type Expected Decimal"
                    return None
            else:
                try:
                    ilosc=int(ilosc)
                except :
                    self.statusLabel["text"]="Error: Wrong data type. Expected int"
                    return None
            try:
                cena=Decimal(cena)
            except:
                self.statusLabel["text"]="Error: Wrong data type Expected Decimal"
                return None

            article=self.shopService.findArticleByCode(kod)
            if article==None:
                self.statusLabel["text"]="Error: Wrong article in row "+str(field[-1])
                return None
            articleInBill=ArticleInBill(article,ilosc,cena)
            articleList.append(articleInBill)
        if len(articleList)==0:
            self.statusLabel["text"]="Error: No articles provided"
            return None
        return articleList


