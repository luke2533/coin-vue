import os
import uuid
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from coinvue import Crypto
if os.path.exists("env.py"):
    import env

app = Flask(__name__)

crypto = Crypto()

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")


@app.route("/coinvue")
def coinvue():
    results = crypto.crypto_top_100()

    for result in results:

        cryptoPrice = float(result["priceUsd"])
        cryptoPercent = float(result["changePercent24Hr"])
        cryptoMcap = float(result["marketCapUsd"])
        cryptoVolume = float(result["volumeUsd24Hr"])

        # token_id = result["id"]
        # token_id = [result["id"]]

        # for token in token_id:
        #     print(token)

        result["priceUsd"] = "$" + "{:.4f}".format(cryptoPrice)
        result["changePercent24Hr"] = "{:.4f}%".format(cryptoPercent)
        result["marketCapUsd"] = "$" + "{:.4f}".format(cryptoMcap)
        result["volumeUsd24Hr"] = "$" + "{:.4f}".format(cryptoVolume)

    return render_template("index.html", results=results)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already exisits")
            return redirect(url_for("signup"))

        password = request.form.get("password")
        check_password = request.form.get("confirm-password")
        email = request.form.get("email")
        check_email = request.form.get("confirm-email")

        if password != check_password:
            flash("Please make sure the passwords match")
            return redirect(url_for("signup"))

        if email != check_email:
            flash("Please make sure the emails match")
            return redirect(url_for("signup"))

        new_user = {
            "username": request.form.get("username").lower(),
            "email": request.form.get("email"),
            "password": generate_password_hash(request.form.get("password"))
        }
        mongo.db.users.insert_one(new_user)

        session["user"] = request.form.get("username").lower()
        flash("Register complete")
        return redirect(url_for("coinvue"))
        # Change to portfolio
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username")})

        if existing_user:
            if check_password_hash(existing_user["password"],
                                   request.form.get("password")):
                session["user"] = request.form.get("username")
                flash("Welcome, {}".format(request.form.get("username")))
                return redirect(url_for("coinvue"))
                # Change to portfolio
            else:
                # Wrong password
                flash("Inccorect username and/or password")
                return redirect(url_for("login"))
        else:
            # Username doesn't exist
            flash("Inccorect username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    flash("You have been logged out")
    session.pop("user")
    return redirect(url_for("login"))


@app.route("/portfolio")
def portfolio():
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    return render_template(("portfolio.html"), username=username)


@app.route("/get_record/<username>")
def get_records(username):
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]

    if session["user"] == username:
        user_records = mongo.db.records.find({"username": session["user"]}
                                             ).sort("date", -1)
    # Will need to add the id to this bit i think or if statement

    return render_template(("records.html"), username=username,
                           user_records=user_records)


# @app.route("/add_record/<token_id>", methods=["GET", "POST"])
@app.route("/add_record", methods=["GET", "POST"])
# <token_id> // Like Bitcoin
# Remove select maybe from add record page
def add_record():
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    results = crypto.crypto_top_100()

    if request.method == "POST":

        record_type = request.form.get("record_type")
        quantity = request.form.get("quantity")
        per_coin = request.form.get("per_coin")
        total = float(quantity) * float(per_coin)
        date = request.form.get("date")
        notes = request.form.get("notes")

        token_id = request.form.get("token_id")
        # Subject to change

        records = {
            "username": session["user"],
            "record_type": record_type,
            "token_id": token_id,
            "quantity": float(quantity),
            "per_coin": float(per_coin),
            "date": date,
            "notes": notes,
            "total": float(total)
        }
        mongo.db.records.insert_one(records)
        flash("Record successfully added")
        return redirect(url_for("get_records",
                        username=username, results=results))

    return render_template("add_record.html")


@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    if request.method == "POST":

        edit_quantity = request.form.get("edit_quantity")
        edit_per_coin = request.form.get("edit_per_coin")
        edit_date = request.form.get("edit_date")
        edit_notes = request.form.get("edit_notes")
        edit_total = float(edit_quantity) * float(edit_per_coin)

        update_record = {
            "quantity": float(edit_quantity),
            "per_coin": float(edit_per_coin),
            "date": edit_date,
            "notes": edit_notes,
            "total": float(edit_total)
        }
        mongo.db.records.update_one({"_id": ObjectId(record_id)},
                                    {"$set": update_record})
        flash("Record successfully updated")
        return redirect(url_for("get_records", username=username))

    return render_template("edit_record.html", record=record)


@app.route("/delete_record/<record_id>", methods=["GET", "POST"])
def delete_record(record_id):
    delete = mongo.db.records.delete_one({"_id": ObjectId(record_id)})
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    flash("Record successfully removed")
    return redirect(url_for("get_records", delete=delete, username=username))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
