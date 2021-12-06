from decimal import Decimal


class Article:
    def __init__(self, code, name, actualPrice, object_id=None):    #object_id can be None if you want to insert new Article
                                                                    #otherwise object_id should be actually filled
        if code is None or not isinstance(code, int):
            raise TypeError('Invalid argument: code')
        if name is None or not isinstance(name, str):
            raise TypeError('Invalid argument: name')
        if actualPrice is None or not isinstance(actualPrice, Decimal):
            raise TypeError('Invalid argument: actualPrice')
        if object_id is not None and not isinstance(object_id, str):
            raise TypeError('Invalid argument: object_id')

        self.code = code
        self.name = name
        self.actualPrice = actualPrice
        if object_id is None:
            self.id = None
        else:
            self.id = object_id

    def __str__(self) -> str:
        return 'Article {' + \
               'id: ' + str(self.id) + \
               ', code: ' + str(self.code) + \
               ', name: ' + str(self.name) + \
               ', price: ' + str(self.actualPrice) + \
               '}'





