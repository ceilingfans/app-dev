import sys
from flask import Flask, render_template, redirect
from pymongo import MongoClient
#set up actually good PYTHONPATH
sys.path.insert(1, "C://Users//Isaac//Desktop//app-dev//app-dev//api")
from getdatabase import *
from structures.User import *

app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))

dbcol = DatabaseCollection("Database","Users")
db = dbcol.get_database()

@app.route("/<name>")
def index(name):
    return render_template("home.html", name = name)


def createUser(form):
    return

if __name__ == "__main__":
    app.run(debug=True)
