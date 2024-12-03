from datetime import datetime
from typing import Optional
from pydantic import BaseModel
from .resources import Resource
from .sandwiches import Sandwich
from typing import List



class RecipeBase(BaseModel):
    amount: int
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None

class RecipeCreate(RecipeBase):
    pass

class RecipeUpdate(BaseModel):
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None
    amount: Optional[int] = None

class Recipe(RecipeBase):
    id: int
    sandwich_id: Optional[int] = None
    resource_id: Optional[int] = None

    class ConfigDict:
        from_attributes = True
class DeductedResource(BaseModel):
    resource_id: int
    resource_name: str
    deducted_amount: int
    remaining_amount: int

class DeductResourcesResponse(BaseModel):
    deducted_resources: List[DeductedResource]