INSERT INTO users (id, customer_name, payment_method) VALUES
(1, 'John Doe', 'Credit Card'),
(2, 'Jane Smith', 'PayPal'),
(3, 'Alice Johnson', 'Cash');

INSERT INTO restaurants (id, restaurant_name) VALUES
(1, 'Burger Haven'),
(2, 'Pizza Palace'),
(3, 'Vegan Delights');

INSERT INTO sandwiches (id, sandwich_name, price, calories, sandwich_size, is_vegetarian, is_vegan, is_gluten_free) VALUES
(1, 'Classic Burger', 5.99, 500, 'Medium', 0, 0, 0),
(2, 'Veggie Delight', 4.99, 300, 'Small', 1, 1, 1),
(3, 'Chicken Sandwich', 6.99, 600, 'Large', 0, 0, 0);

INSERT INTO resources (id, item, amount) VALUES
(1, 'Lettuce', 100),
(2, 'Tomato', 200),
(3, 'Chicken', 50);

INSERT INTO recipes (id, sandwich_id, resource_id, amount) VALUES
(1, 1, 1, 2), -- Burger: 2 units of Lettuce
(2, 2, 2, 3), -- Veggie Sandwich: 3 units of Tomato
(3, 3, 3, 1); -- Chicken Sandwich: 1 unit of Chicken

INSERT INTO coupons (id, promo_code, is_active, restaurant_id) VALUES
(1, 'DISCOUNT10', 1, 1),
(2, 'FREESHIP', 1, 2),
(3, 'BOGO50', 0, 3);

INSERT INTO orders (id, user_id, order_date, description, sandwich_id, amount, restaurant_id, delivery_method, status_of_order) VALUES
(1, 1, '2024-01-01 12:00:00', 'Order 1 description', 1, 2, 1, 'Delivery', 'pending'),
(2, 2, '2024-01-02 13:00:00', 'Order 2 description', 2, 1, 2, 'Pickup', 'completed'),
(3, 3, '2024-01-03 14:00:00', 'Order 3 description', 3, 3, 3, 'Delivery', 'canceled');

INSERT INTO reviews (id, order_id, restaurant_id, user_id, rating, description) VALUES
(1, 1, 1, 1, 5, 'Great food!'),
(2, 2, 2, 2, 4, 'Tasty pizza!'),
(3, 3, 3, 3, 3, 'Good vegan options.');