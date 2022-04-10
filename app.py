import os
import json
import requests
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
def coinvue():
    results = crypto.crypto_top_50()

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
    portfolios = []

    if session["user"] == username:
        user_portfolio_display = (
            mongo.db.portfolios.find_one({"username": session["user"]}))
        if user_portfolio_display is not None:
            portfolios = user_portfolio_display["id"]
            price = 0
            day_percent = 0

            results = {"id": []}

            for token in portfolios:
                tokens = token["tokens"]
                print("-----------------")
                print(tokens)

                url = f"http://api.coincap.io/v2/assets/{ tokens }"

                payload = {}
                headers = {}

                response = requests.request(
                    "GET", url, headers=headers, data=payload)
                json_data = json.loads(response.text.encode("utf8"))
                coin_data = json_data["data"]

                price = coin_data["priceUsd"]
                day_percent = coin_data["changePercent24Hr"]

                print(day_percent)
                print(price)

                new_results = results["id"]
                new_results.append({
                    "price": float(price),
                    "day_percent": float(day_percent)
                })

            print(results)
            token_id = results["id"]

    return render_template(("portfolio.html"), username=username,
                           portfolios=portfolios, token_id=token_id)


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


@app.route("/add_record", methods=["GET", "POST"])
# Remove select maybe from add record page
def add_record():
    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]
    results = crypto.crypto_top_50()
    # Add results at the bottom

    if request.method == "POST":

        record_type = request.form.get("record_type")
        quantity = request.form.get("quantity")
        per_coin = request.form.get("per_coin")
        total = float(quantity) * float(per_coin)
        date = request.form.get("date")
        notes = request.form.get("notes")

        token_data = request.form.get("token_data")
        token_dict = json.loads(token_data)
        token_id = token_dict['token_id']
        tokens = token_dict['token']

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

# =======================================================
#                       PORTFOILIO
# =======================================================

        price = 2
        # Update
        value = float(price) * float(quantity)
        profit_loss = float(value) - float(total)
        token_id_exists = False
        token_id_object = {}
        token_id_object_position = 0

        user_portfolio_contents = mongo.db.portfolios.find_one(
            {"username": session["user"]}
        )

        if user_portfolio_contents is not None:
            for position, token in enumerate(
                    user_portfolio_contents.get("id")):
                if token.get("token_id") == token_id:
                    token_id_exists = True
                    token_id_object = token
                    token_id_object_position = position
                    break
        # Loops through array for the "token" that matches the token_id

        find_portfolio_user = None
        if user_portfolio_contents is not None:
            find_portfolio_user = mongo.db.portfolios.find_one(
                {"username": session["user"]})["username"]
        # If a portfolio username matches the session user exists

        if user_portfolio_contents is None:
            my_portfolios = {
                "username": session["user"],
                "id": [{
                    "tokens": tokens,
                    "token_id": token_id,
                    "holdings": float(quantity),
                    "value": value,
                    "grand_total": total,
                    "profit_loss": profit_loss
                }]
            }
            mongo.db.portfolios.insert_one(my_portfolios)
        # If there are no portfolios matching the session user,
        # a new one is created

        elif (find_portfolio_user == username and
              token_id_exists is False):

            _id = user_portfolio_contents["_id"]
            # Gets portfolio by object id

            portfolio_contents = user_portfolio_contents["id"]
            portfolio_contents.append({
                "tokens": tokens,
                "token_id": token_id,
                "holdings": float(quantity),
                "value": value,
                "grand_total": total,
                "profit_loss": profit_loss
            })
            mongo.db.portfolios.update_one(
                {"_id": _id}, {"$set": {"id": portfolio_contents}})
        # If the username matches a document but is the first record,
        # of the token it adds a new instance to the array

        elif find_portfolio_user == username and token_id_exists is True:
            _id = user_portfolio_contents["_id"]
            portfolio_contents = user_portfolio_contents["id"]

            old_holdings = float(token_id_object.get("holdings"))

            updated_holdings = (float(quantity)
                                + float(old_holdings))
            updated_value = (float(price)
                             * float(updated_holdings))
            updated_total = (float(total)
                             + float(token_id_object.get("grand_total")))
            updated_profit = (float(updated_value)
                              - float(updated_total))
            # Calculates new portfolio contents adding,
            # new record to portfolio values

            if record_type in ["Buy", "Staking"]:
                portfolio_contents[token_id_object_position] = {
                    "tokens": tokens,
                    "token_id": token_id,
                    "holdings": updated_holdings,
                    "value": updated_value,
                    "grand_total": updated_total,
                    "profit_loss": updated_profit
                }
                mongo.db.portfolios.update_one(
                    {"_id": _id}, {"$set": {"id": portfolio_contents}})
            # Updates the user's portfolio by adding all matching,
            # token_id's records value

            elif record_type == "Sell":
                _id = user_portfolio_contents["_id"]
                portfolio_contents = user_portfolio_contents["id"]
                sell_holdings = (float(token_id_object.get("holdings")
                                 - float(quantity)))
                sell_total = (float(token_id_object.get("grand_total")
                              - float(token_id_object.get("value"))))
                # Calculates new portfolio contents subtracting,
                # new record to portfolio values

                portfolio_contents[token_id_object_position] = {
                    "tokens": tokens,
                    "token_id": token_id,
                    "holdings": sell_holdings,
                    "value": updated_value,
                    "grand_total": sell_total,
                    "profit_loss": updated_profit
                }
                mongo.db.portfolios.update_one(
                    {"_id": _id}, {"$set": {"id": portfolio_contents}})
            # Updates the user's portfolio by subtracting all matching,
            # token_id's records value

        flash("Record successfully added")
        return redirect(url_for("get_records",
                        username=username))

    return render_template("add_record.html", results=results)


@app.route("/edit_record/<record_id>", methods=["GET", "POST"])
def edit_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})

    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    if request.method == "POST":

        new_quantity = request.form.get("edit_quantity")
        new_per_coin = request.form.get("edit_per_coin")
        new_date = request.form.get("edit_date")
        new_notes = request.form.get("edit_notes")
        new_total = float(new_quantity) * float(new_per_coin)

        update_record = {
            "quantity": float(new_quantity),
            "per_coin": float(new_per_coin),
            "date": new_date,
            "notes": new_notes,
            "total": float(new_total)
        }
        mongo.db.records.update_one({"_id": ObjectId(record_id)},
                                    {"$set": update_record})

# =======================================================
#                       PORTFOILIO
# =======================================================

        price = 2
        # Subject to change
        token_id_exists = False
        token_id_object = {}
        token_id_object_position = 0
        token_id = record["token_id"]

        user_portfolio_contents = mongo.db.portfolios.find_one(
            {"username": session["user"]}
        )

        if user_portfolio_contents is not None:
            for position, token in enumerate(
                    user_portfolio_contents.get("id")):
                if token.get("token_id") == token_id:
                    token_id_exists = True
                    token_id_object = token
                    token_id_object_position = position
                    break

        find_portfolio_user = None
        if user_portfolio_contents is not None:
            find_portfolio_user = mongo.db.portfolios.find_one(
                {"username": session["user"]})["username"]

        if find_portfolio_user == username and token_id_exists is True:
            _id = user_portfolio_contents["_id"]
            portfolio_contents = user_portfolio_contents["id"]

            old_quantity = record["quantity"]
            old_total = record["total"]
            old_holdings = token_id_object.get("holdings")
            old_grand_total = token_id_object.get("grand_total")

            holdings = float(old_holdings) - float(old_quantity)
            grand_total = float(old_grand_total) - float(old_total)

            new_holdings = (float(new_quantity)
                            + float(holdings))
            new_value = (float(price)
                         * float(new_holdings))
            new_grand_total = (float(new_total)
                               + float(grand_total))
            new_profit = (float(new_value)
                          - float(new_grand_total))

            portfolio_contents[token_id_object_position] = {
                "token_id": token_id,
                "holdings": new_holdings,
                "value": new_value,
                "grand_total": new_total,
                "profit_loss": new_profit
            }
            mongo.db.portfolios.update_one({"_id": _id}, {"$set":
                                           {"id": portfolio_contents}})

        flash("Record successfully updated")
        return redirect(url_for("get_records", username=username))

    return render_template("edit_record.html", record=record)


@app.route("/delete_record/<record_id>", methods=["GET", "POST"])
def delete_record(record_id):
    record = mongo.db.records.find_one({"_id": ObjectId(record_id)})

    username = mongo.db.users.find_one(
            {"username": session["user"]})["username"]

    if request.method == "POST":

        price = 2
        # Subject to change
        token_id_exists = False
        token_id_object = {}
        token_id_object_position = 0
        token_id = record["token_id"]
        quantity = record["quantity"]
        total = record["total"]

        user_portfolio_contents = mongo.db.portfolios.find_one(
            {"username": session["user"]}
        )

        if user_portfolio_contents is not None:
            for position, token in enumerate(
                    user_portfolio_contents.get("id")):
                if token.get("token_id") == token_id:
                    token_id_exists = True
                    token_id_object = token
                    token_id_object_position = position
                    break

        find_portfolio_user = None
        if user_portfolio_contents is not None:
            find_portfolio_user = mongo.db.portfolios.find_one(
                {"username": session["user"]})["username"]

        if find_portfolio_user == username and token_id_exists is True:
            _id = user_portfolio_contents["_id"]
            portfolio_contents = user_portfolio_contents["id"]

            holdings = token_id_object.get("holdings")
            grand_total = token_id_object.get("grand_total")

            updated_holdings = float(holdings) - float(quantity)
            updated_value = float(price) * float(updated_holdings)
            updated_grand_total = float(grand_total) - float(total)
            updated_profit = float(updated_value) - (updated_grand_total)

            portfolio_contents[token_id_object_position] = {
                "token_id": token_id,
                "holdings": updated_holdings,
                "value": updated_value,
                "grand_total": updated_grand_total,
                "profit_loss": updated_profit
            }
            mongo.db.portfolios.update_one({"_id": _id}, {"$set":
                                           {"id": portfolio_contents}})
            mongo.db.records.delete_one({"_id": ObjectId(record_id)})

    flash("Record successfully removed")
    return redirect(url_for("get_records", record=record, username=username))


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
