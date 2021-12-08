from bson import ObjectId

from models.Bill import Bill


class Client:
    def __init__(self,
                 firstName=None,
                 secondName=None,
                 name=None,
                 telephone=None,
                 vatId=None,
                 address=None,
                 clientNr=None,
                 bills=None,
                 object_id=None):
        if firstName is not None and not isinstance(firstName, str):
            raise TypeError('Invalid argument: firstName')
        if secondName is not None and not isinstance(secondName, str):
            raise TypeError('Invalid argument: secondName')
        if name is not None and not isinstance(name, str):
            raise TypeError('Invalid argument: name')
        if telephone is not None and not isinstance(telephone, str):
            raise TypeError('Invalid argument: telephone')
        if vatId is not None and not isinstance(vatId, str):
            raise TypeError('Invalid argument: vatId')
        if address is not None and not isinstance(address, str):
            raise TypeError('Invalid argument: address')
        if clientNr is not None and not isinstance(clientNr, int):
            raise TypeError('Invalid argument: clientNr')
        if bills is not None:
            if not isinstance(bills, list):
                raise TypeError('Invalid argument: bills')
            if not all(isinstance(elem, Bill) for elem in bills):
                raise TypeError('Invalid argument: bills')
        if object_id is not None and not isinstance(object_id, str):
            raise TypeError('Invalid argument: object_id')

        if vatId is None and clientNr is None:
            raise ValueError('Arguments vadId and clientNr cannot both be None')

        self.firstName = firstName
        self.secondName = secondName
        self.name = name
        self.telephone = telephone
        self.vatId = vatId
        self.address = address
        self.clientNr = clientNr
        if bills is None:
            self.bills = []
        else:
            self.bills = bills
        self.object_id = object_id

    def toMongoDictionary(self):
        client_dict = vars(self).copy()
        if 'bills' in client_dict and len(self.bills) > 0:
            client_dict.pop('bills')
            bills_dicts = []
            for bill in self.bills:
                bills_dicts.append(bill.toMongoDictionary())
            client_dict['bills'] = bills_dicts
        for key in list(client_dict.keys()):
            if client_dict[key] is None:
                client_dict.pop(key)
        if 'object_id' in client_dict:
            client_dict.update({'_id': ObjectId(self.object_id)})
            client_dict.pop('object_id')
        return client_dict
