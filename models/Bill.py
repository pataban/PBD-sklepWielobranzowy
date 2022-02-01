from datetime import datetime

from models.ArticleInBill import ArticleInBill
from models.PaymentMethod import PaymentMethod
from models.WorkerSafeDto import WorkerSafeDto


class Bill:
    def __init__(self, billNr, worker, paymentMethod=PaymentMethod.CASH, articlesInBill=None, isAlreadyPaid=False,
                 dateTime=None):
        if billNr is None or not isinstance(billNr, int):
            raise TypeError('Invalid argument: billNr')
        if worker is None or not isinstance(worker, WorkerSafeDto):
            raise TypeError('Invalid argument: worker')
        if not isinstance(paymentMethod, PaymentMethod):
            raise TypeError('Invalid argument: paymentMethod')
        if articlesInBill is not None:
            if not isinstance(articlesInBill, list):
                raise TypeError('Invalid argument: articles')
            if not all(isinstance(elem, ArticleInBill) for elem in articlesInBill):
                raise TypeError('Invalid argument: articles')
        if not isinstance(isAlreadyPaid, bool):
            raise TypeError('Invalid argument: isAlreadyPaid')
        if dateTime is not None and not isinstance(dateTime, datetime):
            raise TypeError('Invalid argument: dateTime')

        self.billNr = billNr
        self.worker = worker
        self.paymentMethod = paymentMethod
        if articlesInBill is None:
            self.articlesInBill = []
        else:
            self.articlesInBill = articlesInBill
        self.isAlreadyPaid = isAlreadyPaid
        if dateTime is None:
            self.dateTime = datetime.utcnow()
        else:
            self.dateTime = dateTime

    def toMongoDictionary(self):
        bill_dict = vars(self).copy()
        if 'worker' in bill_dict:
            bill_dict['workerNr'] = self.worker.nrP
            bill_dict.pop('worker')
        if 'articlesInBill' in bill_dict and len(self.articlesInBill) > 0:
            bill_dict.pop('articlesInBill')
            articles_in_bill_dicts = []
            for articleInBill in self.articlesInBill:
                articles_in_bill_dicts.append(articleInBill.toMongoDictionary())
            bill_dict['articlesInBill'] = articles_in_bill_dicts
        if 'paymentMethod' in bill_dict:
            bill_dict.update({'paymentMethod': self.paymentMethod.name})
        return bill_dict

    @classmethod
    def fromORM(cls, bill_orm):
        pass

    def toORM(self):
        pass

