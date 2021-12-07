import tkinter as tk
from decimal import Decimal


class DocEditFrame(tk.Frame):
    def __init__(self,master, title,doc):
        super().__init__(master)
        titleLabel=tk.Label(self,text=title)
        titleLabel.grid(row=0)

        self.docFrame=tk.Frame(self)
        self.docFrame.grid(row=1)
        self.fields=[]
        for key in doc.keys():
            self.addField(key,doc[key])

        self.addFieldButton=tk.Button(self,text="dodaj pole",command=self.addField)
        self.addFieldButton.grid(row=2)

        self.confirmButton=tk.Button(self,text="potwierdz")
        self.confirmButton.grid(row=3)

        self.statusLabel=tk.Label(self,text="")
        self.statusLabel.grid(row=4)

    def addField(self,labelText=None,value=None):
        label=tk.Entry(self.docFrame)
        if labelText is not None:
            label.insert(0,str(labelText))
        typeEntry=tk.Entry(self.docFrame)
        if typeEntry is not None:
            if(isinstance(value,int)):
                typeEntry.insert(0,"int")
            if(isinstance(value,str)):
                typeEntry.insert(0,"str")
            if(isinstance(value,float)):
                typeEntry.insert(0,"float")
            if(isinstance(value,Decimal)):
                typeEntry.insert(0,"Decimal")
        entry=tk.Entry(self.docFrame)
        if value is not None:
            entry.insert(0,str(value))

        row=0
        if len(self.fields)>0:
            row=self.fields[-1][-1]+1
        label.grid(row=row,column=0)
        typeEntry.grid(row=row,column=1)
        entry.grid(row=row,column=2)
        
        delButton=tk.Button(self.docFrame,text="del")
        delButton.grid(row=row,column=3)

        field=(label,typeEntry,entry,delButton,row)
        self.fields.append(field)

        delButton["command"]=lambda:self.removeField(field)

    def removeField(self,field):
        field[0].grid_forget()
        field[1].grid_forget()
        field[2].grid_forget()
        field[3].grid_forget()
        self.fields.remove(field)
        self.update()

    def getItem(self):
        dict={}
        for field in self.fields:
            label=field[0].get()
            type=field[1].get()
            value=field[2].get()

            if(label==""):
                self.statusLabel["text"]="Error: Missing label"
                return None
            if(label in dict):
                self.statusLabel["text"]="Error: Repeating labels"
                return None
            
            if(type=="int"):
                try:
                    value=int(value)
                except :
                    self.statusLabel["text"]="Error: Wrong data type"
                    return None
            elif(type=="float"):
                try:
                    value=float(value)
                except:
                    self.statusLabel["text"]="Error: Wrong data type"
                    return None
            elif(type=="Decimal"):
                try:
                    value=Decimal(value)
                except:
                    self.statusLabel["text"]="Error: Wrong data type"
                    return None
            elif(type!="float") and (type!="int") and (type!="str")and (type!="Decimal"): 
                self.statusLabel["text"]="Error: Wrong data type"
                return None

            dict[label]=value
        return dict

