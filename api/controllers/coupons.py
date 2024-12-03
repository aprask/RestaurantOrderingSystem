from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import coupons as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_coupon = model.Coupon(
        promo_code = request.promo_code,
        is_active = request.is_active,
        restaurant_id = request.restaurant_id,
        expir_date = request.expir_date,
        discount=request.discount
    )

    try:
        db.add(new_coupon)
        db.commit()
        db.refresh(new_coupon)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_coupon

def read_all(db: Session):
    try:
        result = db.query(model.Coupon).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, coupon_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.id == coupon_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

def get_coupon_by_rest(db: Session, rest_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.restaurant_id == rest_id).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update(db: Session, coupon_id, request):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.restaurant_id == coupon_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()

def delete(db: Session, coupon_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.restaurant_id == coupon_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)