import os
import csv
import pdfrw


import urllib.parse

from flask import redirect, render_template, request, session, jsonify
from functools import wraps
from collections import OrderedDict

def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def allowed_files(filename):
    """ check if PDF """
    from app import app

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_FILE_EXTENSIONS"]:
        return True
    else:
        return False


def allowed_data(filename):
    """ check if CSV """
    from app import app

    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_DATA_FILE_EXTENSIONS"]:
        return True
    else:
        return False


# PDF configuration
""" from Jake @ https://bostata.com/how-to-populate-fillable-pdfs-with-python/ """
ANNOT_KEY = '/Annots'
ANNOT_FIELD_KEY = '/T'
ANNOT_VAL_KEY = '/V'
ANNOT_RECT_KEY = '/Rect'
SUBTYPE_KEY = '/Subtype'
WIDGET_SUBTYPE_KEY = '/Widget'

def write_fillable_pdf(input_pdf_path, output_pdf_path, data_dict):

    template_pdf = pdfrw.PdfReader(input_pdf_path)
   # Set Apparences ( Make Text field visible )
    template_pdf.Root.AcroForm.update(pdfrw.PdfDict(NeedAppearances=pdfrw.PdfObject('true')))

    # Loop all Annotations
    for annotation in template_pdf.pages[0]['/Annots']:
    #   Only annotations that are Widgets Text
        if annotation['/Subtype'] == '/Widget' and annotation['/T']: 
            key = annotation[ANNOT_FIELD_KEY][1:-1]
            if key in data_dict.keys():
                annotation.update(pdfrw.PdfDict(V=f'{data_dict[key]}') )
                print(f'={key}={data_dict[key]}=')
        pdfrw.PdfWriter().write(output_pdf_path, template_pdf)   
    return None   

