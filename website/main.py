from flask import Flask, render_template, request, redirect, url_for
from argon2.exceptions import VerifyMismatchError
import flask_login
import os

from api.db.driver import Driver
from api.structures.User import check_hash

db = Driver()
app = Flask(__name__, static_url_path="/static")
app.secret_key = os.environ.get("FLASK_SECRET_KEY")

login_manager = flask_login.LoginManager()
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


@app.route("/test")
@flask_login.login_required
def test():
    return render_template("test.html", user=flask_login.current_user.get_name())


@app.route("/login")
def login():
    return render_template("login.html")


@app.route("/login", methods=["POST"])
def login_post():
    html = "login.html"

    email = request.form.get("email")
    password = request.form.get("password")

    print("info:", email, password)

    ret_code, user = db.users.find(email=email)
    match ret_code:
        case "USERNOTFOUND":
            return render_template(html, login_result="User not found")

        case "SUCCESS":
            try:
                check_hash(password, user.get_password())
            except VerifyMismatchError:
                return render_template(html, login_result="Incorrect password")

            flask_login.login_user(user)
            return redirect(url_for("test"))

        case _:
            return render_template(html, login_result=f"Internal server error, {user}")


@app.route("/logout")
def logout():
    flask_login.logout_user()
    return redirect(url_for("home"))


@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized cat', 401


if __name__ == "__main__":
    app.run(debug=True)
