from django.urls import path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


def postprocess(result, **_):
    for path_name, api_path in result['paths'].items():
        for operation in api_path.values():
            if operation['tags'] == ['api_v1']:
                operation['tags'] = [path_name.split('/')[2]]
    return result


urlpatterns = [
    path('', SpectacularSwaggerView.as_view(url_name='schema')),
    path('redoc/', SpectacularRedocView.as_view(url_name='schema')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
]
