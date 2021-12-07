class ClientOnlyDto:
    def __init__(self, clientMongoDict):
        self.firstName = clientMongoDict.get('firstName')
        self.secondName = clientMongoDict.get('secondName')
        self.name = clientMongoDict.get('name')
        self.telephone = clientMongoDict.get('telephone')
        self.vatId = clientMongoDict.get('vatId')
        self.address = clientMongoDict.get('address')
        self.clientNr = clientMongoDict.get('clientNr')
        self.object_id = clientMongoDict.get('_id')

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
