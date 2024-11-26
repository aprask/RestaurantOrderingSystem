from fastapi import APIRouter, Depends, FastAPI, status, Response
from sqlalchemy.orm import Session
from ..controllers import orders as controller
from ..schemas import coupons as schema
from ..dependencies.database import engine, get_db

router = APIRouter(
    tags=["Coupons"],
    prefix="/coupons"
)

@router.post("/", response_model=schema.Coupon)
def create(request: schema.CouponCreate, db: Session = Depends(get_db)):
    return controller.create(db, request)

@router.get("/", response_model=list[schema.Coupon])
def read_all(db: Session = Depends(get_db)):
    return controller.read_all(db)

@router.get("/{coupon_id}", response_model=schema.Coupon)
def read_one(coupon_id: int, db: Session = Depends(get_db)):
    return controller.read_one(db, coupon_id)

@router.put("/{coupon_id}", response_model=schema.Coupon)
def update(coupon_id: int, request: schema.CouponUpdate, db: Session = Depends(get_db)):
    return controller.update(db, coupon_id, request)

@router.delete("/{coupon_id}", response_model=schema.Coupon)
def delete(coupon_id: int, db: Session = Depends(get_db)):
    return controller.delete(db, coupon_id)