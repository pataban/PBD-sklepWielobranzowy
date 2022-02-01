from dbConnectivity.MysqlConnector import BillORM
from models.PaymentMethod import PaymentMethod


class NewBillDto:
    def __init__(self, worker_number, paymentMethod, isAlreadyPaid, dateTime, client_number):

        self.worker_number = worker_number
        self.paymentMethod = paymentMethod
        self.isAlreadyPaid = isAlreadyPaid
        self.dateTime = dateTime
        self.client_number = client_number

    def __str__(self) -> str:
        return 'BillDto {' + \
               'worker_number: ' + str(self.worker_number) + \
               ', paymentMethod: ' + str(self.paymentMethod) + \
               ', isAlreadyPaid: ' + str(self.isAlreadyPaid) + \
               ', dateTime: ' + str(self.dateTime) + \
               ', client_number: ' + str(self.client_number) + \
               '}'
