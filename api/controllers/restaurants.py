from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import restaurants as model
from sqlalchemy.exc import SQLAlchemyError

# =====================
# Restaurant Controller
# =====================

# Create a new restaurant in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the restaurant details
# Returns:
#   - The newly created restaurant object
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

# Retrieve all restaurants from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all restaurant objects
def read_all(db: Session):
    try:
        result = db.query(model.Restaurant).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Retrieve a single restaurant by its ID
# Parameters:
#   - db: Database session
#   - restaurant_id: ID of the restaurant to retrieve
# Returns:
#   - The restaurant object if found, raises 404 otherwise
def read_one(db: Session, restaurant_id):
    try:
        result = db.query(model.Restaurant).filter(model.Restaurant.id == restaurant_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Update an existing restaurant by its ID
# Parameters:
#   - db: Database session
#   - restaurant_id: ID of the restaurant to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated restaurant object
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

# Delete a restaurant by its ID
# Parameters:
#   - db: Database session
#   - restaurant_id: ID of the restaurant to delete
# Returns:
#   - A 204 No Content response if successful
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