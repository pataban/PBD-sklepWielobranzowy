from random import randint
from typing import Optional

from models.Article import Article
from models.ArticleInBill import ArticleInBill
from models.Bill import Bill
from models.BillDto import BillDto
from models.Client import Client
from models.ClientOnlyDto import ClientOnlyDto
from models.ClientWithBillsNumbersOnlyDto import ClientWithBillsNumbersOnlyDto
from models.Worker import Worker
from models.WorkerSafeDto import WorkerSafeDto
from repositories.ArticleRepository import ArticleRepository
from repositories.ClientRepository import ClientRepository
from repositories.WorkerRepository import WorkerRepository
from userInterface.DataFrame.RachunkiFrame import getTime


class ShopService:  # future facade for all operations on shop database

    def __init__(self,
                 articleRepository: ArticleRepository,
                 workerRepository: WorkerRepository,
                 clientRepository: ClientRepository):
        self._articleRepository = articleRepository
        self._workerRepository = workerRepository
        self._clientRepository = clientRepository
        self.__fetchActualNumbers()

    def __fetchActualNumbers(self):
        self._articleCode = self._articleRepository.maxArticleCode()
        #self._clientNr = self._clientRepository.maxClientNr()
        #self._workerNr = self._workerRepository.maxWorkerNr()
        #self._billNr = self._clientRepository.maxBillNr()


    # zwraca wszystkich pracowników BEZ loginów i haseł
    def findWorkers(self) -> [WorkerSafeDto]:
        return self._workerRepository.find()

    # jeśli nie znajdzie pracownika, zwraca None
    # jeśli znajdzie, zwraca pracownika BEZ loginu i hasła
    def findWorkerById(self, worker_id: str) -> Optional[WorkerSafeDto]:
        return self._workerRepository.findById(worker_id)

    # zwraca wszystkich klientów BEZ rachunków
    def findClients(self) -> [ClientOnlyDto]:
        return self._clientRepository.findClientOnlyDto()

    # zwraca None jeśli nie znajdzie
    # zwraca klienta bez rachunków jeśli znajdzie
    # alternatywna nazwa: findClientByNrK
    def findClientByClientNr(self, clientNr: int) -> Optional[ClientOnlyDto]:
        return self._clientRepository.findClientOnlyDtoByClientNr(clientNr)

    # zwraca None jeśli nie znajdzie
    # zwraca klienta bez rachunków jeśli znajdzie
    # alternatywna nazwa: findClientByNip
    def findClientByVatId(self, vatId: str) -> Optional[ClientOnlyDto]:
        return self._clientRepository.findClientOnlyDtoByVatId(vatId)

    # jeśli nie znajdzie clienta, zwraca None
    # jeśli znajdzie, zwraca klient w postaci klienta tylko z listą NUMERÓW rachunków
    def findClientById(self, client_id: str) -> Optional[ClientWithBillsNumbersOnlyDto]:
        return self._clientRepository.findByIdClientWithBillsNumbersOnlyDto(client_id)

    # tu najprościej, po prostu zwraca listę wszystkich artykułów :)
    def findArticle(self) -> [Article]:
        return self._articleRepository.find()

    # jeśli nie znajdzie artykułu, zwraca None
    # jeśli znajdzie, zwraca po prostu artykuł :)
    def findArticleById(self, article_id: str) -> Optional[Article]:
        return self._articleRepository.findById(article_id)

    # jeśli nie znajdzie artykułu, zwraca None
    # jeśli znajdzie, zwraca po prostu artykuł
    # z reguły pewnie wolniejsze niż po Id, bo pewnie mongo indeksuje tylko po id
    def findArticleByCode(self, article_code: int) -> Optional[Article]:
        return self._articleRepository.findByCode(article_code)

    # wszystkie rachunki w postaci rachunku bez listy produktów, z dodatkowym id klienta
    def findBills(self) -> [BillDto]:
        return self._clientRepository.findBillDto()

    # wstawia nowego pracownika
    # (wymagany pełny Worker z poprawnym nowym loginem i hasłem)
    # (wymagane puste id - zostanie automatycznie uzupelnione po skutecznym dodaniu do bazy)
    def insertWorker(self, newWorker: Worker) -> bool:
        return self._workerRepository.insert(newWorker)

    # wstawia nowego klienta
    # (MOŻE zawierać rachunki na liście, które MOGĄ już zawierać produkty!)
    # (wymagane puste id - zostanie automatycznie uzupelnione po skutecznym dodaniu do bazy)
    def insertClient(self, newClient: Client) -> bool:
        return self._clientRepository.insert(newClient)

    # wstawia nowy produkt
    # (wymagane puste id - zostanie automatycznie uzupelnione po skutecznym dodaniu do bazy)
    def insertArticle(self, newArticle: Article) -> bool:
        return self._articleRepository.insert(newArticle)

    # wstawia nowy rachunek do klienta o podanym id
    # (wymagany pełny Bill)
    def insertBill(self, client_id: str, newBill: Bill) -> bool:
        return self._clientRepository.addNewBill(client_id, newBill)

    # wstawia nowy produkt do rachunku o podanym numerze do klienta o podanym id
    # (wymagany pełny ArticleInBill)
    def insertArticleInBill(self, client_id: str, billNr: int, newArticleInBill: ArticleInBill) -> bool:
        return self._clientRepository.addNewArticleInBill(client_id, billNr, newArticleInBill)

    # aktualizuje pracownika
    # zazwyczaj z perspektywy listy pracowników, więc dto powinien już być przechowywany przez listę
    # lub zazwyczaj należy pobrać pracownika z bazy, zmodyfikować i podać go tutaj :)
    def updateWorker(self, updatedWorker: WorkerSafeDto) -> bool:
        return self._workerRepository.update(updatedWorker)

    # aktualizuje dane klienta
    # wymaga klienta w postaci dto - rachunki klienta aktualizujemy inną metodą
    # aktualizacja klienta raczej z perspektywy listy klientów, więc dto powinien już być przechowywany
    # na liście, po pobraniu przez findClients()
    def updateClient(self, updatedClient: ClientOnlyDto) -> bool:
        return self._clientRepository.update(updatedClient)

    # aktualizuje dane rachunku
    # wymaga rachunku w postaci dto - przedmioty na rachunku aktualizujemy inną metodą
    # wymaga id_clienta dla wydajności (inaczej, trzeba by było pobierać całą listę klientów)
    def updateBill(self, client_id, updatedBill: BillDto) -> bool:
        pass

    # aktualizuje artykuł
    # tu łatwo: albo artykuł z listy, albo artykuł świeżo pobrany pojedynczo z bazy
    def updateArticle(self, updatedArticle: Article) -> bool:
        return self._articleRepository.update(updatedArticle)

    # operacja usuwa pracownika
    # usuwa pracownika wraz z wszystkimi rachunkami, które wystawił
    def removeWorkerById(self, cascade: bool) -> bool:
        pass

    # usuwa klienta wraz z wszystkimi jego rachunkami
    def removeClientById(self, client_id: str) -> bool:
        return self._clientRepository.remove(client_id)

    # operacja usuwa artykuł
    # usuwa artykuł wraz z wszystkimi rachunkami, na których się znajduje
    def removeArticleById(self) -> bool:
        pass

    def generateNewKodTowaru(self):
        self._articleCode += 1
        return self._articleCode

    def generateNewNrK(self):
        self._clientNr += 1
        return self._clientNr

    def generateNewNrP(self):
        self._workerNr += 1
        return self._workerNr

    def generateNewNrR(self):
        self._billNr += 1
        return self._billNr

    # imitacja logowania
    # jeśli logowanie niepoprawne, zwraca None
    # jeśli logowanie poprawne zwraca pracownika w postaci okrojonej o dane do logowania
    def login(self, login, password) -> Optional[WorkerSafeDto]:    #TODO
        return WorkerSafeDto({"workerNr":111,"firstName":"aaa","secondName":"aaa","isSeller":True,"isManager":True,"isOwner":True,"_id":111})
        #return self._workerRepository.login(login, password)

    def chkTestUser(self):  # uzytkownik testowy
        if (self._workerRepository.login("aaa", "aaa") == None):
            worker = Worker(111, "aaa", "aaa", "aaa", "aaa", True, True, True)
            self._workerRepository.insert(worker)

    def printAll(self):
        print("towary:")
        tow = self._articleRepository.find()
        for t in tow:
            print(str(t))
        print("pracownicy:")
        pra = self._workerRepository.find()
        for p in pra:
            print(str(p))
        print("klienci:")
        """kli=self._clientRepository.find()
        for k in kli:
            print(str(k))"""

    def delAll(self):
        self._articleRepository._articles_handler.delete_many({})
        self._workerRepository._workers_handler.delete_many({})
        self._clientRepository._clients_handler.delete_many({})

    def getData(self, collection, atribute=None, value=None):  # old
        if (atribute == None and value == None):
            return self.db[collection].find({})
        if (value == None):
            return self.db[collection].find({atribute})
        return self.db[collection].find({atribute: value})

    def makeTestData(self):  # old
        for i in range(1, 10):
            prod = {
                'kod': randint(0, 1000000),
                'nazwa': "nazwa" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)),
                'cena': float(randint(0, 10000)) / 100
            }
            self.towary.insert_one(prod)
        for i in range(1, 10):
            prac = {
                'nrP': randint(0, 1000000),
                'imie': "imie" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)),
                'nazwisko': "nazwisko" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)),
                'login': "login" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)),
                'haslo': "haslo" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                    randint(0, 9)) + str(randint(0, 9)),
            }
            self.pracownicy.insert_one(prac)
        for i in range(1, 10):
            kli = None
            if (randint(0, 1) == 0):
                kli = {
                    'NIP': randint(0, 1000000),
                    'nazwa': "nazwa" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                        randint(0, 9)) + str(randint(0, 9)),
                    'rachunki': [{
                        'nrR': randint(0, 1000000),
                        'data': getTime(),
                        'nrP': randint(0, 1000000),
                        'towary': []
                    }]
                }
            else:
                kli = {
                    'imie': "imie" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                        randint(0, 9)) + str(randint(0, 9)),
                    'nazwisko': "nazwisko" + str(randint(0, 9)) + str(randint(0, 9)) + str(randint(0, 9)) + str(
                        randint(0, 9)) + str(randint(0, 9)),
                    'nrK': randint(0, 1000000),
                    'rachunki': [{
                        'nrR': randint(0, 1000000),
                        'data': getTime(),
                        'nrP': randint(0, 1000000),
                        'towary': []
                    }]
                }
            self.klienci.insert_one(kli)

