from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response, Depends
from ..models import recipes, sandwiches, resources as model
from sqlalchemy.exc import SQLAlchemyError
from ..schemas.recipes import DeductResourcesResponse

# =======================
# Recipe Table Controller
# =======================

# Create a new recipe entry in the database
# Parameters:
#   - db: Database session
#   - request: Data containing the recipe details
# Returns:
#   - The newly created recipe object
def create(db: Session, request):
    new_recipe = model.Recipe(
        sandwich_id = request.sandwich_id,
        resource_id = request.resource_id,
        amount = request.amount
    )

    try:
        db.add(new_recipe)
        db.commit()
        db.refresh(new_recipe)

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_recipe

# Deduct resources needed for a specific sandwich
# Parameters:
#   - db: Database session
#   - sandwich_id: ID of the sandwich for which resources are to be deducted
# Returns:
#   - DeductResourcesResponse containing details of deducted resources
def deduct_resources(db: Session, sandwich_id):
    try:
        sandwich = db.query(model.Sandwich).filter(model.Sandwich.id == sandwich_id).first()
        if not sandwich:
            raise HTTPException(status_code=404, detail="Sandwich not found")
        recipes = db.query(model.Recipe).filter(model.Recipe.sandwich_id == sandwich_id).all() # get recipes (could one or many)
        if not recipes:
            raise HTTPException(status_code=400, detail="No recipes found for this sandwich")
        deducted_resources = []
        for recipe in recipes:
            resource = db.query(model.Resource).filter(model.Resource.id == recipe.resource_id).first()
            if not resource:
                raise HTTPException(status_code=404, detail=f"Resource with ID {recipe.resource_id} not found")
            if resource.amount < recipe.amount:
                db.rollback()
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Insufficient resources")
            resource.amount -= recipe.amount # deduct
            deducted_resources.append({ # response body
                "resource_id": resource.id,
                "resource_name": resource.item,
                "deducted_amount": recipe.amount,
                "remaining_amount": resource.amount
            })
        db.commit()

    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return DeductResourcesResponse(deducted_resources)

# Get all recipe entries from the database
# Parameters:
#   - db: Database session
# Returns:
#   - A list of all recipe objects
def read_all(db: Session):
    try:
        result = db.query(model.Recipe).all()
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Get a single recipe by its ID
# Parameters:
#   - db: Database session
#   - recipe_id: ID of the recipe to retrieve
# Returns:
#   - The recipe object if found, raises 404 otherwise
def read_one(db: Session, recipe_id):
    try:
        result = db.query(model.Recipe).filter(model.Recipe.id == recipe_id).first()
        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    except SQLAlchemyError as error:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result

# Update an existing recipe by its ID
# Parameters:
#   - db: Database session
#   - recipe_id: ID of the recipe to update
#   - request: Data containing the fields to update
# Returns:
#   - The updated recipe object
def update(db: Session, recipe_id, request):
    try:
        result = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        update_data = request.dict(exclude_unset = True)
        result.update(update_data, synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return result.first()


# Delete a recipe by its ID
# Parameters:
#   - db: Database session
#   - recipe_id: ID of the recipe to delete
# Returns:
#   - A 204 No Content response if successful
def delete(db: Session, recipe_id):
    try:
        result = db.query(model.Recipe).filter(model.Recipe.id == recipe_id)
        if not result.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        result.delete(synchronize_session=False)
        db.commit()

    except SQLAlchemyError as error:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return Response(status_code=status.HTTP_204_NO_CONTENT)