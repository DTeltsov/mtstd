from drf_spectacular.utils import extend_schema_view, extend_schema
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .serializers import AccountsSerializer, AccountsByLoginSerializer
from rest_framework.generics import CreateAPIView, RetrieveAPIView

from django.apps import apps as django_apps
from .models import AccountUser


UserModel = django_apps.get_model('auth_api.AccountUser', require_ready=False)


@extend_schema_view(post=extend_schema(
    "Login"
))
class AuthView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={'request': request}
        )
        try:
            serializer.is_valid(raise_exception=True)
        except AccountUser.DoesNotExist:
            return Response({'detail': 'Wrong login or password'}, status=400)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_data': AccountsByLoginSerializer(user).data})


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


class LoginByToken(RetrieveAPIView):
    serializer_class = AccountsByLoginSerializer

    def get(self, request, *args, **kwargs):
        token = Token.objects.get(user=request.user)
        return Response({'token': token.key, 'user_data': AccountsByLoginSerializer(request.user).data})
