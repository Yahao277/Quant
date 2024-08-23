from typing import List, Type

from sqlalchemy.orm import Session
from . import schemas, models
from .models import Strategy


class StrategyService:
    def __init__(self, db: Session):
        self.db = db

    def get_strategies(self) -> list[Type[Strategy]]:
        return self.db.query(models.Strategy).limit(10).all()