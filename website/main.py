from flask import Flask, render_template, request, redirect, url_for
from argon2.exceptions import VerifyMismatchError
from flask_login import login_user, login_required, logout_user, current_user, LoginManager
import os
import sys

#sys.path.append("C://Users//mdame//app-dev")

from api.db.driver import Driver
from api.structures.User import check_hash



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


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    html = "login.html"

    email = request.form.get("email")
    password = request.form.get("password")
    remember = request.form.get("remember-me") == "remember-me"

    print("info:", email, password, remember)

    ret_code, user = db.users.find(email=email)
    match ret_code:
        case "USERNOTFOUND":
            return render_template(html, login_result="User not found")

        case "SUCCESS":
            try:
                check_hash(password, user.get_password())
            except VerifyMismatchError:
                return render_template(html, login_result="Incorrect password")

            login_user(user, remember=remember)
            return redirect(url_for("test"))

        case _:
            return render_template(html, login_result=f"Internal server error, {user}")


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized cat', 401


if __name__ == "__main__":
    app.run(debug=True)
