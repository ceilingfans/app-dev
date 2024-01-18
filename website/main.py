from flask import Flask, render_template

app = Flask(__name__, static_url_path="/static")


@app.route("/")
def home():
    return render_template("home.html")

@app.route("/contact.html")
def contact():
    return render_template("contact.html")

@app.route("/shop.html")
def shop():
    return render_template("shop.html")

@app.route("/repair.html")
def repair():
    return render_template("repair.html")



@app.route("/test")
def test():
    return render_template("test.html")


if __name__ == "__main__":
    app.run(debug=True)
