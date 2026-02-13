from ckeditor_uploader.views import upload as ckeditor_upload
from django.contrib.auth.decorators import login_required

# wrap the upload view so that any logged-in user can upload
upload = login_required(ckeditor_upload)