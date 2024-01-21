from flask import Flask, render_template, request, redirect, url_for, jsonify
from argon2.exceptions import VerifyMismatchError
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import os
# import sys
import random
import string
from uuid import uuid4
# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api.db.driver import Driver
from api.structures.User import check_hash, User, get_hash
from api.structures.datavalidation import *
from api.structures.Promo import Promo

db = Driver()
app = Flask(__name__, static_url_path="/static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

login_manager = LoginManager()
login_manager.init_app(app)


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


@app.route("/contact")
def contact():
    return render_template("contact.html")


@app.route("/shop")
def shop():
    return render_template("shop.html")


@app.route("/insurance")
def insurance():
    return render_template("insurance.html")


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
                return redirect(url_for("test"))

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
    return 'Unauthorized cat', 401


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


@app.route("/signup")
def signup():
    return render_template("signup.html")


@app.route("/signup", methods=["POST"])
def signup_post():
    if current_user.is_authenticated:
        return redirect(url_for("test"))

    html = "signup.html"

    name = request.form.get("first-name") + " " + request.form.get("last-name")
    email = request.form.get("email")
    address = request.form.get("address")
    password = request.form.get("password")
    repeat_password = request.form.get("repeat-password")

    ret_code, _ = db.users.find(email=email)
    if ret_code == "SUCCESS":
        return render_template(html, result="Email already in use")

    if len(password) > 20 or len(password) < 8:
        return render_template(html, result="Password must be between 8 and 20 characters long")
    if password != repeat_password:
        return render_template(html, result="Passwords do not match")

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
            return redirect(url_for("test"))

        case _:
            return render_template(html, result=f"Internal server error, {user}")


if __name__ == "__main__":
    app.run(debug=True)
