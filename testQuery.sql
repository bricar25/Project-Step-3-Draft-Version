select * from Customers;

select * from Customer_Seller_Relationships
where sellerID = (select sellerID from Sellers where store_name = 'Son Shades');



