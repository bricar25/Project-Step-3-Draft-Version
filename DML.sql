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
    follower_count    = :follower_count_input,
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
select first_name, last_name from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = :store_selected_from_CRMSelection;

-- get a single CSR data for the Edit Seller Profile form

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


--  ***** ***** ***** ***** ***** ORDERS PAGES ***** ***** ***** ***** *****



--  ***** ***** ***** ***** ***** PRODUCTS PAGES ***** ***** ***** ***** *****