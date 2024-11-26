from . import orders
from . import reviews


def load_routes(app):
    app.include_router(reviews.router)