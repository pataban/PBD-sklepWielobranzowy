from typing import Optional

from bson import ObjectId

from models.Bill import Bill
from models.BillDto import BillDto
from models.ClientOnlyDto import ClientOnlyDto
from models.ClientWithBillsNumbersOnlyDto import ClientWithBillsNumbersOnlyDto
from models.Client import Client


class ClientRepository:
    def __init__(self, clientsMongoHandler):
        self._clients_handler = clientsMongoHandler

    def findClientOnlyDto(self) -> [ClientOnlyDto]:  # wszyscy klienci bez rachunków
        client_only_dtos = []
        for client_mongo_dict in self._clients_handler.find():
            client_only_dtos.append(ClientOnlyDto(client_mongo_dict))
        return client_only_dtos

    def findByIdClientWithBillsNumbersOnlyDto(
            self, client_id) -> Optional[ClientWithBillsNumbersOnlyDto]:  # jeden klient tylko z listą numerów rachunków
        client_mongo_dict = self._clients_handler.find_one({'_id': ObjectId(client_id)})
        if client_mongo_dict is None:
            return None
        return ClientWithBillsNumbersOnlyDto(client_mongo_dict)

    def findBillDto(self) -> [
        BillDto]:  # wszystkie rachunki w postaci rachunku z artykułami w postaci samych id
        bill_dtos = []
        for client_mongo_dict in self._clients_handler.find():
            if 'bills' in client_mongo_dict:
                client_id = client_mongo_dict['_id']
                for bill_mongo_dict in client_mongo_dict['bills']:
                    bill_dtos.append(BillDto(bill_mongo_dict, client_id))
        return bill_dtos

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

    def update(self, updatedClient: ClientOnlyDto) -> bool:
        if updatedClient is None or not isinstance(updatedClient, ClientOnlyDto):
            raise TypeError('Invalid argument: updatedClient')
        updated_client_dict = updatedClient.toMongoDictionary()
        update_result = self._clients_handler.update_one({
            '_id': updated_client_dict['_id']
        }, {
            '$set': updated_client_dict
        })
        return update_result.matched_count == 1

    def remove(self, client_id: str) -> bool:
        delete_result = self._clients_handler.delete_one({
            '_id': ObjectId(client_id)
        })
        deleted_count = delete_result.deleted_count
        return deleted_count >= 1

    def addNewBill(self, client_id: str, newBill: Bill) -> bool:
        client_mongo_dict = self._clients_handler.find_one({'_id': ObjectId(client_id)})
        if client_mongo_dict is None:
            return False
        client_mongo_dict['bills'].append(newBill.toMongoDictionary())
        update_result = self._clients_handler.update_one({
            '_id': client_mongo_dict['_id']
        }, {
            '$set': client_mongo_dict
        })
        return update_result.matched_count == 1

    # def removeAllCreatedByWorker(self, workerNr: int):
    #     for client_mongo_dict in self._clients_handler.find({
    #         'bills': {
    #             'workerNr': workerNr
    #         }
    #     }):
    #         if 'bills' in client_mongo_dict:
    #             for bill_mongo_dict in client_mongo_dict['bills'].copy():
    #                 if bill_mongo_dict['workerNr'] == workerNr:
    #                     client_mongo_dict['bills'].remove(bill_mongo_dict)
    #             update_result = self._clients_handler.update_one({
    #                 '_id': client_mongo_dict['_id']
    #             }, {
    #                 '$set': client_mongo_dict
    #             })
