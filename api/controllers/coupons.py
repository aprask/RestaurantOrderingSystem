from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import coupons as model
from sqlalchemy.exc import SQLAlchemyError

# ========================
# Coupon Table Operations
# ========================

# Create a new coupon in the database
# Parameters:
#   - db: Database session
#   - request: Data containing coupon details (promo_code, is_active, restaurant_id, expir_date, discount)
# Returns:
#   - The newly created coupon object
def create(db: Session, request):
    new_coupon = model.Coupon(
        promo_code=request.promo_code,
        is_active=request.is_active,
        restaurant_id=request.restaurant_id,
        expir_date=request.expir_date,
        discount=request.discount
    )

    try:
        db.add(new_coupon)  # Add the new coupon to the session
        db.commit()         # Commit the transaction to persist changes
        db.refresh(new_coupon)  # Refresh the session to get the latest state of the object
    except SQLAlchemyError as error:
        db.rollback()  # Rollback the transaction in case of an error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return new_coupon

# Retrieve all coupons from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all coupon objects
def read_all(db: Session):
    try:
        result = db.query(model.Coupon).all()  # Query all coupons
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return result

# Retrieve a single coupon by its ID
# Parameters:
#   - db: Database session
#   - coupon_id: The unique ID of the coupon to retrieve
# Returns:
#   - The coupon object if found, otherwise raises 404 error
def read_one(db: Session, coupon_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.id == coupon_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return result

# Retrieve all coupons associated with a specific restaurant
# Parameters:
#   - db: Database session
#   - rest_id: The ID of the restaurant
# Returns:
#   - A list of coupons associated with the given restaurant
def get_coupon_by_rest(db: Session, rest_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.restaurant_id == rest_id).all()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No coupons found for the given restaurant")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return result

# Update an existing coupon by its ID
# Parameters:
#   - db: Database session
#   - coupon_id: The unique ID of the coupon to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated coupon object if successful
def update(db: Session, coupon_id, request):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.id == coupon_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
        update_data = request.dict(exclude_unset=True)  # Extract only fields present in the request
        result.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()  # Rollback transaction on error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return result.first()

# Delete an existing coupon by its ID
# Parameters:
#   - db: Database session
#   - coupon_id: The unique ID of the coupon to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, coupon_id):
    try:
        result = db.query(model.Coupon).filter(model.Coupon.id == coupon_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Coupon not found")
        result.delete(synchronize_session=False)  # Remove the coupon from the database
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
