import tkinter as tk

class DataFrame(tk.Frame):
    def __init__(self,master):
        super().__init__(master)
        menuRow1=tk.Frame(self)
        menuRow1.grid(row=0)

        self.backButton=tk.Button(menuRow1,text="Back")
        self.backButton.grid(row=0,column=0)

        self.newButton=tk.Button(menuRow1,text="New")
        self.newButton.grid(row=0,column=1)
        
        self.editButton=tk.Button(menuRow1,text="Edit")
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

        self.dataListbox=tk.Listbox(self, width=50,selectmode="single")
        self.dataListbox.insert(1,"test ")                        #test
        self.dataListbox.grid(row=2)
