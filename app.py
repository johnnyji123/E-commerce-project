import mysql.connector
from flask import Flask, render_template
from flask import request
from flask import redirect, url_for
import random
import string
from flask import flash

# Connecting to database
db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "password",
    database = "Ecommerce_db"  
    )

# Creating a cursor object
cursor = db.cursor()


# table products
# table cart
# table checkout

# Initialising Flask    
app = Flask(__name__)
# Secret Key for flash messaging
app.secret_key = "123123123"


# Endpoint for products - renders all products from database
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


# Endpoint for cart - gets all the information of a product when you add it to cart. 
# The item details are simultaneously inserted into the cart table
@app.route("/<product_id>", methods = ["GET", "POST"])
def add_to_cart(product_id):
    if request.method == "POST":
        
        cursor.execute("SELECT * FROM products WHERE product_id = %s", 
                       (product_id, ))
        
        product_information = cursor.fetchall() 
            
        for row in product_information:
            cursor.execute("INSERT INTO cart (product_id, name, price, quantity) VALUES (%s, %s, %s, %s)",
                           (row[0], row[1], row[2], row[3]))
            
            db.commit()
            
        return redirect(url_for('products_page'))
        

# Endpoint to view the list of items added to cart
@app.route("/cart", methods = ["GET", "POST"])
def view_cart():
    
    cursor.execute("SELECT COUNT(*) FROM cart")
    for x in cursor:
        if x[0] == 0:
            flash("Your cart is empty !")
            return render_template("cart.html")
        
        else:
            cursor.execute("SELECT * FROM cart")
            all_rows = cursor.fetchall()
            
            col_names = [name[0] for name in cursor.description]
            product_list_cart = []
            
            for row in all_rows:
                product_dict = {}
                
                for col_name, value in zip(col_names, row):
                    product_dict[col_name] = value
                product_list_cart.append(product_dict)
                
            cursor.execute("SELECT SUM(total_price) FROM cart")
            total = cursor.fetchall()
            extract_total = [int(num[0]) for num in total]
            extract_total_from_list = extract_total[0]
            
            return render_template("cart.html", products_in_cart = product_list_cart, total_price = extract_total_from_list)
        
  

# Endpoint that allows you to delete items in cart
@app.route("/delete_item/<product_id>" , methods = ["GET", "POST"])
def delete_item(product_id):
    if request.method == "POST":
        cursor.execute("DELETE FROM cart WHERE product_id = %s",
                       (product_id, ))
        
        db.commit() 

        return redirect(url_for('view_cart'))
    
    
# Endpoint that allows you to add items to cart
@app.route("/add_quantity/<product_id>", methods = ["GET", "POST"])
def add_item(product_id):
    cursor.execute("UPDATE cart SET quantity = (quantity + 1), total_price = (price * quantity) WHERE product_id = %s",
                   (product_id, ))
    
    db.commit()
                
    return redirect(url_for('view_cart'))
    

# Endpoint that allows you to reduce quantity of items in cart
@app.route("/remove_quantity/<product_id>", methods = ["GET", "POST"])
def remove_item(product_id):
    cursor.execute("UPDATE cart SET quantity = (quantity - 1), total_price = (price * quantity) WHERE product_id = %s",
                   (product_id, ))
    
    db.commit()
    
    return redirect(url_for('view_cart'))


# Endpoint to checkout page
@app.route("/checkout", methods = ["POST", "GET"])
def checkout():
    if request.method == "POST":
        
        name = request.form.get("name")
        email = request.form.get("email")
        address = request.form.get("address")
        card_details = request.form.get("card_details")
        
        cursor.execute("INSERT INTO checkout (name, email, address, card_details) VALUES (%s, %s,%s, %s)",
                       (name, email, address, card_details))
        
        db.commit()
        return render_template("checkout.html")
    
    return render_template("checkout.html")


    
if __name__ == ("__main__"):
    app.run(debug= True, use_reloader = False)  