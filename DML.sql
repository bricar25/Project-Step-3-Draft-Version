-- These are some Database Manipulation queries for a partially implemented Project Website 
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.


-- ***** customers and editCustomers pages ***** 

-- get a list of customers for customers main page
select * from Customers; 

-- get a single customer's data for the Edit Customer Profile form
select customerID, first_name, last_name, email, password, phone_number from Customers 
where customerID = :customerID_selected_from_customers_page; 

-- *****  sellers and editSeller pages ***** 

-- get a list of sellers for sellers main page
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers;

-- get a single seller's data for the Edit Seller Profile form
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers
where sellerID = :sellerID_selected_from_sellers_page;

-- *****  CRMSelection, storeX_CRM, ?editCustomer? ***** 


-- ORDERS PAGES



-- PRODUCTS PAGES