INSERT INTO users (id, customer_name, payment_method) VALUES
(1, 'John Doe', 'Credit Card'),
(2, 'Jane Smith', 'PayPal'),
(3, 'Alice Johnson', 'Cash'),
(4, 'Bob Marley', 'Debit Card');

INSERT INTO restaurants (id, restaurant_name) VALUES
(1, 'Burger Haven'),
(2, 'Pizza Palace'),
(3, 'Vegan Delights'),
(4, 'Sandwich Spot');

INSERT INTO sandwiches (id, sandwich_name, price, calories, sandwich_size, is_vegetarian, is_vegan, is_gluten_free) VALUES
(1, 'Classic Burger', 5.99, 500, 'Medium', 0, 0, 0),
(2, 'Veggie Delight', 4.99, 300, 'Small', 1, 1, 1),
(3, 'Chicken Sandwich', 6.99, 600, 'Large', 0, 0, 0),
(4, 'Grilled Cheese', 3.99, 450, 'Small', 1, 0, 1),
(5, 'Gluten-Free Wrap', 6.49, 350, 'Medium', 1, 1, 1);

INSERT INTO resources (id, item, amount) VALUES
(1, 'Lettuce', 100),
(2, 'Tomato', 200),
(3, 'Chicken', 50),
(4, 'Cheese', 150),
(5, 'Gluten-Free Bread', 80);

INSERT INTO recipes (id, sandwich_id, resource_id, amount) VALUES
(1, 1, 1, 2), -- Classic Burger: 2 units of Lettuce
(2, 1, 2, 1), -- Classic Burger: 1 unit of Tomato
(3, 2, 1, 3), -- Veggie Delight: 3 units of Lettuce
(4, 2, 2, 2), -- Veggie Delight: 2 units of Tomato
(5, 3, 3, 1), -- Chicken Sandwich: 1 unit of Chicken
(6, 4, 4, 2), -- Grilled Cheese: 2 units of Cheese
(7, 5, 1, 1), -- Gluten-Free Wrap: 1 unit of Lettuce
(8, 5, 5, 1); -- Gluten-Free Wrap: 1 unit of Gluten-Free Bread

INSERT INTO coupons (id, promo_code, is_active, discount, expir_date, restaurant_id)
VALUES
(1, 'DISCOUNT10', 1, 10.0, '2024-12-31 23:59:59', 1),
(2, 'FREESHIP', 1, 0.0, '2024-12-31 23:59:59', 2),
(3, 'BOGO50', 0, 50.0, '2024-12-31 23:59:59', 3),
(4, 'WRAP15', 1, 15.0, '2024-12-31 23:59:59', 4);

INSERT INTO orders (id, user_id, order_date, description, sandwich_id, amount, restaurant_id, delivery_method, status_of_order, promo_code) VALUES
(1, 1, '2024-01-01 12:00:00', 'Order 1 description', 1, 2, 1, 'Delivery', 'pending', 'DISCOUNT10'),
(2, 2, '2024-01-02 13:00:00', 'Order 2 description', 2, 1, 2, 'Pickup', 'completed', null),
(3, 3, '2024-01-03 14:00:00', 'Order 3 description', 3, 3, 3, 'Delivery', 'canceled', 'BOGO50'),
(4, 4, '2024-01-04 15:00:00', 'Order 4 description', 4, 1, 4, 'Delivery', 'completed', 'WRAP15');

INSERT INTO reviews (id, order_id, restaurant_id, user_id, rating, description) VALUES
(1, 1, 1, 1, 5, 'Great food!'),
(2, 2, 2, 2, 4, 'Tasty pizza!'),
(3, 3, 3, 3, 3, 'Good vegan options.'),
(4, 4, 4, 4, 5, 'Amazing sandwiches!');