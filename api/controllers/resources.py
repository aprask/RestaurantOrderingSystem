from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import resources as model
from sqlalchemy.exc import SQLAlchemyError

# =========================
# Resource Table Controller
# =========================

# Create a new resource in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the resource details (item, amount)
# Returns:
#   - The newly created resource object
def create(db: Session, request):
    new_resource = model.Resource(
        item = request.item,
        amount = request.amount,
    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as error:
        db.rollback()
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource

# Retrieve all resources from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all resource objects
def read_all(db: Session):
    try:
        result = db.query(model.Resource).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Retrieve a single resource by its ID
# Parameters:
#   - db: Database session
#   - resource_id: ID of the resource to retrieve
# Returns:
#   - The resource object if found, raises 404 otherwise
def read_one(db: Session, resource_id):
    try:
        result = db.query(model.Resource).filter(model.Resource.id == resource_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Update an existing resource by its ID
# Parameters:
#   - db: Database session
#   - resource_id: ID of the resource to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated resource object
def update(db: Session, resource_id, request):
    try:
        result = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()

# Delete a resource by its ID
# Parameters:
#   - db: Database session
#   - resource_id: ID of the resource to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, resource_id):
    try:
        result = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)