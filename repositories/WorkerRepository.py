from typing import Optional

import pymongo
from bson import ObjectId
import sqlalchemy as sqla

from models.Worker import Worker
from models.WorkerSafeDto import WorkerSafeDto
from dbConnectivity.MysqlConnector import *

from resources.static.constants import *


class WorkerRepository:
    def __init__(self, workersMongoHandler):
        self._workers_handler = workersMongoHandler

    def find(self) -> [WorkerSafeDto]:
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        worker_objects = []
        for worker_orm in session.query(WorkerORM).all():
            worker_objects.append(WorkerSafeDto(worker_orm))
        session.close()
        return worker_objects

    def findById(self, worker_id) -> Optional[WorkerSafeDto]:
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        worker_result=session.query(WorkerORM).filter_by(id=worker_id)
        worker=None
        if(worker_result.count()==1):
            worker_orm = worker_result.one()
            worker=WorkerSafeDto(worker_orm)
        session.close()
        return worker

    def insert(self, newWorker: Worker) -> bool:
        if newWorker is None:
            raise TypeError('Argument newWorker cannot be None')
        if not isinstance(newWorker, Worker):
            raise TypeError('Argument newWorker must be of type Worker')
        if newWorker.id is not None:
            raise ValueError('New worker cannot have assigned id')
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        workerORM=newWorker.toORM()
        session.add(workerORM)
        session.commit()
        inserted_id = workerORM.id
        session.close()
        if inserted_id is None:
            return False
        newWorker.id = inserted_id  # inserting new worker will automatically fill id field by new _id in db
        return True

    def update(self, updatedWorker: WorkerSafeDto) -> bool:
        if updatedWorker is None or not isinstance(updatedWorker, WorkerSafeDto):
            raise TypeError('Invalid argument: updatedWorker')
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        updated_worker_orm = updatedWorker.toORM()
        select_result= session.query(WorkerORM).filter_by(id=updated_worker_orm.id)
        if(select_result.count()==1):
            worker_orm =select_result.one()
            worker_orm.update(updated_worker_orm)
            select_result=True
        else:
            select_result=False
        session.commit()
        session.close()
        return select_result

    def remove(self, worker_id: str) -> bool:
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        select_result = session.query(WorkerORM).filter_by(id=worker_id)
        delete_count = select_result.count()
        if(delete_count>0):
            session.delete(select_result.all())
        session.commit()
        session.close()
        return delete_count >= 1

    def login(self, login: str, password: str) -> Optional[WorkerSafeDto]:
        if login is None or not isinstance(login, str):
            raise TypeError('Invalid argument: login')
        if len(login) < MIN_LOGIN_LEN:
            raise ValueError('Argument login is too short')
        if password is None or not isinstance(password, str):
            raise TypeError('Invalid argument: password')
        if len(password) < MIN_PASSWORD_LEN:
            raise ValueError('Argument password is too short')

        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        select_result = session.query(WorkerORM).filter_by(login=login).filter_by(password=password)
        worker=None
        if(select_result.count()>0):
            worker_orm=select_result.all()[0]
            worker=WorkerSafeDto(worker_orm)
        session.close()
        return worker

    def maxWorkerNr(self) -> int:
        session=sqla.orm.sessionmaker(bind=self._workers_handler)()
        for result in session.query(WorkerORM).order_by(WorkerORM.workerNr.desc()).all():
            if result.workerNr is not None:
                session.close()
                return result.workerNr
        session.close()
        return -1
