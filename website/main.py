import sys
from flask import Flask, render_template, redirect , request
from pymongo import MongoClient
#set up actually good PYTHONPATH
#sys.path.insert(1, "G://app-dev//app-dev")
from api.structures.User import User
from api.structures.billinghistory import Billinghistory
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

@app.route("/billing_crud", methods=["GET", "POST"])
def billing_crud():
    html = "billing_crud.html"

    if request.method == "POST":
        match request.form["submit"]:
            case "create_bill":
                bill = Billinghistory({
                    "customerid": request.form["customer_id"],
                    "billid": db.generate_id(),
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

if __name__ == "__main__":
    app.run(debug=True)
