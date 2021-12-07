from models.Bill import Bill
from models.BillWithArticlesNamesDto import BillWithArticlesNamesDto
from models.ClientOnlyDto import ClientOnlyDto
from models.ClientWithBillsNumbersOnlyDto import ClientWithBillsNumbersOnlyDto
from models.Client import Client


class ClientRepository:
    def __init__(self, clientsMongoHandler):
        self._clients_handler = clientsMongoHandler

    def findClientOnlyDto(self) -> [ClientOnlyDto]:  # wszyscy klienci bez rachunków
        pass

    def findByIdClientWithBillsNumbersOnlyDto(
            self) -> ClientWithBillsNumbersOnlyDto:  # jeden klient tylko z listą numerów rachunków
        pass

    def findBillDto(self) -> [
        BillWithArticlesNamesDto]:  # wszystkie rachunki w postaci rachunku z artykułami z samymi nazwami
        pass

    def findBillByNumber(self) -> Bill:  # jeden rachunek z wszystkimi artykułami (podpięte obiekty artykułów)
        pass

    def insert(self, newClient: Client) -> bool:
        if newClient is None:
            raise TypeError('Argument newClient cannot be None')
        if not isinstance(newClient, Client):
            raise TypeError('Argument newClient must by of type Client')
        if newClient.object_id is not None:
            raise ValueError('New article cannot have assigned id')
        insert_one_result = self._clients_handler.insert_one(newClient.toMongoDictionary())
        inserted_id = insert_one_result.inserted_id
        if inserted_id is None:
            return False
        newClient.object_id = str(inserted_id)
        return True
