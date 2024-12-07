from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import orders as model
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError


# =====================
# Orders Table Actions
# =====================

# Create a new order in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the order details (user_id, order_date, description, etc.)
# Returns:
#   - The newly created order object
def create(db: Session, request):
    new_item = model.Order(
        user_id=request.user_id,
        order_date=request.order_date,
        description=request.description,
        sandwich_id=request.sandwich_id,
        amount=request.amount,
        restaurant_id=request.restaurant_id,
        delivery_method=request.delivery_method,
        status_of_order=request.status_of_order,
        promo_code=request.promo_code
    )

    try:
        db.add(new_item) # Add the order to the session
        db.commit() # Commit changes to persist the order
        db.refresh(new_item) # Refresh session to get updated state
    except SQLAlchemyError as error:
        db.rollback() # Rollback transaction on failure
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_item

# Get all orders from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all order objects
def read_all(db: Session):
    try:
        result = db.query(model.Order).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return result

# Get a single order by ID
# Parameters:
#   - db: Database session
#   - item_id: ID of the order to retrieve
# Returns:
#   - The order object if found, raises 404 otherwise
def read_one(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return item

# Get the most recent order based on order_date
# Parameters:
#   - db: Database session
# Returns:
#   - The most recent order object
def get_most_recent_order(db: Session):
    try:
        item = db.query(model.Order).order_by(model.Order.order_date.desc()).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Get the oldest order based on order_date
# Parameters:
#   - db: Database session
# Returns:
#   - The oldest order object
def get_oldest_order(db: Session):
    try:
        item = db.query(model.Order).order_by(model.Order.order_date.asc()).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Get all orders by a specific restaurant ID
# Parameters:
#   - db: Database session
#   - rest_id: Restaurant ID
# Returns:
#   - A list of orders for the specified restaurant
def get_order_by_rest(db: Session, rest_id):
    try:
        item = db.query(model.Order).filter(model.Order.restaurant_id == rest_id).all()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item

# Update an existing order
# Parameters:
#   - db: Database session
#   - item_id: ID of the order to update
#   - request: Data containing the updated fields
# Returns:
#   - The updated order object
def update(db: Session, item_id, request):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
        update_data = request.dict(exclude_unset=True)
        item.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return item.first()

# Delete an order by ID
# Parameters:
#   - db: Database session
#   - item_id: ID of the order to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, item_id):
    try:
        item = db.query(model.Order).filter(model.Order.id == item_id)
        if not item.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
        item.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def sort_orders_by_date(db: Session, start_date, end_date):
    try:
        items = db.query(model.Order).filter(
            model.Order.order_date >= start_date,
            model.Order.order_date <= end_date
        ).all()
        if not items:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No orders found within the specified date range."
            )
        return items
    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Database error: {error}"
        )