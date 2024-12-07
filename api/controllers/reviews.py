from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import reviews as model
from sqlalchemy.exc import SQLAlchemyError

# =================
# Review Controller
# =================

# Create a new review in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the review details
# Returns:
#   - A new review object
def create(db: Session, request):
    new_review = model.Review(
        order_id = request.order_id,
        restaurant_id = request.restaurant_id,
        user_id = request.user_id,
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

# Retrieve all reviews from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all review objects
def read_all(db: Session):
    try:
        result = db.query(model.Review).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Retrieve a single review by its ID
# Parameters:
#   - db: Database session
#   - review_id: ID of the review to retrieve
# Returns:
#   - The review object if found, raises 404 otherwise
def read_one(db: Session, review_id):
    try:
        result = db.query(model.Review).filter(model.Review.id == review_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Update an existing review by its ID
# Parameters:
#   - db: Database session
#   - review_id: ID of the review to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated review object
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

# Delete a review by its ID
# Parameters:
#   - db: Database session
#   - review_id: ID of the review to delete
# Returns:
#   - A 204 No Content response if successful
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

# Retrieve all reviews sorted by rating in ascending order
# Parameters:
#   - db: Database session
# Returns:
#   - A list of reviews sorted by ascending rating
def sort_reviews_by_rating_asc(db: Session):
    try:
        result = db.query(model.Review).order_by(model.Review.rating.asc()).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Retrieve all reviews sorted by rating in descending order
# Parameters:
#   - db: Database session
# Returns:
#   - A list of reviews sorted by descending rating
def sort_reviews_by_rating_dsc(db: Session):
    try:
        result = db.query(model.Review).order_by(model.Review.rating.desc()).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__["orig"])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return result

# Retrieve all reviews for a specific restaurant
# Parameters:
#   - db: Database session
#   - rest_id: ID of the restaurant
# Returns:
#   - A list of reviews for the specified restaurant
def get_reviews_from_restaurant(db: Session, rest_id):
    try:
        item = db.query(model.Review).filter(model.Review.restaurant_id == rest_id).first()
        if not item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="ID not found!")
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return item