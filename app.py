from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
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

# Customer Seller Relationships Pages
# To-Do: CRUD not implemented; only proof of concept
@app.route("/CRMSelection")
def CRMSelection():
    return render_template("CRMSelection.html")

@app.route("/storeCRM")
def storeCRM():
    return render_template("store1_CRM.html")

@app.route("/editEmailOptOut")
def editStoreCRM():
    return render_template("editCSR.html")

@app.route("/addCustomerToCRM")
def addCustomerToCRM():
    return render_template("addCustomerToCRM.html")


# Customer Pages
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


# PRODUCT LISTINGS PAGES
@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/editProducts")
def editProducts():
    return render_template("editproducts.html")

# ORDERS PAGES
@app.route("/orders")
def orders():
    return render_template("orders.html")

@app.route("/editorder")
def editorder():
    return render_template("editorder.html")

# LINE ITEMS PAGES
@app.route("/lineitems")
def lineitems():
    return render_template("lineitems.html")

@app.route("/editlineitems")
def editlineitems():
    return render_template("editlineitems.html")


# Listener
if __name__ == "__main__":
    app.run(port=8012, debug=True)