from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import users as model
from sqlalchemy.exc import SQLAlchemyError

# ===============
# User Controller
# ===============

# Create a new user in the database
# Parameters:
#   - db: Database session
#   - request: Data containing user details
# Returns:
#   - A new user object
def create(db: Session, request):
    new_user = model.User(
        customer_name = request.customer_name,
        payment_method = request.payment_method
    )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_user

# Retrieve all users from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all user objects
def read_all(db: Session):
    try:
        result = db.query(model.User).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Retrieve a single user by its ID
# Parameters:
#   - db: Database session
#   - user_id: ID of the user to retrieve
# Returns:
#   - The user object if found, raises 404 otherwise
def read_one(db: Session, user_id):
    try:
        result = db.query(model.User).filter(model.User.id == user_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Update an existing user by its ID
# Parameters:
#   - db: Database session
#   - user_id: ID of the user to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated user object
def update(db: Session, user_id, request):
    try:
        result = db.query(model.User).filter(model.User.id == user_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()

# Delete a user by its ID
# Parameters:
#   - db: Database session
#   - user_id: ID of the user to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, user_id):
    try:
        result = db.query(model.User).filter(model.User.id == user_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))

    return Response(status_code=status.HTTP_204_NO_CONTENT)