from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import reviews as controller
from ..schemas import reviews as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=["Reviews"],
    prefix="/reviews"
)

@router.post("/", response_model=schema.Review)
def create(request: schema.ReviewCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Review])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{rest_id}", response_model=schema.Review)
def get_reviews_from_restaurant(rest_id: int, db: Session = Depends(get_db)):
    return controller.get_reviews_from_restaurant(db=db, rest_id=rest_id)

@router.get("/order-asc", response_model=list[schema.Review])
def order_rating_asc_order(db: Session = Depends(get_db)):
    return controller.sort_reviews_by_rating_asc(db)

@router.get("/order-desc", response_model=list[schema.Review])
def order_rating_asc_order(db: Session = Depends(get_db)):
    return controller.sort_reviews_by_rating_dsc(db)

@router.get("/{review_id}", response_model=schema.Review)
def read_one(review_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, review_id)

@router.put("/{review_id}", response_model=schema.Review)
def update(review_id: int, request: schema.ReviewUpdate, db: Session = Depends(get_db)):
    return controller.update(db, review_id, request)

@router.delete("/{review_id}", response_model=schema.Review)
def delete(review_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, review_id)