
"""Flask config."""
from tempfile import mkdtemp
from os import path

TEMPLATES_AUTO_RELOAD = True

SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"

SECRET_KEY='Drmhze6EPcv0fN_81Bj-nA'

#SQLALCHEMY
SQLALCHEMY_DATABASE_URI = "postgres://pbgyupohiwokof:3f70cc356939727d7042944d5c92bbcc7f3d9c71fdfe7e2b9c9752110f666b02@ec2-34-197-141-7.compute-1.amazonaws.com:5432/d2ajb7mgl6ulaq"
SQLALCHEMY_ECHO = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Path for file Uploads
PDF_UPLOADS = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\form_uploads'
CSV_UPLOADS = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\data_uploads'

# Check uploaded files
ALLOWED_FILE_EXTENSIONS = ["PDF"]
MAX_CONTENT_LENGTH = 16 * 1024 * 1024
ALLOWED_DATA_FILE_EXTENSIONS =["CSV"]

# Path for new files rendered
FORM_OUTPUT = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\completed_forms'

