import os
import psycopg2
import csv
import zipfile
import boto3

from psycopg2 import sql
from io import BytesIO
from flask import Flask, flash, jsonify, redirect, render_template, request, session, send_from_directory, send_file
from flask_session.__init__ import Session
from flask_sqlalchemy import SQLAlchemy
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

from helpers import apology, login_required, allowed_files, write_fillable_pdf, allowed_data, create_bucket, upload_file

# Configure application
app = Flask(__name__)
app.config.from_pyfile('config.py')

# Configure AWS
s3 = boto3.resource('s3')
my_bucket = "s3://bucketeer-e5202f86-104e-4258-9fe1-2aaa9178c5e0"

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Connect to postgres 

#def dict_factory(cursor, row):
   # d = {}
    #for idx, col in enumerate(cursor.description):
    #    d[col[0]] = row[idx]
    #return d


db = psycopg2.connect('postgres://pbgyupohiwokof:3f70cc356939727d7042944d5c92bbcc7f3d9c71fdfe7e2b9c9752110f666b02@ec2-34-197-141-7.compute-1.amazonaws.com:5432/d2ajb7mgl6ulaq')
#db.row_factory = dict_factory
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
            flash("must provide username")
            return redirect("register.html")

        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return redirect("register.html")
            

        # Ensure password was confirmed
        elif not request.form.get("confirmation"):
            flash("must confirm password")
            return redirect("register.html")
            

        elif request.form.get("password") != request.form.get("confirmation"):
            flash("passwords do not match")
            return redirect("register.html")
            

        # Query database for username
        user = request.form.get("username")
        query = sql.SQL("select * from {table} where {key} = %s").format(
            table=sql.Identifier('users'),
            key=sql.Identifier('username'))
        cur.execute(query, (user,))
        rows = cur.fetchall()

        # Ensure username does not exist
        if len(rows) == 1:
            flash("username unavailable")
            return redirect("/register")

        #TODO ADD EMAIL to form    
        # Store username and password into table
        hash = generate_password_hash(request.form.get("password"))
        user = request.form.get("username")
        cur.execute(sql.SQL("INSERT INTO {table} ({key}, {hkey}) VALUES(%s,%s)").format(
        table=sql.Identifier('users'),
        key=sql.Identifier('username'),
        hkey=sql.Identifier('hash')),
        (user, hash)) 
        
        db.commit()

        # Create User Bucket
        bucket_name = user + "bucket"
        folder_name = "form_uploads/"
        create_bucket(bucket_name)
        s3.put_object(Bucket=bucket_name, Key=(folder_name))


        # Redirect user to home page
        return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            flash("must provide username")
            return render_template("login.html")
            
        # Ensure password was submitted
        elif not request.form.get("password"):
            flash("must provide password")
            return render_template("login.html")
            
        # Query database for username
        user = request.form.get("username")
        query = sql.SQL("select * from {table} where {key} = %s").format(
            table=sql.Identifier('users'),
            key=sql.Identifier('username'))
        cur.execute(query, (user,))
        rows = cur.fetchall()

                     
        # Ensure username exists and password is correct
        if len(rows) != 1: 
            flash("invalid username")
            return render_template("login.html")

        # Ensure password is correct 
        temp = request.form.get("password")

        cur.execute(sql.SQL("Select * from {table} where {key} = %s").format(
        table=sql.Identifier('users'),
        key=sql.Identifier('username')),
        [user])
        row = cur.fetchone()
        
        if not check_password_hash(row[2], temp):
            flash("invalid password")
            return render_template("login.html")
        
        # Remember which user has logged in
        session["user_id"] = row[0]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/", methods=["GET", "POST"])
@login_required

def index():
    """Show uploaded files"""
    if request.method == "GET":
        x = os.listdir("./form_uploads")
        y = os.listdir("./data_uploads")
        return render_template("index.html", x=x, y=y)

    else:
        # Get csv filename from form
        filename = request.form.get("csv")
        file_to_open = os.path.join("./data_uploads", filename)

        # Get pdf filename from form
        formname = request.form.get("pdf")
        template_pdf = os.path.join("./form_uploads", formname)
        
        # Open csv and read key/value pairs into dictionary
        with open(file_to_open, 'r') as csvfile:
            info = csv.DictReader(csvfile)
            n = 1
            for row in info:
                save_as = "output" + str(n)
                write_fillable_pdf(template_pdf, os.path.join(app.config["FORM_OUTPUT"], save_as + ".pdf"), row)
                n = n + 1
            flash("Sucess!")

    return redirect("/download-forms")

# Download Completed Forms
@app.route("/download-forms", methods=["GET", "POST"])
def downloadforms():
    """Return Forms to User for Download"""  
    if request.method == "GET":
        x = os.listdir("./completed_forms")
        return render_template("download-forms.html", x=x)

    else:
        if request.form['submit'] == 'download_one':
            dwn = request.form.get("download")

            if dwn == None:
                flash("Select file to download")
                return redirect("/download-forms")

            else:
                return send_from_directory(directory="./completed_forms/", filename=dwn, as_attachment=True)
        
        elif request.form['submit'] == 'download_all':

            zipf = zipfile.ZipFile('complete.zip','w', zipfile.ZIP_DEFLATED)

            files = os.listdir('./completed_forms')
            for x in files:
                zipf.write(os.path.join('./completed_forms/', x), x)
            zipf.close()

            
            return send_file('complete.zip',
                mimetype = 'zip',
                attachment_filename= 'complete.zip',
                as_attachment = True)
        
                
               
        return redirect("/download-forms")


# Upload files
@app.route("/upload", methods=["GET", "POST"])
def uploadpdf():
    """Get PDF from User"""
    if request.method == "POST":
              
        if request.form['submit'] == 'submit_pdf':
            
            pdf = request.files["pdf"]

            if pdf.filename == "":
                flash("No filename")
                return redirect(request.url)
            
            if allowed_files(pdf.filename):
                filename = secure_filename(pdf.filename)
                pdf.save(os.path.join(app.config["PDF_UPLOADS"], filename))
                flash("Form saved")

            else:
                flash("That file extension is not allowed")
                return redirect(request.url)
        
        elif request.form['submit'] == 'submit_csv_data':
            
            data = request.files["csv_data"]

            if data.filename == "":
                flash("No filename")
                return redirect(request.url)
            
            if allowed_data(data.filename):
                filename = secure_filename(data.filename)
                data.save(os.path.join(app.config["CSV_UPLOADS"], filename))
                flash("Form saved")

            else:
                flash("That file extension is not allowed")
                return redirect(request.url)

    return render_template("upload.html")
    
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

