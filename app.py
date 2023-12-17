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

lst = []

for x in range(3):
    random_id = "".join(random.choices(string.ascii_uppercase, k = 6))
    lst.append(random_id)
    
values = [
        (lst[0], ),
        (lst[1], ),
        (lst[2], )
        
    ]
    
    
add = "INSERT INTO products (product_id) VALUES (%s)"
cursor.executemany(add, values)
db.commit()

@app.route("/")
def products_page():
    return render_template("products.html")


#if __name__ == ("__main__"):
   # app.run(debug= True, use_reloader = False)