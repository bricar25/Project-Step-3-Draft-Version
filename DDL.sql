-- CREATE TABLES

-- create Customers table
CREATE OR REPLACE TABLE Customers (
    customerID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    first_name VARCHAR(32) NOT NULL,
    last_name VARCHAR(32) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(50) NOT NULL,  
    phone_number VARCHAR(12)
);

-- create Sellers table
CREATE OR REPLACE TABLE Sellers (
    sellerID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    seller_first_name VARCHAR(32) NOT NULL,
    seller_last_name VARCHAR(32) NOT NULL,
    store_name VARCHAR(32) NOT NULL,
    store_rating DECIMAL(3,1),
    follower_count INT
);

-- create Products table
CREATE OR REPLACE TABLE Products (
    productID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    sellerID INT NOT NULL, 
    category VARCHAR(32) NOT NULL,
    brand VARCHAR(32),
    size VARCHAR(32),
    price DECIMAL(6,2) NOT NULL,
    product_condition VARCHAR(32) NOT NULL,
    color VARCHAR(32),
    FOREIGN KEY (sellerID) REFERENCES Sellers(sellerID)
);

-- create Orders table
CREATE OR REPLACE TABLE Orders (
    orderID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    customerID INT NOT NULL,
    order_date DATE NOT NULL,
    shipped BOOLEAN DEFAULT FALSE,
    total DECIMAL(6,2) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID)
);

-- create Customer_Seller_Relationships table. intersection table between Customers and Sellers
CREATE OR REPLACE TABLE Customer_Seller_Relationships (
    csrID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    customerID INT NOT NULL,
    sellerID INT NOT NULL,
    email_opt_out BOOLEAN DEFAULT TRUE,
    FOREIGN KEY (customerID) REFERENCES Customers(customerID),
    FOREIGN KEY (sellerID) REFERENCES Sellers(sellerID)
);

-- create Line_Items table. intersection table between Orders and Products
CREATE OR REPLACE TABLE Line_Items (
    lineitemID INT AUTO_INCREMENT NOT NULL PRIMARY KEY,
    orderID INT NOT NULL,
    productID INT NOT NULL,
    sell_price DECIMAL(6,2) NOT NULL,
    qty INT NOT NULL,
    UNIQUE (orderID, productID),  
    FOREIGN KEY (orderID) REFERENCES Orders(orderID),
    FOREIGN KEY (productID) REFERENCES Products(productID)
);

-- insert sample data into Customers table
INSERT INTO Customers (first_name, last_name, email, password, phone_number) VALUES
('Jamie', 'Dillan', 'jdill@yahoo.com', '123pasS!', '223-505-1234'),
('Jane', 'Smith', 'janesmith@yahoo.com', 'Pass!word2', '425-505-6678'),
('Alice', 'James', 'alicej@gmail.com', '2p0a2s4s?', '334-758-8765'),
('Bobby', 'Wilde', 'bwilde@gmail.com', 'beWure!', '202-577-4321');

-- insert sample data into Sellers table
INSERT INTO Sellers (seller_first_name, seller_last_name, store_name, store_rating, follower_count) VALUES
('Pam', 'Brell', 'Winner Tech Shop', 2.8, 1023),
('Jon', 'Wimber', 'Wimber Wear', 4.5, 850),
('Ella', 'Garcia', 'Crate and Home', 4.9, 670),
('Sonny', 'Smith', 'Son Shades', 3.7, 1540);


-- insert sample data in Products table
INSERT INTO Products (sellerID, category, brand, size, price, product_condition, color) VALUES
(1, 'Shirts', 'Adidas', 'Medium', 119.99, 'New', 'Black'),
(2, 'Pants', 'Nike', 'Large', 49.99, 'New', 'Red'),
(3, 'Pants', 'Arizona', 'Large', 19.99, 'Used', 'White'),
(4, 'Accessories', 'Eddie Bauer', 'Small', 15.99, 'Used', 'Blue');

-- insert sample data in Orders table
INSERT INTO Orders (customerID, order_date, shipped, total) VALUES
(1, '2023-08-06', TRUE, 259.18),
(2, '2022-11-03', TRUE, 161.97),
(3, '2021-10-01', TRUE, 86.36),
(4, '2024-11-07', FALSE, 86.35);

-- insert sample data in CSR table
INSERT INTO Customer_Seller_Relationships (customerID, sellerID) VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4);

-- insert sample data in Line_Items table
INSERT INTO Line_Items (orderID, productID, sell_price, qty) VALUES
(1, 1, 119.99, 2),
(2, 2, 49.99, 3),
(3, 3, 19.99, 4),
(4, 4, 15.99, 5);


