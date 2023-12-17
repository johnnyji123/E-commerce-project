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


