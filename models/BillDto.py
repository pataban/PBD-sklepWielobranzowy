from models.PaymentMethod import PaymentMethod


class BillDto:
    def __init__(self, bill_mongo_dict, client_id):
        self.billNr = bill_mongo_dict.get('billNr')
        self.workerNr = bill_mongo_dict.get('workerNr')
        if bill_mongo_dict.get('paymentMethod') == 'CASH':
            self.paymentMethod = PaymentMethod.CASH
        elif bill_mongo_dict.get('paymentMethod') == 'BANK_TRANSFER':
            self.paymentMethod = PaymentMethod.BANK_TRANSFER
        else:
            self.paymentMethod = None
        self.articlesIds = []
        if 'articlesInBill' in bill_mongo_dict:
            for articleInBill in bill_mongo_dict.get('articlesInBill'):
                self.articlesIds.append(str(articleInBill.get('article_id')))
        self.isAlreadyPaid = bill_mongo_dict.get('isAlreadyPaid')
        self.dateTime = bill_mongo_dict.get('dateTime')
        self.client_id = str(client_id)

    def __str__(self) -> str:
        return 'BillDto {' + \
            'billNr: ' + str(self.billNr) + \
            ', workerNr: ' + str(self.workerNr) + \
            ', paymentMethod: ' + str(self.paymentMethod) + \
            ', articlesIds: ' + str(self.articlesIds) + \
            ', isAlreadyPaid: ' + str(self.isAlreadyPaid) + \
            ', dateTime: ' + str(self.dateTime) + \
            ', client_id: ' + str(self.client_id) + \
            '}'
