 select * from Orders where orderID = 1;


 select 
    orderID,
    Orders.customerID,
    first_name,
    last_name,
    order_date,
    shipped,
    total
from Orders inner join Customers on Orders.customerID = Customers.customerID
where orderID = 1;
