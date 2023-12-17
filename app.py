import mysql.connector
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
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
# table cart

    
app = Flask(__name__)


@app.route("/")
def products_page():
    cursor.execute("SELECT * FROM products")
    
    col_names_list = []
    product_list = []
    product_list_duplicates_removed = []
    
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


@app.route("/<product_id>", methods = ["GET", "POST"])
def add_to_cart(product_id):
    if request.method == "POST":
        
        cursor.execute("SELECT * FROM products WHERE product_id = %s", 
                       (product_id, ))
        
        product_information = cursor.fetchall() 
        # convert tuple to dictionary
        col_names = [name [0] for name in cursor.description]
        to_dict = []
        for row in product_information:
            my_dict = {}
            for col_name, value in zip(col_names, row):
                my_dict[col_name] = value
                
            to_dict.append(my_dict) 
                
        
     
        for row in to_dict:
            cursor.execute("INSERT INTO cart (product_id, name, price, quantity) VALUES (%s, %s, %s, %s)",
                           (row['product_id'], row['name'], row['price'], row['quantity']))
            
            db.commit()
                    
                
        return redirect(url_for('products_page'))
        

@app.route("/cart", methods = ["GET", "POST"])
def view_cart():
    return render_template("cart.html")
    

                
if __name__ == ("__main__"):
    app.run(debug= True, use_reloader = False)