from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import sandwiches as model
from sqlalchemy.exc import SQLAlchemyError

# ===================
# Sandwich Controller
# ===================

# Create a new sandwich in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the sandwich details (name, price, calories, size, etc.)
# Returns:
#   - The newly created sandwich object
def create(db: Session, request):
    new_sandwich = model.Sandwich(
        sandwich_name=request.sandwich_name,
        price=request.price,
        calories=request.calories,
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

# Retrieve all sandwiches from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all sandwich objects
def read_all(db: Session):
    try:
        return db.query(model.Sandwich).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Filter sandwiches based on specific criteria
# Parameters:
#   - db: Database session
#   - filter_string: A string to filter sandwiches by
# Returns:
#   - A list of sandwiches that match the filter string
def filter_by(db: Session, filter_string):
    try:
        if filter_string=="vegan":
            result = db.query(model.Sandwich).filter(model.Sandwich.is_vegan)
        elif filter_string=="vegetarian":
            result = db.query(model.Sandwich).filter(model.Sandwich.is_vegetarian)
        elif filter_string == "gluten free" or filter_string == "gluten_free":
            result = db.query(model.Sandwich).filter(model.Sandwich.is_gluten_free)
        elif filter_string.isalpha():
            result = db.query(model.Sandwich).filter(model.Sandwich.sandwich_name.contains(filter_string))
        elif filter_string.isdigit:
            result = db.query(model.Sandwich).filter(model.Sandwich.id == filter_string)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Retrieve a single sandwich by its ID
# Parameters:
#   - db: Database session
#   - sandwich_id: ID of the sandwich to retrieve
# Returns:
#   - The sandwich object if found, raises 404 otherwise
def read_one(db: Session, sandwich_id):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Update an existing sandwich by its ID
# Parameters:
#   - db: Database session
#   - sandwich_id: ID of the sandwich to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated sandwich object
def update(db: Session, sandwich_id, request):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()

# Delete a sandwich by its ID
# Parameters:
#   - db: Database session
#   - sandwich_id: ID of the sandwich to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, sandwich_id):
    try:
        result = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)