
"""Flask config."""
from tempfile import mkdtemp
from os import path

TEMPLATES_AUTO_RELOAD = True

SESSION_FILE_DIR = mkdtemp()
SESSION_PERMANENT = False
SESSION_TYPE = "filesystem"
SECRET_KEY='Drmhze6EPcv0fN_81Bj-nA'

# Path for file Uploads
PDF_UPLOADS = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\form_uploads'
CSV_UPLOADS = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\data_uploads'

# Check uploaded files
ALLOWED_FILE_EXTENSIONS = ["PDF", "CSV"]
MAX_CONTENT_LENGTH = 16 * 1024 * 1024

# Path for new files rendered
FORM_OUTPUT = r'c:\Users\SUC\Desktop\Projects\GitHub\form-fill-project\completed_forms'
