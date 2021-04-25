import os
import pandas as pd

from flask import Flask, render_template, request
from flask_mail import Mail, Message

from helpers import query, top, full

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Sets configuration for sending emails
app.config["MAIL_PORT"] = 587
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = 'pynancialapp@gmail.com'
app.config["MAIL_DEFAULT_SENDER"] = 'pynancialapp@gmail.com'
app.config["MAIL_PASSWORD"] = 'SuperSecretPassword123!'
mail = Mail(app)

# Check for API key
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


""" Main Page for Searching for Value Stocks """
@app.route('/', methods=["GET", "POST"])
def index():

    if request.method == "POST":
        cap = request.form.get("cap")
        sector = request.form.get("sector")
        exchange = request.form.get("exchange")

        data = query(cap, sector, exchange)

        # Checks if function returned no stocks
        if not data:
            return render_template("error.html")

        else:
            # Sends data to dataframe
            df = pd.DataFrame(data, columns=["Symbol", "Price", "Est. Value", "Difference"])
            return render_template("results.html", df=df.to_html(index=False), cap=cap, sector=sector, exchange=exchange)

    else:
        return render_template("index.html")

""" For Auto-Search of Top Ten Value Stocks of the Day """
@app.route('/top', methods=["GET", "POST"])
def top_ten():

    if request.method == "POST":

        data = top()

        # Checks if function returned no stocks
        if not data:
            return render_template("error.html")

        else:
            df = pd.DataFrame(data, columns=["Symbol", "Price", "Est. Value", "Difference"])
            # Sorts by biggest price difference
            df = df.sort_values("Difference", ascending=False)
            df = df.head(10)
            return render_template("ten_results.html", df=df.to_html(index=False))

    else:
        return render_template("get_top.html")

""" Guide Page for Using App """
@app.route('/guide', methods=["GET"])
def guide():

    return render_template("guide.html")


""" Controls email sending if user provides email address """
@app.route('/send', methods=["POST"])
def send():

    email = request.form.get("email")

    if not email:
        return render_template("problem.html")

    # Grabs parameters from user's initial search to push them to larger search function
    cap = request.form.get("cap")
    sector = request.form.get("sector")
    exchange = request.form.get("exchange")

    data = full(cap, sector, exchange)

    # Probably unnecessary, but just in case the new/larger search encounters an error
    if not data:
        return render_template("error.html")

    else:

        df = pd.DataFrame(data, columns=["Symbol", "Price", "Est. Value", "Difference"])
        # Sort by the biggest price difference
        df = df.sort_values("Difference", ascending=False)

        # Sends dataframe to CSV to attach it to email more easily
        df.to_csv('df.csv', index=False)

        # Sends email with CSV of value stocks
        message = Message("Value Stocks from PyNancial", recipients=[email])
        message.body = "See the attached CSV file."
        with app.open_resource("df.csv") as fp:
            message.attach("df.csv", "df/csv", fp.read())

        mail.send(message)

        return render_template("sent.html")