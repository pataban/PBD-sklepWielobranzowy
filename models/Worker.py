from bson import ObjectId

class Worker:
    def __init__(self,
                 nrP,
                 firstName,
                 secondName,
                 login,
                 password,
                 isSeller=False,
                 isManager=False,
                 isOwner=False,
                 object_id=None):  #object_id can be None if you want to insert new Worker
                                   #otherwise object_id should be actually filled
        if nrP is None or not isinstance(nrP, int):
            raise TypeError('Invalid argument: nrP')
        if firstName is None or not isinstance(firstName, str):
            raise TypeError('Invalid argument: firstName')
        if secondName is None or not isinstance(secondName, str):
            raise TypeError('Invalid argument: secondName')
        if login is None or not isinstance(login, str):
            raise TypeError('Invalid argument: login')
        if password is None or not isinstance(password, str):
            raise TypeError('Invalid argument: password')
        if not isinstance(isSeller, bool):
            raise TypeError('Invalid argument: isSeller')
        if not isinstance(isManager, bool):
            raise TypeError('Invalid argument: isManager')
        if not isinstance(isOwner, bool):
            raise TypeError('Invalid argument: isOwner')
        if object_id is not None and not isinstance(object_id, str):
            raise TypeError('Invalid argument: object_id')

        self.nrP = nrP
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
    def fromMongoDictionary(cls, worker_mong_dict):
        return cls(
            worker_mong_dict["nrP"],
            worker_mong_dict["firstName"],
            worker_mong_dict["secondName"],
            worker_mong_dict["login"],
            worker_mong_dict["password"],
            worker_mong_dict["isSeller"],
            worker_mong_dict["isManager"],
            worker_mong_dict["isOwner"],
            str(worker_mong_dict["_id"])
        )

    def toMongoDictionary(self):
        worker_dict = vars(self).copy()
        if 'id' in worker_dict:
            worker_dict.update({'_id': ObjectId(self.id)})
            worker_dict.pop('id')
        return worker_dict
