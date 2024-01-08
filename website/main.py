import sys
import uuid

from flask import Flask, render_template, redirect , request
from pymongo import MongoClient
#set up actually good PYTHONPATH
#sys.path.insert(1, "G://app-dev//app-dev")
from api.structures.User import User
from api.structures.billinghistory import Billinghistory
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


@app.route("/billing_crud", methods=["GET", "POST"])
def billing_crud():
    html = "billing_crud.html"

    if request.method == "POST":
        match request.form["submit"]:
            case "create_bill":
                bill = Billinghistory({
                    "customerid": request.form["customer_id"],
                    "billid": str(uuid.uuid4()),
                    "status": False
                })
                db.create_bill(bill)
                return render_template(html, created_bill=str(dict(bill)))

            case "find_bill":
                bill_id = request.form["bill_id"]
                result = db.get_bill_by_id(bill_id)
                if result is None:
                    return render_template(html, found_bill=f"Bill with id {bill_id} not found")

                return render_template(html, found_bill=str(dict(result)))

            case "update_bill":
                bill_id = request.form.get("bill_id")
                customer_id = request.form.get("customer_id")
                status = request.form.get("bill_status") == "payed"

                bill = Billinghistory({
                    "billid": bill_id,
                    "customerid": customer_id,
                    "status": status
                })

                result = db.update_bill(bill)
                return render_template(html, updated_bill=str(result))

            case "delete_bill":
                bill_id = request.form.get("bill_id")

                result = db.delete_bill_by_id(bill_id)
                return render_template(html, deleted_bill=f"Deleted bill with id {bill_id}" if result else f"No bill with id {bill_id} found")

            case _:
                return "<body>invalid submit button pressed<br>somehow pressed button that doesnt exist</body>"

    else:
        return render_template(html)

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
