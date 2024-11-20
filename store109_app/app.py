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
    return redirect("/customers")

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
    



# Listener
if __name__ == "__main__":
    app.run(port=8012, debug=True)