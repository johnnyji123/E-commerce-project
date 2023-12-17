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


products = [
        ("Marco 1/4 resin", 360, 1),
        ("Aokiji 1/6 resin", 440, 1),
        ("Blackbeard sd resin", 280, 1)
    
    ]



    
@app.route("/")
def products_page():
    return render_template("products.html")


#if __name__ == ("__main__"):
   # app.run(debug= True, use_reloader = False)