from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from server import schemas, services
from server.database import get_db

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello World"}

@app.get("/strategies", response_model=list[schemas.Strategy])
def get_strategies(db: Session = Depends(get_db)):
    service = services.StrategyService(db=db)
    return service.get_strategies()