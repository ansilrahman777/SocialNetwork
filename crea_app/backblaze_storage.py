from django.core.files.storage import Storage
import b2sdk.v2 as b2
from django.conf import settings
import os
import re
import requests

class BackblazeStorage(Storage):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.b2_api = self._authorize()

    def _authorize(self):
        info = b2.InMemoryAccountInfo()
        b2_api = b2.B2Api(info)
        b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)
        return b2_api

    def _get_bucket(self):
        return self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    def _open(self, name, mode='rb'):
        bucket = self._get_bucket()
        file_info = bucket.get_file_info_by_name(name)
        download_url = file_info.download_url
        response = requests.get(download_url)
        response.raise_for_status()
        return response.content

    def _save(self, name, content):
        bucket = self._get_bucket()
        file_bytes = content.read()
        bucket.upload_bytes(file_bytes, name)
        return name

    def exists(self, name):
        bucket = self._get_bucket()
        try:
            bucket.get_file_info_by_name(name)
            return True
        except b2.exception.FileNotPresent:
            return False

    def url(self, name):
        return f"https://{settings.END_POINT_URL}/file/{settings.B2_BUCKET_NAME}/{name}"

    def delete(self, name):
        bucket = self._get_bucket()
        bucket.delete_file_version(name, bucket.get_file_info_by_name(name).file_id)

    def size(self, name):
        bucket = self._get_bucket()
        try:
            file_info = bucket.get_file_info_by_name(name)
            return file_info.size
        except b2.exception.FileNotPresent:
            return None

def sanitize_filename(filename):
    base_name = os.path.basename(filename)
    sanitized_name = re.sub(r'[\\/:*?"<>|]', '', base_name)
    return sanitized_name

def upload_to_backblaze(file, user_id):
    info = b2.InMemoryAccountInfo()
    b2_api = b2.B2Api(info)
    b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)

    bucket = b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

    file_name = sanitize_filename(file.name)
    folder_name = "onboarding-images"
    file_path = f"{folder_name}/{user_id}/{file_name}"

    file_bytes = file.read()
    bucket.upload_bytes(file_bytes, file_path)

    file_url = f"https://{settings.END_POINT_URL}/file/{settings.B2_BUCKET_NAME}/{file_path}"
    return file_url
