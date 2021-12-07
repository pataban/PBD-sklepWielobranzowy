from models.Worker import Worker

class ShopService:  # future facade for all operations on shop database
    def __init__(self, articleRepository, workerRepository, clientRepository):
        self._articleRepository = articleRepository
        self._workerRepository = workerRepository
        self._clientRepository = clientRepository

    def chkTestUser(self):          #uzytkownik testowy
        if(self._workerRepository.login("aaa","aaa")==None):
            worker=Worker(111,"aaa","aaa","aaa","aaa",True,True,True)
            self._workerRepository.insert(worker)
        
    def login(self,login,password):
        return self._workerRepository.login(login,password)

    def printAll(self):
        print("towary:")
        tow=self._articleRepository.find()
        for t in tow:
            print(t)
        print("pracownicy:")
        pra=self._workerRepository.find()
        for p in pra:
            print(p)
        print("klienci:")
        """kli=self._clientRepository.find()
        for k in kli:
            print(k)"""

    def delAll(self):
        self._articleRepository._articles_handler.delete_many({})
        self._workerRepository._workers_handler.delete_many({})
        self._clientRepository._clients_handler.delete_many({})
    
    





    def getData(self,collection,atribute=None,value=None):  #old
        if(atribute==None and value==None):
            return self.db[collection].find({})
        if(value==None):
            return self.db[collection].find({atribute})
        return self.db[collection].find({atribute:value})

    def makeTestData(self):     #old
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

    

    # there will be many, many operations available...
