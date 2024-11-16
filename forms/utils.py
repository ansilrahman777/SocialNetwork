def project_upload_to(instance, filename):
    return f'profiles/{instance.user.id}_{instance.user.username}/document/{filename}'