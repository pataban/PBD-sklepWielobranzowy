from typing import Optional

from bson import ObjectId

from models.Worker import Worker


class WorkerRepository:
    def __init__(self, workersMongoHandler):
        self._workers_handler = workersMongoHandler

    def find(self) -> [Worker]:
        worker_objects = []
        for worker_mongo_dict in self._workers_handler.find():
            worker_objects.append(Worker.fromMongoDictionary(worker_mongo_dict))
        return worker_objects

    def findById(self, worker_id) -> Optional[Worker]:
        worker_mongo_dict = self._workers_handler.find_one({'_id': ObjectId(worker_id)})
        if worker_mongo_dict is None:
            return None
        return Worker.fromMongoDictionary(worker_mongo_dict)

    def insert(self, newWorker: Worker) -> bool:
        if newWorker is None:
            raise TypeError('Argument newWorker cannot be None')
        if not isinstance(newWorker, Worker):
            raise TypeError('Argument newWorker must be of type Worker')
        if newWorker.id is not None:
            raise ValueError('New worker cannot have assigned id')
        insert_one_result = self._workers_handler.insert_one(newWorker.toMongoDictionary)
        inserted_id = insert_one_result.inserted_id
        if inserted_id is None:
            return False
        newWorker.id = str(inserted_id)     # inserting new worker will automatically fill id field by new _id in db
        return True

    def update(self, updatedWorker: Worker) -> bool:
        if updatedWorker is None or not isinstance(updatedWorker, Worker):
            raise TypeError('Invalid argument: updatedWorker')
        updated_worker_dict = updatedWorker.toMongoDictionary()
        update_result = self._workers_handler.update_one({
            '_id': updated_worker_dict['_id']
        }, {
            '$set': updated_worker_dict
        })
        return update_result.matched_count == 1

    def remove(self, existingWorker: Worker) -> bool:
        if existingWorker is None or not isinstance(existingWorker, Worker):
            raise TypeError('Invalid argument: existingWorker')
        existing_article_dict = existingWorker.toMongoDictionary()
        delete_result = self._workers_handler.delete_one(
            existing_article_dict
        )
        deleted_count = delete_result.deleted_count
        if deleted_count < 1:
            return False
        existingWorker.id = None
        return True
