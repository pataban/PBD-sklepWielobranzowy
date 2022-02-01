from dbConnectivity.MysqlConnector import *


class ClientWithBillsNumbersOnlyDto:
    def __init__(self, client_orm: ClientORM):
        self.firstName = client_orm.firstName
        self.secondName = client_orm.secondName
        self.name = client_orm.name
        self.telephone = client_orm.telephone
        self.vatId = client_orm.vatId
        self.address = client_orm.address
        self.clientNr = client_orm.clientNr
        self.object_id = client_orm.id
        self.billsNumbers = []
        if 'bills' in client_orm.bills:
            for bill_orm in client_orm.bills:
                self.billsNumbers.append(bill_orm.billNr)

    def __str__(self) -> str:
        return 'ClientWithBillsNumbersOnlyDto {' + \
               'firstName: ' + str(self.firstName) + \
               ', secondName: ' + str(self.secondName) + \
               ', name: ' + str(self.name) + \
               ', telephone: ' + str(self.telephone) + \
               ', vatId: ' + str(self.vatId) + \
               ', address: ' + str(self.address) + \
               ', clientNr: ' + str(self.clientNr) + \
               ', object_id: ' + str(self.object_id) + \
               ', billsNumbers: ' + str(self.billsNumbers) + \
               '}'

    @classmethod
    def fromORM(cls, client_orm):
        pass

    def toORM(self):
        pass
