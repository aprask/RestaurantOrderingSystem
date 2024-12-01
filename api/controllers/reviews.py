from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import reviews as model
from sqlalchemy.exc import SQLAlchemyError

def create(db: Session, request):
    new_review = model.Review(
        order_id = request.order_id,
        restaurant_id = request.restaurant_id,
        rating = request.rating,
        description = request.description
    )

    try:
        db.add(new_review)
        db.commit()
        db.refresh(new_review)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_review

def read_all(db: Session):
    try:
        result = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

def read_one(db: Session, review_id):
    try:
        result = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

def update(db: Session, review_id, request):
    try:
        result = db.query(model.Review).filter(model.Review.id == review_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset=True)
        result.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result.first()

def delete(db: Session, review_id):
    try:
        result = db.query(model.Review).filter(model.Review.id == review_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)