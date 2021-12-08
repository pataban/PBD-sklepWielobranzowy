from typing import Optional

from bson import ObjectId

from models.Worker import Worker
from models.WorkerSafeDto import WorkerSafeDto

from resources.static.constants import *


class WorkerRepository:
    def __init__(self, workersMongoHandler):
        self._workers_handler = workersMongoHandler

    def find(self) -> [WorkerSafeDto]:
        worker_objects = []
        for worker_mongo_dict in self._workers_handler.find():
            worker_objects.append(WorkerSafeDto(worker_mongo_dict))
        return worker_objects

    def findById(self, worker_id) -> Optional[WorkerSafeDto]:
        worker_mongo_dict = self._workers_handler.find_one({'_id': ObjectId(worker_id)})
        if worker_mongo_dict is None:
            return None
        return WorkerSafeDto(worker_mongo_dict)

    def insert(self, newWorker: Worker) -> bool:
        if newWorker is None:
            raise TypeError('Argument newWorker cannot be None')
        if not isinstance(newWorker, Worker):
            raise TypeError('Argument newWorker must be of type Worker')
        if newWorker.id is not None:
            raise ValueError('New worker cannot have assigned id')
        insert_one_result = self._workers_handler.insert_one(newWorker.toMongoDictionary())
        inserted_id = insert_one_result.inserted_id
        if inserted_id is None:
            return False
        newWorker.id = str(inserted_id)  # inserting new worker will automatically fill id field by new _id in db
        return True

    def update(self, updatedWorker: WorkerSafeDto) -> bool:
        if updatedWorker is None or not isinstance(updatedWorker, WorkerSafeDto):
            raise TypeError('Invalid argument: updatedWorker')
        updated_worker_dict = updatedWorker.toMongoDictionary()
        update_result = self._workers_handler.update_one({
            '_id': updated_worker_dict['_id']
        }, {
            '$set': updated_worker_dict
        })
        return update_result.matched_count == 1

    def remove(self, worker_id: str) -> bool:
        delete_result = self._workers_handler.delete_one({
            '_id': ObjectId(worker_id)
        })
        deleted_count = delete_result.deleted_count
        return deleted_count >= 1

    def login(self, login: str, password: str) -> Optional[WorkerSafeDto]:
        if login is None or not isinstance(login, str):
            raise TypeError('Invalid argument: login')
        if len(login) < MIN_LOGIN_LEN:
            raise ValueError('Argument login is too short')
        if password is None or not isinstance(password, str):
            raise TypeError('Invalid argument: password')
        if len(password) < MIN_PASSWORD_LEN:
            raise ValueError('Argument password is too short')

        worker_mongo_dict = self._workers_handler.find_one({
            'login': login,
            'password': password
        })
        if worker_mongo_dict is None:
            return None
        return WorkerSafeDto(worker_mongo_dict)
