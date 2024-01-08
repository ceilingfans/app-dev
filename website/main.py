import sys
from flask import Flask, render_template, redirect , request
from pymongo import MongoClient
#set up actually good PYTHONPATH
#sys.path.insert(1, "G://app-dev//app-dev")
from api.structures.User import User
from api.db.driver import Driver
from api.structures.datavalidation import UserForm



db = Driver()
app = Flask(__name__)
app.config.update(dict(SECRET_KEY='yoursecretkey'))


@app.route("/")
def index():
    return render_template("home.html")

@app.route("/contact")
def page():
    return render_template("contact.html")

@app.route("/CRUDUSER",methods=['GET','POST'])
def cruduser():
    userform = UserForm()
    if request.method == 'POST':
        if request.form['submit'] == 'CreateUser':
            if userform.validate_on_submit() == False:
                return render_template("CRUDUSER.html", form=userform, Status=userform.errors)
            else:
                user = User({
                "name": userform.name.data,
                "password": userform.password.data,
                "id": db.generate_id(),
                "email": userform.email.data,
                "address": userform.address.data,
                })
                db.create_user(user)
                if userform.errors == {}:
                    return render_template("CRUDUSER.html", form=userform, Status="User Created")
        if request.form['submit'] == 'GetUser':
            return render_template("CRUDUSER.html", form=userform, Userdata=db.get_user_by_id(request.form['id']))
        if request.form['submit'] == 'UpdateUser':
            new_user = User({
            "name": request.form['upname'],
            "password": request.form['uppassword'],
            "id": request.form['upid'],
            "email": request.form['upemail'],
            "address": request.form['upaddress'],
            })
            return render_template("CRUDUSER.html", form=userform, Updated=db.update_user(new_user))
        if request.form['submit'] == 'DelUser':
            return render_template("CRUDUSER.html", form=userform, Deleted=db.delete_user_by_id(request.form['delid']))
    return render_template("CRUDUSER.html", form=userform, Status="User Not Created")

if __name__ == "__main__":
    app.run(debug=True)
