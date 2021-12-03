import pymongo
from pymongo import MongoClient
import random

#rename na DataHandler

class DataHandler:
    def __init__(self):
        self.client=MongoClient("mongodb://localhost:27017")    
            #mongodb://myDBReader:D1fficultP%40ssw0rd@DBAddress:27017/?authSource=admin
        self.db=self.client["sklepWielobranzowy"]
        self.towary=self.db["towary"]
        self.pracownicy=self.db["pracownicy"]
        self.klienci=self.db["klienci"]

        if(self.pracownicy.find_one({'login':"aaa"})==None):
            self.pracownicy.insert_one({'login':"aaa",'haslo':"aaa"})           #uzytkownik testowy
        #self.makeTestData()
        #self.towary.delete_many({})
        #self.pracownicy.delete_many({})
        #self.klienci.delete_many({})
        self.printAll()

    def login(self,login,password):
        user=self.pracownicy.find_one({'login':login})
        if (user==None):
            return False
        if(user["haslo"]==password):
            return True
        return False

    def makeTestData(self):
        for i in range(1,10):
            prod={
                'kod': random.randint(0,1000000),
                'nazwa': "nazwa"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
                'cena': float(random.randint(0,10000))/100
            }
            self.towary.insert_one(prod)
        for i in range(1,10):
            prac={
                'nrP': random.randint(0,1000000),
                'imie': "imie"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
                'nazwisko': "nazwisko"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
                'login': "login"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
                'haslo': "haslo"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
            }
            self.pracownicy.insert_one(prac)
        for i in range(1,10):
            kli={
                'NIP': random.randint(0,1000000),
                'nazwa': "nazwa"+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26))+str(random.randint(65,65+26)),
                'rachunki':[{}] 
            }
            self.klienci.insert_one(kli)

    def printAll(self):
        print("towary:")
        tow=self.towary.find({})
        for t in tow:
            print(t)
        print("pracownicy:")
        pra=self.pracownicy.find({})
        for p in pra:
            print(p)
        print("klienci:")
        kli=self.klienci.find({})
        for k in kli:
            print(k)



if __name__=="__main__":
    input("confirm data creation (enter)")
    data=DataHandler()
