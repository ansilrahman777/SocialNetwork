import os
import re
import b2sdk.v2 as b2
from django.conf import settings
from django.core.files.storage import Storage
from django.utils.deconstruct import deconstructible

def sanitize_filename(filename):
    """Sanitize filename to remove any invalid characters."""
    return re.sub(r'[\\/:*?"<>|]', '', os.path.basename(filename))

@deconstructible
class CustomBackblazeStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b2_api = self._authorize()

    def _authorize(self):
        """Authorize and return a B2Api instance."""
        info = b2.InMemoryAccountInfo()
        b2_api = b2.B2Api(info)
        b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)
        return b2_api

    def _get_bucket(self):
        """Retrieve the Backblaze bucket."""
        return self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    def _save(self, name, content):
        """Save a file to Backblaze, ensuring forward slashes in the path."""
        bucket = self._get_bucket()
        file_bytes = content.read()
        file_path = name.replace("\\", "/")
        bucket.upload_bytes(file_bytes, file_path)
        return file_path

    def url(self, name):
        """Return the URL for the saved file."""
        return f"https://{settings.B2_BUCKET_NAME}.{settings.END_POINT_URL}/{name.replace('\\', '/')}"

    def delete(self, name):
        """Delete a file from Backblaze."""
        bucket = self._get_bucket()
        file_info = bucket.get_file_info_by_name(name.replace("\\", "/"))
        bucket.delete_file_version(file_info.file_name, file_info.file_id)

    def exists(self, name):
        """Check if a file already exists."""
        try:
            self._get_bucket().get_file_info_by_name(name.replace("\\", "/"))
            return True
        except b2.exception.FileNotPresent:
            return False

def custom_upload_to(instance, filename, folder_type):

    user_folder = f"user/{instance.user.id}_{instance.user.username}"
    sanitized_filename = sanitize_filename(filename)

    if folder_type == "posts_images":
        path = f"{user_folder}/posts/images"
    elif folder_type == "posts_videos":
        path = f"{user_folder}/posts/videos"
    else:
        path = f"{user_folder}/{folder_type}"

    return f"{path}/{sanitized_filename}".replace("\\", "/")
