from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('docs/', include('api.swagger'), name='docs'),
    path('api_v1/', include([
        path('auth_api/', include('auth_api.urls'), name='login_user'),
        path('music/', include('music.urls'), name='music')]
    ))
]
