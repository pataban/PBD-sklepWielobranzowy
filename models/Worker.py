from bson import ObjectId

from resources.static.constants import *


class Worker:
    def __init__(self,
                 workerNr,
                 firstName,
                 secondName,
                 login,
                 password,
                 isSeller=False,
                 isManager=False,
                 isOwner=False,
                 object_id=None):  # object_id can be None if you want to insert new Worker
                                   # object_id should be actually filled otherwise
        if workerNr is None or not isinstance(workerNr, int):
            raise TypeError('Invalid argument: worker_id')
        if firstName is None or not isinstance(firstName, str):
            raise TypeError('Invalid argument: firstName')
        if secondName is None or not isinstance(secondName, str):
            raise TypeError('Invalid argument: secondName')
        if login is None or not isinstance(login, str):
            raise TypeError('Invalid argument: login')
        if len(login) < MIN_LOGIN_LEN:
            raise ValueError('Argument login is too short')
        if password is None or not isinstance(password, str):
            raise TypeError('Invalid argument: password')
        if len(password) < MIN_PASSWORD_LEN:
            raise ValueError('Argument password is too short')
        if not isinstance(isSeller, bool):
            raise TypeError('Invalid argument: isSeller')
        if not isinstance(isManager, bool):
            raise TypeError('Invalid argument: isManager')
        if not isinstance(isOwner, bool):
            raise TypeError('Invalid argument: isOwner')
        if object_id is not None and not isinstance(object_id, str):
            raise TypeError('Invalid argument: object_id')

        self.workerNr = workerNr
        self.firstName = firstName
        self.secondName = secondName
        self.login = login
        self.password = password
        self.isSeller = isSeller
        self.isManager = isManager
        self.isOwner = isOwner
        if object_id is None:
            self.id = None
        else:
            self.id = object_id

    @classmethod
    def fromMongoDictionary(cls, worker_mongo_dict):
        return cls(
            worker_mongo_dict["worker_id"],
            worker_mongo_dict["firstName"],
            worker_mongo_dict["secondName"],
            worker_mongo_dict["login"],
            worker_mongo_dict["password"],
            worker_mongo_dict["isSeller"],
            worker_mongo_dict["isManager"],
            worker_mongo_dict["isOwner"],
            str(worker_mongo_dict["_id"])
        )

    def toMongoDictionary(self):
        worker_dict = vars(self).copy()
        if 'id' in worker_dict:
            worker_dict.update({'_id': ObjectId(self.id)})
            worker_dict.pop('id')
        return worker_dict

    @classmethod
    def fromORM(cls, worker_orm):
        pass

    def toORM(self):
        pass

