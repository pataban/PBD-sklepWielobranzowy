from bson import ObjectId

class WorkerSafeDto:
    def __init__(self, worker_mongo_dict):  #WorkerSafeDto can be obtained only by logging in through WorkerRepository

        self.nrP = worker_mongo_dict["nrP"]
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
