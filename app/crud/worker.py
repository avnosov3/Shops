from app.crud.base import CRUDBase
from app.models.worker import Worker


class WorkerCRUD(CRUDBase):
    pass


worker_crud = WorkerCRUD(Worker)
