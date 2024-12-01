update Customer_Seller_Relationships set
    email_opt_out = FALSE
where csrID = (
    select csrID from Customer_Seller_Relationships 
    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
    where Sellers.store_name = 'Son Shades' and Customers.customerID = 4);