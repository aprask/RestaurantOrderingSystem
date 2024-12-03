from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import restaurants as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_restaurant = model.Restaurant(
        restaurant_name = request.restaurant_name
    )

    try:
        db.add(new_restaurant)
        db.commit()
        db.refresh(new_restaurant)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_restaurant


def read_all(db: Session):
    try:
        result = db.query(model.Restaurant).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result


def read_one(db: Session, restaurant_id):
    try:
        result = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

def update(db: Session, restaurant_id, request):
    try:
        result = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()


def delete(db: Session, restaurant_id):
    try:
        result = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)