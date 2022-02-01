from bson import ObjectId
from dbConnectivity.MysqlConnector import *


class WorkerSafeDto:
    def __init__(self, worker_mongo_dict):  # WorkerSafeDto can be obtained only by logging in through WorkerRepository

        self.nrP = worker_mongo_dict["worker_id"]
        self.firstName = worker_mongo_dict["firstName"]
        self.secondName = worker_mongo_dict["secondName"]
        self.isSeller = worker_mongo_dict["isSeller"]
        self.isManager = worker_mongo_dict["isManager"]
        self.isOwner = worker_mongo_dict["isOwner"]
        self.id = str(worker_mongo_dict["_id"])

    def toMongoDictionary(self):
        worker_dict = vars(self).copy()
        if 'id' in worker_dict:
            worker_dict.update({'_id': ObjectId(self.id)})
            worker_dict.pop('id')
        return worker_dict

    @classmethod
    def fromORM(cls, worker_orm):
        return cls({
            "workerNr":worker_orm.workerNr,
            "firstName":worker_orm.firstName,
            "secondName":worker_orm.secondName,
            "isSeller":worker_orm.isSeller,
            "isManager":worker_orm.isManager,
            "isOwner":worker_orm.isOwner,
            "_id":worker_orm.id
        })

    def toORM(self):
        return WorkerORM(id=self.id,workerNr=self.nrP,
                firstName=self.firstName,secondName=self.secondName,
                login=None,password=None,
                isSeller=self.isSeller,isManager=self.isManager,
                isOwner=self.isOwner)

