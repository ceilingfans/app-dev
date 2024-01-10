import sys
from flask import Flask, render_template, redirect , request
from pymongo import MongoClient
#set up actually good PYTHONPATH
sys.path.insert(1, "C://Users//mdame//OneDrive//Desktop//School//Sem 2//AppDevelopment//app-dev")
from api.structures.InsuredItem import InsuredItem
from api.db.driver import Driver
db = Driver()
app = Flask(__name__, static_url_path="/static")
app.config.update(dict(SECRET_KEY='yoursecretkey'))

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/contact")
def page():
    return render_template("contact.html")


@app.route("/CRUDTESTItem",methods=['GET','POST'])
def crudtest():
    if request.method == "POST":
        if request.form['submit'] == 'CreateItem':
            item = InsuredItem({
                "owner_id": request.form['Owner ID'],
                "item_id": db.generate_id(),
                "status": {
                    "damage": {
                        "description": request.form['dmgstatus'],
                        "date": 1704537866402
                    },
                    "repair_status": {
                        "past_repairs": [],
                        "current": {
                            "description": "Sent to our specialists for repair",
                            "start_date": 1704538866402,
                            "end_date": None
                        }
                    },
                    "address": request.form['address']
                },
                "subscription": {
                    "plan": "Bronze",
                    "duration": {
                        "start": 1704464537925,
                        "end": 1712353937925,
                        "length": 7889400000
                    }
                }
            })
            db.create_insured_item(item)
            return render_template("CRUDTESTItem.html")
        if request.form['submit'] == 'GetItem':
            return render_template("CRUDTESTItem.html",Userdata = db.find_insured_item(item_id=request.form['id']))
        if request.form['submit'] == 'UpdateItem':
            item = InsuredItem({
                "owner_id": request.form["upOwnerID"],
                "item_id": request.form["itemID"],
                "status": {
                    "damage": {
                        "description": request.form['upstatus'],
                        "date": 1704537866402
                    },
                    "repair_status": {
                        "past_repairs": [],
                        "current": {
                            "description": request.form['uprepairstatus'],
                            "start_date": 1704538866402,
                            "end_date": None
                        }
                    },
                    "address": request.form['upaddress']
                },
                "subscription": {
                    "plan": "Bronze",
                    "duration": {
                        "start": 1704464537925,
                        "end": 1712353937925,
                        "length": 7889400000
                    }
                }
            })
            return render_template("CRUDTESTItem.html",Updated = db.update_insured_item(item))
        if request.form['submit'] == 'DelItem':
            return render_template("CRUDTESTItem.html",Deleted = db.delete_insured_item_by_id(request.form['delid']))
    else:
        return render_template("CRUDTESTItem.html")

if __name__ == "__main__":
    app.run(debug=True)
