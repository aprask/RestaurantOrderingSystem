from fastapi.testclient import TestClient
from ..controllers import reviews as controller
from ..main import app
import pytest
from ..models import reviews as model

# Models and controllers for order, etc
from ..models import orders as order_model
from ..controllers import orders as order_controller
from ..models import restaurants as restaurant_model
from ..controllers import restaurants as restaurant_controller
from ..models import users as user_model
from ..controllers import users as user_controller
from ..models import sandwiches as sandwich_model
from ..controllers import sandwiches as sandwich_controller

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_review(db_session):

    # Create order and restaurant objects for mock db
    order_data = {
        "user_id": 1,
        "description": "Test order",
        "sandwich_id": 1,
        "amount": 10.00,
        "restaurant_id": 1,
        "delivery_method": "pickup",
        "status_of_order": "pending",
    }

    # Order requires a restaurant, user and sandwich model
    user_data = {
        "customer_name": "Test user",
        "payment_method": "cash"
    }

    sandwich_data = {
        "sandwich_name": "Test sandwich",
        "description": "Test description",
        "price": 10.00,
        "calories": 100,
        "sandwich_size": "small",
        "is_vegetarian": True,
        "is_vegan": False,
        "is_gluten_free": False
    }

    restaurant_data = {
        "restaurant_name": "(S)Andrew's Sandwiches"
    }

    user_object = user_model.User(**user_data)
    sandwich_object = sandwich_model.Sandwich(**sandwich_data)
    restaurant_object = restaurant_model.Restaurant(**restaurant_data)
    order_object = order_model.Order(**order_data)

    user_controller.create(db_session, user_object)
    sandwich_controller.create(db_session, sandwich_object)
    restaurant_controller.create(db_session, restaurant_object)
    order_controller.create(db_session, order_object)

    # Create a sample review
    review_data = {
        "order_id": 1,
        "restaurant_id": 1,
        "user_id": 1,
        "rating": 5,
        "description": "Test review"
    }

    review_object = model.Review(**review_data)

    # Call the create function
    created_review = controller.create(db_session, review_object)

    # Assertions
    assert created_review is not None
    assert created_review.order_id == 1
    assert created_review.restaurant_id == 1
    assert created_review.user_id == 1
    assert created_review.rating == 5
    assert created_review.description == "Test review"
