from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import orders as schema
from ..dependencies.database import Base, get_db

router = APIRouter(
    tags=['Orders'],
    prefix="/orders"
)


@router.post("/", response_model=schema.Order)
def create(request: schema.OrderCreate, db: Session = Depends(get_db)):
    return controller.create(db=db, request=request)

@router.get("/", response_model=list[schema.Order])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/revenue")
def get_total_revenue(db: Session = Depends(get_db)):
    return controller.get_total_revenue(db=db)

@router.post("/sort-date", response_model=list[schema.Order])
def sort_orders_by_date(request: schema.SortOrdersRequest, db: Session = Depends(get_db)):
    return controller.sort_orders_by_date(db, start_date=request.start_date, end_date=request.end_date)

@router.get("/latest", response_model=schema.Order)
def get_most_recent_order(db: Session = Depends(get_db)):
    return controller.get_most_recent_order(db=db)

@router.get("/oldest", response_model=schema.Order)
def get_oldest_order(db: Session = Depends(get_db)):
    return controller.get_oldest_order(db=db)

@router.get("/{item_id}", response_model=schema.Order)
def read_one(item_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, item_id=item_id)

@router.get("/{rest_id}", response_model=list[schema.Order])
def get_order_by_rest(rest_id: int, db: Session = Depends(get_db)):
    return controller.get_order_by_rest(db, rest_id=rest_id)

@router.put("/{item_id}", response_model=schema.Order)
def update(item_id: int, request: schema.OrderUpdate, db: Session = Depends(get_db)):
    return controller.update(db=db, request=request, item_id=item_id)

@router.delete("/{item_id}")
def delete(item_id: int, db: Session = Depends(get_db)):
    return controller.delete(db=db, item_id=item_id)