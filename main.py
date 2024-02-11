from flask import Flask, render_template, request, redirect, url_for, jsonify, abort
from argon2.exceptions import VerifyMismatchError
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import os
import sys
import random
import string
from uuid import uuid4
from werkzeug.utils import secure_filename
from dhooks import Webhook
from PIL import Image
import json

from flask_uploads import UploadSet, configure_uploads, IMAGES
from flask_login import AnonymousUserMixin

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.db.driver import Driver
from api.structures.User import check_hash, User, get_hash
from api.structures.Promo import Promo
from api.Insuranceprice.getprice import getprice
from api.structures.Bill import Bill
from api.structures.datavalidation import *

db = Driver()
app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
app.config["UPLOADED_PHOTOS_DEST"] = os.path.join(app.root_path, "static", "images", "userprofileimg")
login_manager = LoginManager()
login_manager.init_app(app) 
profile_pics = UploadSet("photos", IMAGES)
configure_uploads(app, profile_pics)


@app.context_processor
def base():
    searchform = SearchForm()
    if searchform.submit_search.data and searchform.validate():
        return redirect(url_for("search"))
    return dict(searchform=searchform)


@login_manager.user_loader
def user_loader(id):
    ret_code, user = db.users.find(user_id=id)
    match ret_code:
        case "USERNOTFOUND":
            return

        case "SUCCESS":
            return user

        case _:
            return


@login_manager.request_loader
def request_loader(request):
    print("info: request_loader")
    email = request.form.get("email")
    ret_code, user = db.users.find(email=email)
    match ret_code:
        case "USERNOTFOUND":
            return

        case "SUCCESS":
            return user

        case _:
            return


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    search = request.args.get('search')
    search = search.lower()
    # the keys are the html files, the values are the words that will trigger the search
    html_files = {"contact": ["contact", "contact-us", "email"],
                  "insurance": ["insurance", "coverage", "products", "quote", "price", "cost", "estimate", "calculate",
                                "calc"],
                  "login": ["login", "signin", "sign-in", "sign in"],
                  "repair": ["repair", "fix"],
                  "shop": ["shop", "phone", "samsung", "iphone", "products", "oppo"],
                  "signup": ["signup", "create", "account", "make", "register", "sign-up", "sign"],
                  "wheel": ["wheel", "spin", "prize", "win"],
                  "home": ["home", "main", "index", "website", "site", "page"],
                  "profile": ["profile", "account", "me", "user", "settings", "preferences", "password"]
                  }
    results = []
    # Ignore the O(n^2) complexity, it's only 7 items
    for search in search.split(" "):
        for key, desc in html_files.items():
            for word in desc:
                if search == word:
                    results.append(key)
    return render_template("search.html", search=search, results=results)


@app.route("/contact", methods=["GET", "POST"])
def contact():
    hook = Webhook(
        "https://discord.com/api/webhooks/1198939240235532358/Gu5Dw7cmkupwqo9yg-PgdSKXlj1toWbCHsSqQUabIJc-A3dOlHfDdVkkqwurh34wXdaR")
    contactform = ContactUs()
    if contactform.submit_contact.data and contactform.validate():
        print("info: contact form submitted")
        hook.send(
            f"Name: {contactform.name.data}\nEmail: {contactform.email.data}\nPhone Number: {contactform.phone_number.data}\nMessage: {contactform.message.data}")
        return render_template("contact.html", form=contactform, result="Your message has been sent")
    return render_template("contact.html", form=contactform)


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/payment", methods=["GET", "POST"])
@login_required
def payment():
    try:
        cart = request.args.get('cart')
        cart = json.loads(cart)
    except:
        abort(404)

    userid = current_user.get_id()
    ret_code, bills = db.bills.find(owner_id=userid)

    total = sum(item[1] for item in cart.values())
    cnt = 0

    if ret_code != "BILLNOTFOUND":
        for bill in bills:
            if not bill.get_status():
                bill_price = round(bill.get_price(), 2)
                total += bill_price
                cnt += 1
                cart[f"Plan Quote {cnt}"] = ['1', bill_price]

    return render_template("payment.html", cart=cart, total=round(total, 2))


@app.route("/insurance", methods=["GET", "POST"])
@login_required
def insurance():
    insuranceform = InsuranceForm()
    if insuranceform.submit_insure.data and insuranceform.validate():
        if insuranceform.user_phone_price.data < 700:
            phoneprice = 1
        else:
            phoneprice = 0
        data = [insuranceform.user_age.data, insuranceform.user_gender.data, insuranceform.user_job.data,
                insuranceform.user_sports.data, insuranceform.user_education.data, insuranceform.user_vacations.data,
                phoneprice]
        if insuranceform.user_plan.data == "1":
            price = 50
        elif insuranceform.user_plan.data == "2":
            price = 100
        elif insuranceform.user_plan.data == "3":
            price = 150
        # calculate price using the model
        insureprice = getprice(data, price)
        bill = Bill({
            "customer_id": current_user.get_id(),
            "bill_id": str(uuid4()),
            "price": insureprice.item(),
            "status": False
        })
        db.bills.create(bill)
        return redirect(url_for('shop'))
    return render_template("insurance.html", form=insuranceform)


@app.route("/repair")
def repair():
    return render_template("repair.html")


@app.route("/test")
@login_required
def test():
    return render_template("test.html", user=current_user.get_name())


@app.route("/login", methods=["GET", "POST"])
def login():
    usersigninform = UserSignInForm()
    html = "login.html"
    if usersigninform.submit_user_signin.data and usersigninform.validate():
        email = usersigninform.email_signin.data
        password = usersigninform.password_signin.data
        remember = usersigninform.remember_me.data

        print("info:", email, password, remember)

        ret_code, user = db.users.find(email=email)
        match ret_code:
            case "USERNOTFOUND":
                return render_template(html, form=usersigninform, login_result="User not found")

            case "SUCCESS":
                try:
                    check_hash(password, user.get_password())
                except VerifyMismatchError:
                    return render_template(html, form=usersigninform, login_result="Incorrect password")

                login_user(user, remember=remember)
                print("info: logged in user at login, ", user.get_name(), current_user.get_name())
                return redirect(url_for("profile"))

            case _:
                return render_template(html, form=usersigninform, login_result=f"Internal server error, {user}")
    else:
        return render_template("login.html", form=usersigninform)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@app.route("/wheel")
@login_required
def wheel():
    return render_template("wheel.html")


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("401.html"), 401


@app.route("/wheelspin")
@login_required
def wheelspin():
    print(current_user.get_newuser())
    number = random.randint(1, 10000)
    section = number % 360
    if not current_user.get_newuser():
        return jsonify(spun=True)
    coupon = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    if section < 30:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 5,
            "expire": 1
        })
        value = 5
    elif section >= 330:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 5,
            "expire": 1
        })
        value = 5
    elif section >= 30 and section < 90:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 5,
            "expire": 1
        })
        value = 5
    elif section >= 90 and section < 150:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 10,
            "expire": 1
        })
        value = 10
    elif section >= 150 and section < 210:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 20,
            "expire": 1
        })
        value = 20
    elif section >= 210 and section < 270:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 10,
            "expire": 1
        })
        value = 10
    elif section >= 270 and section < 330:
        promo = Promo({
            "id": coupon,
            "type": "Value",
            "value": 5,
            "expire": 1
        })
        value = 5
    db.promos.create(promo)
    db.users.update({"id": current_user.get_id()}, {"newuser": False})
    return jsonify(number=number, section=section, spun=False, coupon=coupon, value=value)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("profile"))
    logout_user()  # request_loader gets called here, so we need to log out the user before signing up
    # print("info:", dict(current_user))
    html = "signup.html"
    form = UserCreationForm()
    if form.submit_user_create.data and form.validate():
        name = form.name_create.data + " " + form.name_last_create.data
        email = form.email_create.data
        address = form.address_create.data
        password = form.password_create.data
        password_confirm = form.password_confirm.data
        ret_code, _ = db.users.find(email=email)
        print("info:", ret_code)
        if ret_code == "SUCCESS":
            return render_template(html, form=form, result="Email already in use")

        user = User({
            "name": name,
            "password": get_hash(password),
            "id": str(uuid4()),
            "email": email,
            "address": address,
            "newuser": True,
            "admin": False
        })

        ret_code, user = db.users.create(user)
        match ret_code:
            case "SUCCESS":
                login_user(user)
                print("info: logged in user at signup, ", user.get_name(), current_user.get_name())
                return redirect(url_for("profile"))

            case _:
                return render_template(html, form=form, result=f"Internal server error, {user}")
    return render_template(html, form=form)


@app.route("/profile", methods=["POST", "GET"])
@login_required
def profile():
    html = "profile.html"
    form = UserUpdateForm()
    imageform = UserProfile()
    if imageform.submit_profile.data and imageform.validate():
        print(imageform.errors)
        file = imageform.image.data
        filename, file_extension = os.path.splitext(file.filename)
        new_filename = secure_filename(str(current_user.get_id()) + file_extension)
        file.filename = new_filename
        target = os.path.join(app.config["UPLOADED_PHOTOS_DEST"], new_filename)
        if os.path.isfile(target):
            os.remove(target)
        img = Image.open(file)

        img = img.resize((200, 200))

        img.save(target)
        db.users.update({"id": current_user.get_id()}, {"picture": new_filename})

        return render_template(html, form=form, imageform=imageform, result2="Profile picture updated", image=(
            url_for('static', filename=f'images/userprofileimg/{current_user.get_picture()}')))

    if form.submit_user_update.data and form.validate():

        first_name = form.name_update.data
        last_name = form.name_last_update.data
        email = form.email_update.data
        address = form.email_update.data
        password = form.old_password.data
        new_password = form.password_update.data
        password_confirm = form.password_confirm.data

        items = [first_name, last_name, email, address, password, new_password, password_confirm]
        print("info:",
              f"first_name: {first_name}, last_name: {last_name}, email: {email}, address: {address}, password: {password}, new_password: {new_password}, password_confirm: {password_confirm}")
        if not any(bool(i) for i in items):
            return render_template(html, form=form, imageform=imageform, result="You need at least 1 field filled out",
                                   image=(url_for('static',
                                                  filename=f'images/userprofileimg/{current_user.get_picture()}')))

        try:
            check_hash(password, current_user.get_password())
        except VerifyMismatchError:
            return render_template(html, form=form, imageform=imageform, result="Incorrect password", image=(
                url_for('static', filename=f'images/userprofileimg/{current_user.get_picture()}')))

        new = {}
        if first_name != "":
            new["name"] = first_name + " " + current_user.get_name().split()[1]
        if last_name != "":
            new["name"] = current_user.get_name().split()[0] + " " + last_name
        if first_name != "" and last_name != "":
            new["name"] = first_name + " " + last_name

        if email != "":
            ret_code, _ = db.users.find(email=email)
            if ret_code == "SUCCESS":
                return render_template(html, form=form, imageform=imageform, result="Email already in use", image=(
                    url_for('static', filename=f'images/userprofileimg/{current_user.get_picture()}')))
            new["email"] = email

        if address != "":
            new["address"] = address

        if new_password != "":
            new["password"] = get_hash(new_password)

        if len(new) == 0:
            return render_template(html, form=form, imageform=imageform, result="You need at least 1 field filled out",
                                   image=(url_for('static',
                                                  filename=f'images/userprofileimg/{current_user.get_picture()}')))

        ret_code, user = db.users.update({"id": current_user.get_id()}, new)
        match ret_code:
            case "SUCCESS":
                login_user(user)
                print("info: logged in user at profile, ", user.get_name(), current_user.get_name())
                return render_template(html, form=form, imageform=imageform, result="Profile updated", image=(
                    url_for('static', filename=f'images/userprofileimg/{current_user.get_picture()}')))

            case _:
                return render_template(html, form=form, imageform=imageform, result=f"Internal server error, {user}",
                                       image=(url_for('static',
                                                      filename=f'images/userprofileimg/{current_user.get_picture()}')))
    return render_template(html, form=form, imageform=imageform,
                           image=(url_for('static', filename=f'images/userprofileimg/{current_user.get_picture()}')))


@login_required
@app.route("/admin")
def admin_home():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    if not current_user.get_admin():
        return abort(401)
    
    return render_template("admin.html", ip_addr=request.remote_addr)

@login_required
@app.route("/admin/users", methods=["POST"])
def admin_search():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)

    if not current_user.get_admin():
        return abort(401)

    id = request.form.get("search")
    is_email = bool(re.search(r"^[\w\.-]+@[\w\.-]+\.\w+$", id)) # praying this works

    if not id:
        ret_code, users = db.users.find()
        if ret_code == "USERNOTFOUND":
            return abort(500)

        return render_template("admin_user.html", users=users, ip_addr=request.remote_addr)
    
    if is_email:
        ret_code, user = db.users.find(email=id)
    else:
        ret_code, user = db.users.find(user_id=id)

    if ret_code == "USERNOTFOUND":
        return render_template("admin_user.html", ip_addr=request.remote_addr, error="USER_NOT_FOUND", search=id)
    
    return render_template("admin_user.html", ip_addr=request.remote_addr, users=[user])

@login_required
@app.route("/admin/users")
def admin_users():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    if not current_user.get_admin():
        return abort(401)

    ret_code, users = db.users.find()
    if ret_code == "USERNOTFOUND":
        return abort(500) # TODO: actual error page
    
    return render_template("admin_user.html", users=users, ip_addr=request.remote_addr)

@login_required
@app.route("/admin/invoices")
def admin_bills():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    if not current_user.get_admin():
        return abort(401)
    
    ret_code, bills = db.bills.find()
    if ret_code == "BILLNOTFOUND":
        return abort(500)
    
    pairs = []
    for bill in bills:
        ret_code, user = db.users.find(user_id=bill.get_customer_id())  # why are we using customer instead of owner
        if ret_code == "USERNOTFOUND":
            db.bills.delete(bill.get_bill_id())
        
        pairs.append((bill, user))

    return render_template("admin_bill.html", bills=pairs, ip_addr=request.remote_addr)

@login_required
@app.route("/api/admin/create_user")
def create_user():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    logout_user()
    return redirect(url_for("signup"))

@login_required
@app.route("/api/admin/roles", methods=["POST"])
def update_roles():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)

    if not current_user.get_admin():
        return jsonify({"error": "Unauthorized"}), 401

    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400
    if not data.get("id"):
        return jsonify({"error": "Missing id"}), 400
    if data.get("role") is None:  # role can be False so cannot do 'not data.get(...)'
        return jsonify({"error": "Missing role"}), 400
    
    ret_code, user = db.users.find(user_id=data["id"])
    if ret_code == "USERNOTFOUND":
        return jsonify({"error": "User not found"}), 404
    
    if user.get_admin() == data["role"]:
        return jsonify({"error": "Role already set"}), 400
    
    ret_code, e = db.users.update({"id": data["id"]}, {"admin": data["role"]})
    if ret_code != "SUCCESS":
        return jsonify({"error": "Internal server error", "message": str(e)}), 500

    return jsonify({"success": "Role updated"}), 200

@login_required
@app.route("/api/admin/invoices/status", methods=["POST"])
def update_invoice_status():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    if not current_user.get_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json
    print(data)

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not data.get("id"):
        return jsonify({"error": "Missing id"}), 400
    
    if data.get("status") is None:
        return jsonify({"error": "Missing status"}), 400
    
    ret_code, bill = db.bills.find(bill_id=data["id"])
    print(ret_code, bill)
    if ret_code == "BILLNOTFOUND":
        return jsonify({"error": "Bill not found"}), 404
    
    if bill.get_status() == data["status"]:
        return jsonify({"error": "Status already set"}), 400
    
    ret_code, e = db.bills.update(data["id"], {"status": data["status"]})
    if ret_code != "SUCCESS":
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    return jsonify({"success": "Status updated"}), 200

@login_required
@app.route("/api/admin/password", methods=["POST"])
def admin_password():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)

    if not current_user.get_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not data.get("id"):
        return jsonify({"error": "Missing id"}), 400
    
    if not data.get("password"):
        return jsonify({"error": "Missing password"}), 400
    
    ret_code, user = db.users.find(user_id=data["id"])
    if ret_code == "USERNOTFOUND":
        return jsonify({"error": "User not found"}), 404
    
    ret_code, e = db.users.update({"id": data["id"]}, {"password": get_hash(data["password"])})
    if ret_code != "SUCCESS":
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    return jsonify({"success": "Password updated"}), 200

@login_required
@app.route("/api/admin/delete", methods=["POST"])
def delete_user():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)

    if not current_user.get_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not data.get("id"):
        return jsonify({"error": "Missing id"}), 400
    
    ret_code, user = db.users.find(user_id=data["id"])
    if ret_code == "USERNOTFOUND":
        return jsonify({"error": "User not found"}), 404
    
    if user.get_admin():
        return jsonify({"error": "Cannot delete admin"}), 400

    ret_code, e = db.users.delete(data.get('id'))
    
    if ret_code != "SUCCESS":
        return jsonify({"error": "Internal server error", "message": str(e)}), 500
    
    return jsonify({"success": "User deleted"}), 200

@login_required
@app.route("/api/admin/bills/delete", methods=["POST"])
def delete_bill():
    if isinstance(current_user, AnonymousUserMixin):
        return abort(401)
    
    if not current_user.get_admin():
        return jsonify({"error": "Unauthorized"}), 401
    
    data = request.json

    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    if not data.get("id"):
        return jsonify({"error": "Missing id"}), 400
    
    ret_code, bill = db.bills.delete(data.get('id'))
    if ret_code == "BILLNOTFOUND":
        return jsonify({"error": "Bill not found"}), 404
    elif ret_code == "ERROR":
        return jsonify({"error": "Internal server error", "message": str(bill)}), 500
    
    return jsonify({"success": "Bill deleted"}), 200


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404

@app.errorhandler(401)
def unauthorized(e):
    return render_template("401.html"), 401

if __name__ == "__main__":
    app.run(debug=True)
