from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_sandwich = model.Sandwich(
        sandwich_name = request.sandwich_name,
        price = request.price,
        calories = request.calories,
        sandwich_size=request.sandwich_size,
        is_vegetarian=request.is_vegetarian,
        is_vegan=request.is_vegan,
        is_gluten_free=request.is_gluten_free
    )

    try:
        db.add(new_sandwich)
        db.commit()
        db.refresh(new_sandwich)
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_sandwich

def read_all(db: Session):
    try:
        result = db.query(model.Sandwich).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def read_one(db: Session, sandwich_id):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# def get_sandwich_by_rest(db: Session, rest_id):
#     try:
#         result = db.query(model.Sandwich).filter(model.Sandwich.restaurant_id == rest_id).all()
#         if not result:
#             raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
#     except SQLAlchemyError as error:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
#     return result

def update(db: Session, sandwich_id, request):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.restaurant_id == sandwich_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()

def delete(db: Session, sandwich_id):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.order_id == sandwich_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)