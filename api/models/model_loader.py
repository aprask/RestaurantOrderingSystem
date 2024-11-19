from . import orders, recipes, sandwiches, resources, restaurants, users, coupons

from dependencies.database import engine


def index():
    orders.Base.metadata.create_all(engine)
    recipes.Base.metadata.create_all(engine)
    sandwiches.Base.metadata.create_all(engine)
    resources.Base.metadata.create_all(engine)
    restaurants.Base.metadata.create_all(engine)
    users.Base.metadata.create_all(engine)
    coupons.Base.metadata.create_all(engine)