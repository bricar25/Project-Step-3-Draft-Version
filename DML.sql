-- These are some Database Manipulation queries for a partially implemented Project Website 
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.



-- ***** ***** ***** ***** ***** customers and editCustomers pages ***** ***** ***** ***** *****
-- get a list of customers for customers main page
select customerID, first_name, last_name, email, password, phone_number from Customers; 

-- get a single customer's data for the Edit Customer Profile form
select customerID, first_name, last_name, email, password, phone_number from Customers 
where customerID = :customerID_selected_from_customers_page; 

-- update customer 
update Customers set 
    first_name   = :first_name_input, 
    last_name    = :last_name_input,
    email        = :email_input,
    password     = :password_input,
    phone_number = :phone_number_input
where customerID = :customerID_selected_from_customers_page;

-- add a new customer profile
insert into Customers (first_name, last_name, email, password, phone_number)
values (:first_name_input, :last_name_input, :email_input, :password_input, :phone_number_input);

-- delete customer profile
delete from Customers where customerID = :customerID_selected_from_customers_page;


-- ***** ***** ***** ***** ***** sellers and editSeller pages ***** ***** ***** ***** *****
-- get a list of sellers for sellers main page
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers;

-- get a single seller's data for the Edit Seller Profile form
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers
where sellerID = :sellerID_selected_from_sellers_page;

-- update seller
update Sellers set
    seller_first_name = :seller_first_name_input,
    seller_last_name  = :seller_first_name_input,
    store_name        = :store_name_input,
    store_rating      = :store_rating_input,
    follower_count    = :follower_count_input
where sellerID = :sellerID_selected_from_sellers_page;

-- add a new seller profile
insert into Sellers (seller_first_name, seller_last_name, store_name, store_rating, follower_count)
values (:seller_first_name_input, :seller_last_name_input, :store_name_input, :store_rating_input, :follower_count_input);

-- delete seller profile
delete from Sellers where sellerID = :sellerID_selected_from_sellers_page;


--  ***** ***** ***** ***** ***** CRMSelection, storeX_CRM, ?editCustomer? ***** ***** ***** ***** *****
-- for store dropdown on CRMSelection
select store_name from Sellers;

-- get customers after user selects which CRM (which seller's CRM) to view
select Customers.customerID, first_name, last_name, email_opt_out from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection;

-- get a single CSR data for the Edit Seller Profile form
select first_name, last_name, email_opt_out from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection and Customers.customerID = :customerID_selected_from_CRM;

-- update store's CRM by updating 
update Customer_Seller_Relationships set
    email_opt_out = :email_opt_out_input
where csrID = (
    select csrID from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection and Customers.customerID = :customerID_selected_from_CRM);

-- delete customer tracking from store's CRM 
delete from Customer_Seller_Relationships 
where csrID = (
    select csrID from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection and Customers.customerID = :customerID_selected_from_CRM
);

-- add customer to store's CRM
insert into Customer_Seller_Relationships (customerID, sellerID) values
(:customerID_selected, :sellerID_of_store_CRM);

--  ***** ***** ***** ***** ***** ORDERS PAGES ***** ***** ***** ***** *****
-- get a list of orders for the orders main page
select orderID, customerID, order_date, shipped, total from Orders;

-- get a single order's data for the Edit Order page
select orderID, customerID, order_date, shipped, total from Orders
where orderID = :orderID_selected_from_orders_page;

-- update order information
update Orders set
    customerID = :customerID_input,
    order_date = :order_date_input,
    shipped    = :shipped_input,
    total      = :total_input
where orderID = :orderID_selected_from_orders_page;

-- add a new order
insert into Orders (customerID, order_date, shipped, total)
values (:customerID_input, :order_date_input, :shipped_input, :total_input);

-- delete an order
delete from Orders where orderID = :orderID_selected_from_orders_page;

--  ***** ***** ***** ***** ***** PRODUCTS PAGES ***** ***** ***** ***** *****
-- get a list of products for the products main page
select productID, sellerID, category, brand, size, price, product_condition, color from Products;

-- get a single product's data for the Edit Product page
select productID, sellerID, category, brand, size, price, product_condition, color from Products
where productID = :productID_selected_from_products_page;

-- update product information
update Products set
    sellerID          = :sellerID_input,
    category          = :category_input,
    brand             = :brand_input,
    size              = :size_input,
    price             = :price_input,
    product_condition = :product_condition_input,
    color             = :color_input
where productID = :productID_selected_from_products_page;

-- add a new product
insert into Products (sellerID, category, brand, size, price, product_condition, color)
values (:sellerID_input, :category_input, :brand_input, :size_input, :price_input, :product_condition_input, :color_input);

-- delete a product
delete from Products where productID = :productID_selected_from_products_page;

--  ***** ***** ***** ***** ***** LINE ITEMS PAGES ***** ***** ***** ***** *****
-- get a list of line items for a specific order on the line items page
select lineitemID, orderID, productID, sell_price, qty from Line_Items
where orderID = :orderID_selected_from_orders_page;

-- get a single line item data for editing
select lineitemID, orderID, productID, sell_price, qty from Line_Items
where lineitemID = :lineitemID_selected_from_line_items;

-- update line item information
update Line_Items set
    orderID    = :orderID_input,
    productID  = :productID_input,
    sell_price = :sell_price_input,
    qty        = :qty_input
where lineitemID = :lineitemID_selected_from_line_items;

-- add a new line item
insert into Line_Items (orderID, productID, sell_price, qty)
values (:orderID_input, :productID_input, :sell_price_input, :qty_input);

-- delete a line item
delete from Line_Items where lineitemID = :lineitemID_selected_from_line_items;
