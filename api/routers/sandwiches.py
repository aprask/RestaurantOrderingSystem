from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import sandwiches as controller
from ..schemas import sandwiches as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=['Sandwiches'],
    prefix="/sandwiches"
)

@router.post("/", response_model=schema.Sandwich)
def create(request: schema.SandwichCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Sandwich])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

# @router.get("/{rest_id}", response_model=list[schema.Sandwich])
# def read_one(rest_id: int, db: Session = Depends(get_db)):
#     return controller.get_sandwich_by_rest(db, rest_id)

@router.get("/{sandwich_id}", response_model=schema.Sandwich)
def read_one(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, sandwich_id)

@router.put("/{sandwich_id}", response_model=schema.Sandwich)
def update(sandwich_id: int, request: schema.SandwichUpdate, db: Session = Depends(get_db)):
    return controller.update(db, sandwich_id, request)

@router.delete("/{sandwich_id}", response_model=schema.Sandwich)
def delete(sandwich_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, sandwich_id)