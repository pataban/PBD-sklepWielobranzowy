from bson import ObjectId

from dbConnectivity.MysqlConnector import *


class ClientOnlyDto:
    def __init__(self, client_orm: ClientORM):
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

    def toMongoDictionary(self):
        client_dict = vars(self).copy()
        for key in list(client_dict.keys()):
            if client_dict[key] is None:
                client_dict.pop(key)
        if 'object_id' in client_dict:
            client_dict.update({'_id': ObjectId(self.object_id)})
            client_dict.pop('object_id')
        return client_dict

    @classmethod
    def fromORM(cls, client_orm):
        pass

    def toORM(self):
        pass
