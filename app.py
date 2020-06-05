import os
import sqlite3

from flask import Flask, flash, jsonify, redirect, render_template, request, session
from flask_session.__init__ import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

app.config['SECRET_KEY'] = "Drmhze6EPcv0fN_81Bj-nA"


# Connect to sqlite database, set up dict

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
    
db = sqlite3.connect('forms.db', check_same_thread=False)
db.row_factory = dict_factory
cur = db.cursor()


# Register User
@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""

    # User reached route via link or url
    if request.method == "GET":
        return render_template("register.html")

    # User reached route via POST (as by submitting a form via POST)
    elif request.method == "POST":

       # Create user database
       #db.execute("CREATE TABLE 'users' ('id' INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 'username' TEXT NOT NULL, 'hash' TEXT NOT NULL)")
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            return apology("must confirm password", 403)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology("passwords do not match", 403)

        # Query database for username
        user = request.form.get("username")
        rows = cur.execute("SELECT * FROM users WHERE username =:username", {"username": user}).fetchall()
                          

        # Ensure username does not exist
        if len(rows) == 1:
            return apology("username unavailable", 403)

        # Store username and password into table
        
        hash = generate_password_hash(request.form.get("password"))
        user = request.form.get("username")
        cur.execute("INSERT INTO users (username, hash) VALUES(?,?)", (user, hash))
        db.commit()

        # Redirect user to home page
        return redirect("/")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        user = request.form.get("username")
        rows = cur.execute("SELECT * FROM users WHERE username=:username", {"username": user}).fetchall()
                          
        # Ensure username exists and password is correct
        if len(rows) != 1: 
            return apology("invalid username", 403)

        # Ensure password is correct 
        temp = request.form.get("password")
        if not check_password_hash(rows[0]["hash"], temp):
            return apology("invalid password", 403)
        
        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)

