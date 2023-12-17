import mysql.connector
from flask import Flask, render_template
from flask import request


db = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "projects123123",
    database = "Ecommerce_db"
    
    )

cursor = db.cursor()


# table products


values = [
        ("Marco resin 1/4", 380,  1),
        ("Aokji resin 1/6", 420, 1),
        ("Blackebeard resin sd", 260, 1)
    ]


app = Flask(__name__)

@app.route("/")
def products_page():
    return render_template("products.html")


if __name__ == ("__main__"):
    app.run(debug= True, use_reloader = False)