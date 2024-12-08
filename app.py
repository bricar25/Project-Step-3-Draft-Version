from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
from datetime import datetime
import os

app = Flask(__name__)

# database connection info
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_sanromau"
app.config["MYSQL_PASSWORD"] = "7612"
app.config["MYSQL_DB"] = "cs340_sanromau"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

@app.route("/")
def home():
    return render_template("main.html")

#                 CUSTOMER SELLER RELATIONSHIP PAGES
# route for CRMSelection - let's user select the store to view store's CRM
@app.route("/CRMSelection")
def CRMSelection():
    if request.method == "GET":
        # query to grab all the store names from DB
        query = "select store_name from Sellers;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    return render_template("CRMSelection.j2", data = data)

# route for store's CRM - let's user view selected store's CRM
@app.route("/storeCRM/<store_name>")
def storeCRM(store_name):
    if request.method == "GET":

        # query to get data for Store's CRM
        query = """
                select 
                csrID, 
                first_name,
                last_name,
                CASE 
                    WHEN email_opt_out = 1 THEN 'Yes' 
                    WHEN email_opt_out = 0 THEN 'No' 
                END AS email_opt_out
                from Customer_Seller_Relationships 
                    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
                    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
                where Sellers.store_name = '%s';
                """ %(store_name)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("store_CRM.j2", data = data, store_name = store_name)

# let's user edit customer seller relationship. let's user change email opt out
@app.route("/editEmailOptOut/<store_name>/<int:csrID>", methods = ["POST", "GET"])
def editEmailOptOut(store_name, csrID):

    # GET - simply show the CSR
    if request.method == "GET":
        query = """
                select csrID, first_name, last_name, email_opt_out 
                from Customer_Seller_Relationships 
                    inner join Customers on Customer_Seller_Relationships.customerID = Customers.customerID
                    inner join Sellers on Customer_Seller_Relationships.sellerID = Sellers.sellerID
                where Sellers.store_name = %s and csrID = %s;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query, (store_name, csrID))
        data = cursor.fetchall()

        return render_template("editEmailOptOut.j2", data = data, csrID = csrID, store_name = store_name)
    
    # POST - update email opt out
    if request.method == "POST":
        if request.form.get("edit_opt_out"):
            email_opt_option = request.form.get('email_opt_out')

            query = """
                    update Customer_Seller_Relationships set
                        email_opt_out = %s
                    where csrID = %s;
                    """%(email_opt_option, csrID)
            
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query)
            mysql.connection.commit()

            return redirect("/storeCRM/%s" %(store_name))

# lists the customers so that a customer can be added to Store's CRM
@app.route("/listCustomers_CRM/<store_name>")
def listCustomers_CRM(store_name):
    if request.method == "GET":
        # query to grab all customers in db. 
        # To-Do: write the cury so that customers already in the crm are excluded
        query = """
                select customerID, first_name, last_name, email, password, phone_number 
                from Customers; 
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render customer page paassing our query data to the customers template
        return render_template("addCustomerToCRM_R2.j2", data = data, store_name = store_name)

# if user selects to ADD customer to CRM, this runs and commmits the appropriate query
@app.route("/addCustomerToCRM/<store_name>/<int:customerID>")
def addCustommerToCRM(store_name, customerID):
    query = """
            insert into Customer_Seller_Relationships (customerID, sellerID) 
            values (%s, (select sellerID from Sellers where store_name = '%s'));
            """%(customerID, store_name) 
    
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    return redirect("/storeCRM/%s"%(store_name))

# if user selects to DELETE customer from CRM, this runs and commits the appropriate query
@app.route("/deleteCustomerFromCRM/<store_name>/<int:csrID>")
def deleteCustomerFromCRM(store_name, csrID):
    query = """
            delete from Customer_Seller_Relationships
            where csrID = %s; 
            """%(csrID)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    return redirect("/storeCRM/%s"%(store_name))


#                           CUSTOMER PAGES
# ***** CUSTOMER'S C[R]UD *****
@app.route("/customers", methods=["POST", "GET"])
def customers():
    if request.method == "GET":
        # query to grab all customers in db. 
        query = """
                select customerID, first_name, last_name, email, password, phone_number 
                from Customers; 
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render customer page paassing our query data to the customers template
        return render_template("customers.j2", data = data)

# route for editCustomer page
# ***** CUSTOMER'S CR[U]D *****
@app.route("/editCustomer/<int:id>", methods = ["POST", "GET"])
def editCustomer(id):
    if request.method == "GET":
        # get customer's data to set as default values in editCustomer page
        query = "select * from Customers where customerID = %s" %(id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("editCustomer.j2", data = data)
    
    if request.method == "POST":
        if request.form.get("edit_customer"):
            # get user form inputs
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            phone_number = request.form["phone_number"]

            # build query
            query = """
                    update Customers set
                    first_name   = %s, 
                    last_name    = %s,
                    email        = %s,
                    password     = %s,
                    phone_number = %s
                    where customerID = %s;
                    """
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (first_name, last_name, email, password, phone_number, id))
            mysql.connection.commit()

            # once edit is made, go to customers page
            return redirect("/customers")

# addCustomer route
# ***** CUSTOMER'S [C]RUD *****
@app.route("/addCustomer", methods = ["POST", "GET"])
def addCustomer():
    if request.method == "GET":
        return render_template("addCustomer.j2")
    
    if request.method == "POST":
        if request.form.get("add_customer"):
            # get user form inputs
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            email = request.form["email"]
            password = request.form["password"]
            phone_number = request.form["phone_number"]

            # build query
            query = """
                    insert into Customers (first_name, last_name, email, password, phone_number)
                    values (%s, %s, %s, %s, %s);
                    """
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (first_name, last_name, email, password, phone_number))
            mysql.connection.commit()

            # once edit is made, go to customers page
            return redirect("/customers")

# delete customer
# ***** CUSTOMER'S CRU[D] *****
@app.route("/deleteCustomer/<int:id>")
def deleteCustomer(id):
    query = "delete from Customers where customerID = %s;" %(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    return redirect("/customers")

#                               SELLER PAGES
# route to sellers page 
# ***** SELLERS C[R]UD *****
@app.route("/sellers")
def sellers():
    if request.method == 'GET':
        # query to grab all sellers in DB
        query = """
                select sellerID, seller_first_name, seller_last_name, store_name, store_rating, follower_count 
                from Sellers;
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    return render_template("sellers.j2", data = data)

# route for editSeller page
# ***** SELLERS CR[U]D *****
@app.route("/editSeller/<int:id>", methods = ["POST", "GET"])
def editSeller(id):
    if request.method == "GET":
        query = "select * from Sellers where sellerID = %s;" %(id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("editSeller.j2", data = data)
    if request.method == "POST":
        if request.form.get("edit_seller"):
            # get form inputs
            seller_first_name = request.form["first_name"]
            seller_last_name  = request.form["last_name"]
            store_name        = request.form["store_name"]
            store_rating      = request.form["store_rating"]
            follower_count    = request.form["follower_count"]

            # build query
            query = """
                    update Sellers set
                        seller_first_name = %s,
                        seller_last_name  = %s,
                        store_name        = %s,
                        store_rating      = %s,
                        follower_count    = %s
                    where sellerID    = %s;
                    """
            
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (seller_first_name, seller_last_name, store_name, store_rating, follower_count, id))
            mysql.connection.commit()

            # redirect to sellers page to display seller with edit
            return redirect("/sellers")


# route for addSeller page
# ***** SELLERS [C]RUD *****
@app.route("/addSeller", methods = ["POST", "GET"])
def addSeller():
    if request.method == "GET":
        return render_template("addSeller.j2")
    if request.method == "POST":
        if request.form.get("add_seller"):
            # get form inputs
            seller_first_name = request.form["first_name"]
            seller_last_name  = request.form["last_name"]
            store_name        = request.form["store_name"]
            store_rating      = request.form["store_rating"]
            follower_count    = request.form["follower_count"]

            # build query
            query = """
                    insert into Sellers 
                    (seller_first_name, seller_last_name, store_name, store_rating, follower_count)
                    values (%s, %s, %s, %s, %s);
                    """
            
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (seller_first_name, seller_last_name, store_name, store_rating, follower_count))
            mysql.connection.commit()

            # redirect to sellers page to display seller with edit
            return redirect("/sellers")

# route to delete seller
# ***** SELLERS CRU[D] *****
@app.route("/deleteSeller/<int:id>")
def deleteSeller(id):
    query = "delete from Sellers where sellerID = %s;" %(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    return redirect("/sellers")


#                       PRODUCT PAGES
# route show all products
@app.route("/products", methods=["POST", "GET"])
def products():
    if request.method == "GET":
        # query to grab all customers in db. 
        query = """
                select productID, sellerID, category, brand, price, product_condition, color 
                from Products; 
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
        print(data)
        # render customer page paassing our query data to the customers template
        return render_template("products.html", data = data)

# route to edit products
@app.route("/editProduct/<int:id>", methods = ["POST", "GET"])
def editProduct(id):
    if request.method == "GET":
        # get customer's data to set as default values in editCustomer page
        query = "select * from Products where productID = %s" %(id)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("editProduct.j2", data = data)
    
    if request.method == "POST":
        print(f"if statement ok and product id = {id}")
        if request.form.get("edit_product"):
            print("second if statement ok")
            # get user form inputs
            productID = request.form["productID"]
            print(f'productID = {productID}')
            sellerID = request.form["sellerID"]
            print(f'sellerID = {sellerID}')
            category = request.form["category"]
            print(f'category = {category}')
            brand = request.form["brand"]
            print(f'brand = {brand}')
            price = request.form["price"]
            print(f'price = {price}')
            product_condition = request.form["product_condition"]
            print(f'condition = {product_condition}')
            color = request.form["color"]
            print(f'color = {color}')
            

            # build query
            query = """
                    update Products set
                    productID = %s, 
                    sellerID = %s,
                    category = %s,
                    brand  = %s,
                    price = %s,
                    product_condition = %s,
                    color = %s
                    where productID = %s;
                    """
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (productID, sellerID, category, brand, price, product_condition, color, id))
            mysql.connection.commit()
            # once edit is made, go to customers page
            return redirect("/products")

# addProducts route
# ***** Products [C]RUD *****
@app.route("/addProducts", methods = ["POST", "GET"])
def addProducts():
    if request.method == "GET":
        return render_template("addProducts.j2")
    
    if request.method == "POST":
        if request.form.get("add_products"):
            # get user form inputs
            productID = request.form["productID"]
            sellerID = request.form["sellerID"]
            category = request.form["category"]
            brand = request.form["brand"]
            price = request.form["price"]
            product_condition = request.form["product_condition"]
            color = request.form["color"]

            # build query
            query = """
                    insert into Products (productID, sellerID, category, brand, price, product_condition, color)
                    values (%s, %s, %s, %s, %s, %s, %s);
                    """
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (productID, sellerID, category, brand, price, product_condition, color))
            mysql.connection.commit()

            # once edit is made, go to customers page
            return redirect("/products")

# delete products
# ***** PRODUCTS'S CRU[D] *****
@app.route("/deleteProducts/<int:id>")
def deleteProducts(id):
    query = "delete from Products where productID = %s;" %(id)
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    return redirect("/products")


#                           ORDERS PAGES
# route to view all orders
@app.route("/viewOrders", methods=["POST", "GET"])
def viewOrders():
    if request.method == "GET":
        # query to grab orders
        query = """
                select * 
                from Orders; 
                """
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render 
        return render_template("viewOrders.j2", data = data)

# route to view specific order's line items and details
@app.route("/viewOrderDetails/<int:orderID>")
def viewOrderDetails(orderID):
    if request.method == "GET":
        
        # query to get order data
        query = """
                select 
                    orderID,
                    Orders.customerID,
                    first_name,
                    last_name,
                    order_date,
                    shipped,
                    total
                from Orders inner join Customers 
                on Orders.customerID = Customers.customerID
                where orderID = %s; 
                """ %(orderID)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        orderData = cursor.fetchall()

        # query to get line item data
        query2 = """
                select lineitemID, Orders.orderID, store_name, Line_Items.productID, sell_price, qty 
                from Orders inner join Line_Items on Orders.orderID = Line_Items.orderID
                inner join Products on Products.productID = Line_Items.productID
                inner join Sellers on Sellers.sellerID = Products.sellerID
                where Orders.orderID = %s
                order by lineitemID;
                """ %(orderID)
        
        cursor = mysql.connection.cursor()
        cursor.execute(query2)
        data = cursor.fetchall()

        return render_template("order_line_items.j2", data = data, orderID = orderID, orderData = orderData)

# route used to edit order total, order status, order date only (not line items)
@app.route("/editOrder/<int:orderID>", methods = ["POST", "GET"])
def editOrder(orderID):
    
    if request.method == "GET":
        # get specific order data
        query = "select * from Orders where orderID = %s" %(orderID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("editOrder.j2", data = data)
    
    if request.method == "POST":
        if request.form.get("edit_order"):
            # get user form inputs
            order_date = request.form["order_date"]
            order_status = request.form["order_status"]
            order_total = request.form["order_total"]

            # build query
            query = """
                    update Orders set
                    order_date   = %s, 
                    shipped = %s,
                    total  = %s
                    where orderID = %s;
                    """
            # submit and commit query to update specific order's details
            cursor = mysql.connection.cursor()
            cursor.execute(query, (order_date, order_status, order_total, orderID))
            mysql.connection.commit()

            # once edit is made, go to 
            return redirect("/viewOrders")

# this is to first select a customer to CREATE a new order
@app.route("/customerSelection")
def CustomerSelection():
    if request.method == "GET":
        # query to grab all the customer names from DB
        query = "select customerID, first_name, last_name from Customers;"
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()
    return render_template("customer_select_create_order.j2", data = data)

# this creates a Blank Order - once blank order is created, we can add line items and edit its data
@app.route("/createBlankOrder/<int:customerID>/", methods = ["POST", "GET"])
def createBlankOrder(customerID):

    # Get today's date
    today = datetime.today()

    # Format the date as YYYY-MM-DD
    format_date = today.strftime('%Y-%m-%d')

    # query to create blank order
    query = """
            insert into Orders (customerID, order_date, shipped, total)
            values (%s, '%s', 0, 0)
            """ %(customerID, format_date)
    # submit and commit query
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    # query to get the ID of the last order created
    query2 = "select LAST_INSERT_ID()"
    cursor = mysql.connection.cursor()
    cursor.execute(query2)
    orderID = cursor.fetchall()[0]['LAST_INSERT_ID()']
    
    # redirect to view all orders
    return redirect("/viewOrderDetails/%s"%(orderID))

# this is list all product (not already in order) so that user can select product to add to order
@app.route("/listProducts_addToOrder/<int:orderID>", methods = ["POST", "GET"])
def list_products(orderID):
    if request.method == "GET":
        # query to grab all products not already in order
        query = """
                SELECT 
                    Products.productID, 
                    store_name, 
                    category, 
                    brand, 
                    size, 
                    price, 
                    product_condition, 
                    color
                FROM Products
                INNER JOIN Sellers 
                    ON Products.sellerID = Sellers.sellerID
                WHERE Products.productID NOT IN (
                    SELECT productID 
                    FROM Line_Items 
                    WHERE orderID = %s);
                """%(orderID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        # render list of products to add to order
        return render_template("list_products_add_to_order.j2", data = data, orderID = orderID)

# this sends the command to add product to order once user hits the submit button to do so
@app.route("/addProductToOrder/<int:orderID>/<int:productID>")
def addProductToOrder(orderID, productID):
    query = """
            insert into Line_Items (orderID, productID, sell_price, qty) 
            values (%s, %s, (select price from Products where productID = %s), 1);
            """%(orderID, productID, productID) 
    
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    mysql.connection.commit()

    # redirect to view order details
    return redirect("/viewOrderDetails/%s"%(orderID))

# once line items are added to order, we need to update the order total 
# we can do it, manually or press a button to do so
@app.route("/updateOrderTotal/<int:orderID>")
def updateOrderTotal(orderID):
    # build query to get all order line_items
    query = """
            select lineitemID, sell_price, qty 
            from Line_Items 
            where orderID = %s
            order by lineitemID;
            """ %(orderID)
        
    cursor = mysql.connection.cursor()
    cursor.execute(query)
    data = cursor.fetchall()

    # calculate total, iterate through line items
    new_total = 0
    sales_tax_rate = 8.1/100
    if data:
        for item in data: 
            new_total += float(item['sell_price']) * float(item['qty'])
        new_total = new_total * (1+sales_tax_rate)
    
    # query to update total
    query2 = """
                update Orders 
                set total  = %s
                where orderID = %s;
             """ %(new_total, orderID)

    cursor = mysql.connection.cursor()
    cursor.execute(query2)
    mysql.connection.commit()

    # redirect to order
    return redirect("/viewOrderDetails/%s"%(orderID))

# route to edit line item of order
@app.route("/edit_line_item/<int:orderID>/<int:itemID>", methods = ["POST", "GET"])
def edit_line_item(orderID, itemID):
    if request.method == "GET":
        # get line_item data
        query = "select * from Line_Items where orderID = %s and lineitemID = %s" %(orderID, itemID)
        cursor = mysql.connection.cursor()
        cursor.execute(query)
        data = cursor.fetchall()

        return render_template("edit_line_item.j2", orderID = orderID, data = data)
    
    if request.method == "POST":
        if request.form.get("edit_line_item"):
            # get user form inputs
            line_item_sell_price = request.form["line_item_sell_price"]
            line_item_qty        = request.form["line_item_qty"]


            # build query to update line item data with inputs from user
            query = """
                    update Line_Items set
                    sell_price   = %s, 
                    qty = %s
                    where lineitemID = %s;
                    """
            # submit and commit query
            cursor = mysql.connection.cursor()
            cursor.execute(query, (line_item_sell_price, line_item_qty, itemID))
            mysql.connection.commit()

            # once edit is made, go back to Order details
            return redirect("/viewOrderDetails/%s" %(orderID))





# Listener
if __name__ == "__main__":
    app.run(port=8013, debug=True)