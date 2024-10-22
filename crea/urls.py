from django.contrib import admin
from django.urls import path, include
from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.conf import settings
schema_view = get_schema_view(
    openapi.Info(
        title="",
        default_version='v1',
        description="API ",
     

    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
    # url='http://127.0.0.1:8000/api/',
    # patterns=[path('api/', include('books.api.urls'))]


)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',include('crea_app.urls')),
    path('api/profile/', include('profiles.urls')),
    # path('api/gigwork/', include('gigwork.urls')), 
    
     ]


if settings.SHOW_SWAGGER:
    urlpatterns += [
        path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ]