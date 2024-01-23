from flask import Flask, render_template, request, redirect, url_for, jsonify
from argon2.exceptions import VerifyMismatchError
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import os
import sys
import random
import string
from uuid import uuid4
from dhooks import Webhook

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.db.driver import Driver
from api.structures.User import check_hash, User, get_hash
from api.structures.Promo import Promo
from api.Insuranceprice.getprice import getprice
from api.structures.Bill import Bill
from api.structures.datavalidation import *

db = Driver()
app = Flask(__name__, static_url_path="/static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")
login_manager = LoginManager()
login_manager.init_app(app)


@app.context_processor
def base():
    searchform = SearchForm()
    if searchform.submit_search and searchform.validate():
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
    if contactform.submit_contact and contactform.validate():
        print("info: contact form submitted")
        hook.send(
            f"Name: {contactform.name.data}\nEmail: {contactform.email.data}\nPhone Number: {contactform.phone_number.data}\nMessage: {contactform.message.data}")
        return render_template("contact.html", form=contactform, result="Your message has been sent")
    return render_template("contact.html", form=contactform)


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/insurance", methods=["GET", "POST"])
@login_required
def insurance():
    insuranceform = InsuranceForm()
    if insuranceform.submit_insure and insuranceform.validate():
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
        # TODO MAKE THIS ADD TO THE CART and redirect to cart page
        return render_template("insurance.html", form=insuranceform)
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
    if usersigninform.submit_user_signin and usersigninform.validate():
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
    if form.submit_user_create and form.validate():
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
            "newuser": True
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


@app.route("/profile")
@login_required
def profile():
    return render_template("profile.html")


@app.route("/profile", methods=["POST"])
@login_required
def profile_post():
    html = "profile.html"

    first_name = request.form.get("first-name")
    last_name = request.form.get("last-name")
    email = request.form.get("email")
    address = request.form.get("address")
    password = request.form.get("old-password")
    new_password = request.form.get("new-password")
    password_confirm = request.form.get("confirm-password")

    items = [first_name, last_name, email, address, password, new_password, password_confirm]
    print("info:",
          f"first_name: {first_name}, last_name: {last_name}, email: {email}, address: {address}, password: {password}, new_password: {new_password}, password_confirm: {password_confirm}")
    if not any(bool(i) for i in items):
        return render_template(html, result="You need at least 1 field filled out")

    if password != "":
        try:
            check_hash(password, current_user.get_password())
        except VerifyMismatchError:
            return render_template(html, result="Incorrect password")

        if new_password == "" or password_confirm == "":
            return render_template(html, result="You need to fill out all the password fields")

        if new_password != password_confirm:
            return render_template(html, result="New passwords do not match")

        if len(new_password) < 8:
            return render_template(html, result="New password must be at least 8 characters long")

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
            return render_template(html, result="Email already in use")
        new["email"] = email

    if address != "":
        new["address"] = address

    if new_password != "":
        new["password"] = get_hash(new_password)

    if len(new) == 0:
        return render_template(html, result="You need at least 1 field filled out")

    ret_code, user = db.users.update({"id": current_user.get_id()}, new)
    match ret_code:
        case "SUCCESS":
            login_user(user)
            print("info: logged in user at profile, ", user.get_name(), current_user.get_name())
            return render_template(html, result="Profile updated")

        case _:
            return render_template(html, result=f"Internal server error, {user}")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


if __name__ == "__main__":
    app.run(debug=True)
