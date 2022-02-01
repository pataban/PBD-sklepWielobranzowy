from bson import ObjectId

from dbConnectivity.MysqlConnector import *


class ClientOnlyDto:
    def __init__(self, client_orm):
        self.firstName = client_orm.firstName
        self.secondName = client_orm.secondName
        self.name = client_orm.name
        self.telephone = client_orm.telephone
        self.vatId = client_orm.vatId
        self.address = client_orm.address
        self.clientNr = client_orm.clientNr
        self.object_id = client_orm.id

    def __str__(self) -> str:
        return 'ClientOnlyDto {' + \
               'firstName: ' + str(self.firstName) + \
               ', secondName: ' + str(self.secondName) + \
               ', name: ' + str(self.name) + \
               ', telephone: ' + str(self.telephone) + \
               ', vatId: ' + str(self.vatId) + \
               ', address: ' + str(self.address) + \
               ', clientNr: ' + str(self.clientNr) + \
               ', object_id: ' + str(self.object_id) + \
               '}'
