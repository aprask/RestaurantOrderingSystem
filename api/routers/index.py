from . import orders, coupons, users, reviews, restaurants, recipes


def load_routes(app):
    app.include_router(orders.router)
    app.include_router(coupons.router)
    app.include_router(users.router)
    app.include_router(reviews.router)
    app.include_router(recipes.router)
    app.include_router(restaurants.router)