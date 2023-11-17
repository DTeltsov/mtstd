from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import AccountsSerializer, AccountsByLoginSerializer
from rest_framework.generics import CreateAPIView

from django.apps import apps as django_apps

from api.api import settings

UserModel = django_apps.get_model(settings.AUTH_USER_MODEL, require_ready=False)


class AuthView(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})


@extend_schema_view(post=extend_schema(
    "Create account"
))
class AccountsView(CreateAPIView):
    authentication_classes = tuple()
    permission_classes = tuple()
    serializer_class = AccountsSerializer


class AccountsByLoginView(ModelViewSet):
    serializer_class = AccountsByLoginSerializer

    def get_object(self):
        return self.request.user
