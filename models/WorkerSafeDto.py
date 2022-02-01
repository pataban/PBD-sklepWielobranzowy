from bson import ObjectId
from dbConnectivity.MysqlConnector import *


class WorkerSafeDto:
    def __init__(self, worker_orm):  # WorkerSafeDto can be obtained only by logging in through WorkerRepository

        self.nrP = worker_orm.workerNr
        self.firstName = worker_orm.firstName
        self.secondName = worker_orm.secondName
        self.isSeller = worker_orm.isSeller
        self.isManager = worker_orm.isManager
        self.isOwner = worker_orm.isOwner
        self.id = worker_orm.id

    def toMongoDictionary(self):
        worker_dict = vars(self).copy()
        if 'id' in worker_dict:
            worker_dict.update({'_id': ObjectId(self.id)})
            worker_dict.pop('id')
        return worker_dict

    def toORM(self):
        return WorkerORM(
            id=self.id,
            workerNr=self.nrP,
            firstName=self.firstName,
            secondName=self.secondName,
            login=None,
            password=None,
            isSeller=self.isSeller,
            isManager=self.isManager,
            isOwner=self.isOwner
        )

