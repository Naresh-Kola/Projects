-- ============================================================
-- ECOM_ANALYTICS.RAW - Load Sample Data
-- ============================================================

USE DATABASE ECOM_ANALYTICS;
USE SCHEMA RAW;

-- Customers (5 rows)
INSERT INTO RAW_CUSTOMERS (CUSTOMER_ID, FIRST_NAME, LAST_NAME, EMAIL, SIGNUP_DATE, COUNTRY)
VALUES
  (1, 'Ava', 'Mitchell', 'ava.mitchell@gmail.com', '2024-01-15', 'US'),
  (2, 'Liam', 'Patel', 'liam.patel@outlook.com', '2024-03-22', 'UK'),
  (3, 'Sofia', 'Andersson', 'sofia.andersson@yahoo.com', '2024-05-08', 'SE'),
  (4, 'Noah', 'Garcia', 'noah.garcia@hotmail.com', '2024-07-30', 'MX'),
  (5, 'Emma', 'Tanaka', 'emma.tanaka@icloud.com', '2024-09-12', 'JP');

-- Products (5 rows)
INSERT INTO RAW_PRODUCTS (PRODUCT_ID, PRODUCT_NAME, CATEGORY, PRICE, SUPPLIER)
VALUES
  (101, 'Wireless Noise-Cancelling Headphones', 'Electronics', 149.99, 'SoundWave Co.'),
  (102, 'Organic Cotton T-Shirt', 'Apparel', 34.95, 'GreenThread'),
  (103, 'Stainless Steel Water Bottle', 'Home & Kitchen', 24.50, 'HydroLife'),
  (104, 'Running Shoes Pro', 'Footwear', 119.00, 'StrideMax'),
  (105, 'Portable Bluetooth Speaker', 'Electronics', 79.99, 'SoundWave Co.');

-- Orders (8 rows)
INSERT INTO RAW_ORDERS (ORDER_ID, CUSTOMER_ID, ORDER_DATE, STATUS, TOTAL_AMOUNT)
VALUES
  (1001, 1, '2025-01-10 09:23:00', 'completed', 184.94),
  (1002, 2, '2025-01-15 14:05:00', 'completed', 149.99),
  (1003, 3, '2025-02-02 11:30:00', 'completed', 83.95),
  (1004, 1, '2025-02-18 16:45:00', 'shipped', 119.00),
  (1005, 4, '2025-03-05 08:12:00', 'completed', 254.48),
  (1006, 5, '2025-03-12 20:00:00', 'processing', 229.98),
  (1007, 2, '2025-03-20 13:37:00', 'cancelled', 34.95),
  (1008, 3, '2025-03-28 10:15:00', 'shipped', 73.50);

-- Order Items (12 rows)
INSERT INTO RAW_ORDER_ITEMS (ORDER_ITEM_ID, ORDER_ID, PRODUCT_ID, QUANTITY, UNIT_PRICE)
VALUES
  (1, 1001, 102, 1, 34.95),
  (2, 1001, 101, 1, 149.99),
  (3, 1002, 101, 1, 149.99),
  (4, 1003, 102, 1, 34.95),
  (5, 1003, 103, 2, 24.50),
  (6, 1004, 104, 1, 119.00),
  (7, 1005, 101, 1, 149.99),
  (8, 1005, 103, 1, 24.50),
  (9, 1005, 105, 1, 79.99),
  (10, 1006, 104, 1, 119.00),
  (11, 1006, 105, 1, 79.99),
  (12, 1008, 103, 3, 24.50);
