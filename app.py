import mysql.connector
from flask import Flask, render_template
from flask import request
import random
import string

db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "projects123123",
    database = "Ecommerce_db"
    
    )

cursor = db.cursor()


# table products

    
app = Flask(__name__)


@app.route("/")
def products_page():
    cursor.execute("SELECT * FROM products")
    
    col_names_list = []
    product_list = []
    
    col_names = cursor.description
    for x in col_names:
        col_names_list.append(x[0])

    all_rows = cursor.fetchall()    
    for row in all_rows:
        my_dict = {}
        for col_name, value in zip(col_names_list, row):
            my_dict[col_name] = value
            product_list.append(my_dict)
    
    return render_template("products.html", product_list = product_list)



    
if __name__ == ("__main__"):
    app.run(debug= True, use_reloader = False)