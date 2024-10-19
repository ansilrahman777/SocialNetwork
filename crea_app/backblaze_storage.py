from django.core.files.storage import Storage
import b2sdk.v2 as b2
from django.conf import settings

class BackblazeStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b2_api = self._authorize()

    def _authorize(self):
        # Authorize B2 API using the account info
        info = b2.InMemoryAccountInfo()
        b2_api = b2.B2Api(info)
        b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)
        return b2_api

    def _get_bucket(self):
        # Get the bucket using its name
        return self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    def _open(self, name, mode='rb'):
        # File download functionality can be added here later
        raise NotImplementedError("Download not implemented for Backblaze storage.")

    def _save(self, name, content):
        # Upload the file to Backblaze
        bucket = self._get_bucket()
        file_bytes = content.read()  # Read file content
        bucket.upload_bytes(file_bytes, name)  # Upload file to B2
        return name  # Return the file name or path as needed

    def exists(self, name):
        # Check if the file exists in Backblaze
        bucket = self._get_bucket()
        try:
            bucket.get_file_info_by_name(name)
            return True
        except b2.exception.FileNotPresent:  # Correct exception for file not found
            return False

    def url(self, name):
        # Generate the file URL
        return f"https://{settings.END_POINT_URL}/file/{settings.B2_BUCKET_NAME}/{name}"

import os
import re

def sanitize_filename(filename):
    # Get the base filename (no directory path)
    base_name = os.path.basename(filename)
    # Remove any unwanted characters (like backslashes) using regex
    sanitized_name = re.sub(r'[\\/:*?"<>|]', '', base_name)
    return sanitized_name


# Function to upload a file to Backblaze B2 and return the file URL
def upload_to_backblaze(file, user_id):
    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)

    # Authorize the B2 account
    b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)

    # Get the bucket for storing files
    bucket = b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    # Construct file path using user ID for organization
    file_name = file.name
    # Set the desired folder structure (e.g., "onboarding-images")
    folder_name = "onboarding-images"
    file_path = f"{folder_name}/{file_name}"  # Path example: "onboarding-images/filename.jpg"

    # Upload file content to Backblaze
    file_bytes = file.read()
    bucket.upload_bytes(file_bytes, file_path)

    # Return the URL to access the uploaded file
    file_url = f"https://{settings.END_POINT_URL}/file/{settings.B2_BUCKET_NAME}/{file_path}"
    return file_url
