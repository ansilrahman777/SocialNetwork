def cover_image_upload_to(instance, filename):
    return f'profiles/{instance.user.id}_{instance.user.username}/cover_image/{filename}'

def profile_image_upload_to(instance, filename):
    return f'profiles/{instance.user.id}_{instance.user.username}/profile_image/{filename}'

def document_upload_to(instance, filename):
    return f'profiles/{instance.user.id}_{instance.user.username}/document/{filename}'


