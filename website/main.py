import sys
from flask import Flask, render_template, redirect , request
from pymongo import MongoClient
#set up actually good PYTHONPATH
#sys.path.insert(1, "G://app-dev//app-dev")
from api.structures.User import User
from api.db.driver import Driver
db = Driver()
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/contact")
def page():
    return render_template("contact.html")


@app.route("/CRUDTEST",methods=['GET','POST'])
def crudtest():
    if request.method == "POST":
        if request.form['submit'] == 'CreateUser':
            user = User({
            "name": request.form['name'],
            "password": request.form['password'],
            "id": Driver.generate_id(),
            "email": request.form['email'],
            "address": request.form['address'],
            })  
            db.create_user(user)
            return render_template("CRUDTEST.html")
        if request.form['submit'] == 'GetUser':
            return render_template("CRUDTEST.html",Userdata = db.get_user_by_id(request.form['id']))
        if request.form['submit'] == 'UpdateUser':
            new_user = User({
            "name": request.form['upname'],
            "password": request.form['uppassword'],
            "id": request.form['upid'],
            "email": request.form['upemail'],
            "address": request.form['upaddress'],
            })
            return render_template("CRUDTEST.html",Updated = db.update_user(new_user))
        if request.form['submit'] == 'DelUser':
            return render_template("CRUDTEST.html",Deleted = db.delete_user_by_id(request.form['delid']))
    else:
        return render_template("CRUDTEST.html")

if __name__ == "__main__":
    app.run(debug=True)
