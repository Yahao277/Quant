from datetime import datetime

from pydantic import BaseModel

class StrategyBase(BaseModel):
    name: str

class StrategyCreate(StrategyBase):
    pass

class Strategy(StrategyBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True