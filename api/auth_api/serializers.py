import re
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import AccountUser, Subscription
from music.serializers import SongSerializer

def is_latin_string(string_to_check: str) -> bool:
    pattern = r'^[a-zA-Z0-9@.+\-_]+$'
    return bool(re.match(pattern, string_to_check))


def is_latin_string_with_space(string_to_check: str) -> bool:
    splitted = string_to_check.split()
    for i in splitted:
        pattern = r'^[a-zA-Z0-9@.+\-_]+$'
        if not re.match(pattern, i):
            return False
    return True


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = '__all__'


class AccountsByLoginSerializer(serializers.ModelSerializer):
    subscription_model = SubscriptionSerializer()
    songs = SongSerializer(many=True)

    class Meta:
        model = AccountUser
        fields = ('first_name', 'last_name', 'username', 'subscription_model', 'songs')


class AccountsSerializer(serializers.ModelSerializer):
    password = serializers.CharField(required=True, allow_null=False, allow_blank=False, write_only=True)
    default_validators = []

    class Meta:
        model = AccountUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def validate_last_name(self, attrs):
        self._validate_latin_string("last_name", attrs, with_space=True)
        return attrs

    def validate_first_name(self, attrs):
        self._validate_latin_string("first_name", attrs, with_space=True)
        return attrs

    def validate_username(self, attrs):
        self._validate_latin_string("username", attrs)
        return attrs

    def _validate_latin_string(self, field_name, string, with_space=False):
        spaces_info = "without spaces"
        fn = is_latin_string
        if with_space:
            spaces_info = "with/without spaces"
            fn = is_latin_string_with_space
        if not fn(string):
            raise ValidationError("Valid characters for {}: latins, digits, specials({}), {}".format(
                field_name, "@.+-_", spaces_info))

    def create(self, validated_data):
        validated_data['is_staff'] = True
        validated_data['password'] = make_password(validated_data['password'])
        return super(AccountsSerializer, self).create(validated_data)
