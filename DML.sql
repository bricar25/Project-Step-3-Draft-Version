-- These are some Database Manipulation queries for a partially implemented Project Website 
-- Your submission should contain ALL the queries required to implement ALL the
-- functionalities listed in the Project Specs.


-- ***** ***** ***** ***** customers and editCustomers pages ***** ***** ***** *****
-- get a list of customers for customers main page
select * from Customers; 

-- get a single customer's data for the Edit Customer Profile form
select customerID, first_name, last_name, email, password, phone_number from Customers 
where customerID = :customerID_selected_from_customers_page; 

-- ***** ***** ***** *****  sellers and editSeller pages ***** ***** ***** *****
-- get a list of sellers for sellers main page
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers;

-- get a single seller's data for the Edit Seller Profile form
select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count from Sellers
where sellerID = :sellerID_selected_from_sellers_page;

-- *****  ***** ***** ***** CRMSelection, storeX_CRM, ?editCustomer? ***** ***** ***** *****
-- for store dropdown on CRMSelection
select store_name from Sellers;

-- get customers after user selects which CRM (which seller's CRM) to view
select first_name, last_name from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection;

-- ***** ***** ***** ***** ORDERS PAGES ***** ***** ***** *****



-- ***** ***** ***** ***** PRODUCTS PAGES ***** ***** ***** *****