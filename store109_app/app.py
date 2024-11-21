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
    return render_template("index2.html")

# route for customer's page
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
@app.route("/editCustomer/<int:id>", methods = ["POST", "GET"])
def editCustomer(id):
    if request.method == "GET":
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





# Listener
if __name__ == "__main__":
    app.run(port=8011, debug=True)