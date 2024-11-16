import os
from uuid import uuid4
from datetime import datetime

def post_image_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}{ext}"
    return f"profiles/{instance.user.id}_{instance.user.username}/posts/images/{unique_filename}"

def post_video_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}{ext}"
    return f"profiles/{instance.user.id}_{instance.user.username}/posts/videos/{unique_filename}"

def headshot_upload_to(instance, filename):
    ext = os.path.splitext(filename)[-1].lower()
    unique_filename = f"{datetime.now().strftime('%Y%m%d%H%M%S')}_{uuid4().hex}{ext}"
    return f"profiles/{instance.user.id}_{instance.user.username}/headshots/{unique_filename}"

