from fastapi.testclient import TestClient
from ..controllers import reviews as controller
from ..main import app
import pytest
from ..models import reviews as model

# Create a test client for the app
client = TestClient(app)


@pytest.fixture
def db_session(mocker):
    return mocker.Mock()


def test_create_review(db_session):
    # Create a sample review
    review_data = {
        "order_id": 1,
        "restaurant_id": 1,
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
    assert created_review.rating == 5
    assert created_review.description == "Test review"
