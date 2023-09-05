from app.crud.base import CRUDBase
from app.models.visit import Visit


class VisitCRUD(CRUDBase):
    pass


visit_crud = VisitCRUD(Visit)
