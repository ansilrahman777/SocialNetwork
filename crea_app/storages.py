from storages.backends.s3boto3 import S3Boto3Storage
from django.conf import settings
 
class UthoStorage(S3Boto3Storage):
    bucket_name = settings.UTHO_STORAGE_BUCKET_NAME
    region_name = settings.UTHO_STORAGE_REGION
    endpoint_url = "https://creap2.innoida.utho.io/"
 
    def __init__(self, *args, **kwargs):
        kwargs['access_key'] = settings.UTHO_STORAGE_ACCESS_KEY
        kwargs['secret_key'] = settings.UTHO_STORAGE_SECRET_KEY
        super().__init__(*args, **kwargs)

    # def _normalize_name(self, name):
    #     if name.startswith(f"{self.bucket_name}/"):
    #         name = name[len(self.bucket_name) + 1:]
    #     return name.lstrip('/')

    
    # def _save(self, name, content):
    #     name = self._normalize_name(name)
    #     if name.startswith(f"{self.bucket_name}/"):
    #         name = name[len(self.bucket_name) + 1:]
    #     print(f"Final path for saving: {name}")
    #     return super()._save(name, content)

