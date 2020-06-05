
"""Flask config."""
from tempfile import mkdtemp
from os import path

TEMPLATES_AUTO_RELOAD = True

SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SECRET_KEY='Drmhze6EPcv0fN_81Bj-nA'

# Path for PDF Uploads
PDF_UPLOADS = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\form_uploads'
ALLOWED_FILE_EXTENSIONS = ["PDF"]
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

