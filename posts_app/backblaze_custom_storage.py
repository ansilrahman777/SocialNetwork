# import os
# import re
# import requests
# import b2sdk.v2 as b2
# from django.conf import settings
# from django.core.files.storage import Storage
# from django.utils.deconstruct import deconstructible
# from django.utils.text import slugify

# def sanitize_filename(filename):
#     """Sanitize filenames by removing invalid characters and enforce forward slashes."""
#     sanitized_name = re.sub(r'[\\/:*?"<>|]', '', filename)
#     return sanitized_name.replace("\\", "/")

# @deconstructible
# class CustomBackblazeStorage(Storage):
#     def __init__(self, *args, **kwargs):
#         """Initialize a custom Backblaze B2 storage instance."""
#         super().__init__(*args, **kwargs)
#         self.b2_api = self._authorize()

#     def _authorize(self):
#         """Authorize and create a B2Api instance."""
#         info = b2.InMemoryAccountInfo()
#         b2_api = b2.B2Api(info)
#         b2_api.authorize_account("production", settings.B2_ACCOUNT_ID, settings.B2_APPLICATION_KEY)
#         return b2_api

#     def _get_bucket(self):
#         """Get the bucket from Backblaze B2."""
#         return self.b2_api.get_bucket_by_name(settings.B2_BUCKET_NAME)

#     def _save(self, name, content):
#         """Save a file to Backblaze B2 storage, ensuring forward slashes in path."""
#         bucket = self._get_bucket()
#         file_bytes = content.read()
#         name = name.replace("\\", "/")
#         bucket.upload_bytes(file_bytes, name)
#         return name

#     def _open(self, name, mode='rb'):
#         """Open a file from Backblaze B2 storage."""
#         bucket = self._get_bucket()
#         file_info = bucket.get_file_info_by_name(name)
#         download_url = file_info.download_url
#         response = requests.get(download_url)
#         response.raise_for_status()
#         return response.content

#     def exists(self, name):
#         """Check if a file exists in Backblaze B2."""
#         bucket = self._get_bucket()
#         try:
#             bucket.get_file_info_by_name(name)
#             return True
#         except b2.exception.FileNotPresent:
#             return False

#     def url(self, name):
#         """Get the URL for accessing a file in Backblaze B2."""
#         return f"https://{settings.B2_BUCKET_NAME}.{settings.END_POINT_URL}/{name}"

#     def delete(self, name):
#         """Delete a file from Backblaze B2 storage."""
#         bucket = self._get_bucket()
#         file_info = bucket.get_file_info_by_name(name)
#         bucket.delete_file_version(file_info.file_name, file_info.file_id)

#     def size(self, name):
#         """Retrieve the file size in bytes from Backblaze B2 storage."""
#         bucket = self._get_bucket()
#         try:
#             file_info = bucket.get_file_info_by_name(name)
#             return file_info.size
#         except b2.exception.FileNotPresent:
#             return None

# def custom_upload_to(instance, filename, folder_type):
#     """Generate a custom path with forward slashes for Backblaze B2 storage."""
#     sanitized_filename = sanitize_filename(filename)
#     user_folder = f"user/{instance.user.id}_{instance.user.username}/{folder_type}"
#     return f"{user_folder}/{sanitized_filename}".replace("\\", "/")

# # Define specific functions for each upload type
# def post_image_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'posts/images')

# def post_video_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'posts/videos')

# def headshot_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'headshots')

# def profile_image_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'profile_images')

# def cover_image_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'cover_images')

# def document_upload_to(instance, filename):
#     return custom_upload_to(instance, filename, 'documents')

# def project_upload_to(instance, filename):
#     project_title_slug = slugify(instance.project_title)
    
#     extension = os.path.splitext(filename)[1].lower()
#     if extension in ['.jpg', '.jpeg', '.png', '.gif']:
#         folder = 'images'
#     elif extension in ['.mp4', '.avi', '.mov']:
#         folder = 'videos'
#     else:
#         folder = 'others'
#     return f'projects/{project_title_slug}/{folder}/{filename}'
