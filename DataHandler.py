import pymongo
from pymongo import MongoClient
import random
from random import randint
import datetime

def getTime():
    return datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
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
        

    def getData(self,collection,atribute=None,value=None):
        if(atribute==None and value==None):
            return self.db[collection].find({})
        if(value==None):
            return self.db[collection].find({atribute})
        return self.db[collection].find({atribute:value})

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
                'kod': randint(0,1000000),
                'nazwa': "nazwa"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                'cena': float(randint(0,10000))/100
            }
            self.towary.insert_one(prod)
        for i in range(1,10):
            prac={
                'nrP': randint(0,1000000),
                'imie': "imie"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                'nazwisko': "nazwisko"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                'login': "login"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                'haslo': "haslo"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
            }
            self.pracownicy.insert_one(prac)
        for i in range(1,10):
            kli=None
            if(randint(0,1)==0):
                kli={
                    'NIP': randint(0,1000000),
                    'nazwa': "nazwa"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                    'rachunki':[{
                        'nrR':randint(0,1000000),
                        'data':getTime(),
                        'nrP':randint(0,1000000),
                        'towary':[]
                    }] 
                }
            else:
                kli={
                    'imie': "imie"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                    'nazwisko': "nazwisko"+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9))+str(randint(0,9)),
                    'nrK': randint(0,1000000),
                    'rachunki':[{
                        'nrR':randint(0,1000000),
                        'data':getTime(),
                        'nrP':randint(0,1000000),
                        'towary':[]
                    }] 
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
    #data.makeTestData()

    #data.towary.delete_many({})
    #data.pracownicy.delete_many({})
    #data.klienci.delete_many({})

    data.printAll()
