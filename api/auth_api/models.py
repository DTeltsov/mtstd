from django.db import models
from django.core.exceptions import ValidationError
from music.models import Song
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone


class Subscription(models.Model):
    active = models.BooleanField(default=True)
    start_date = models.DateTimeField(auto_now_add=True)
    end_date = models.DateTimeField()

    class Meta:
        db_table = 'subscription'

    def __str__(self):
        return f'{self.start_date} - {self.end_date}'

    def clean(self):
        if (self.start_date and self.end_date <= self.start_date) or (self.end_date <= timezone.now()):
            raise ValidationError({'end_date': "Must be after start date"})


class AccountUser(AbstractUser):
    first_name = models.CharField(_('first name'), max_length=30)
    last_name = models.CharField(_('last name'), max_length=150)
    subscription_model = models.OneToOneField(Subscription, blank=True, null=True, on_delete=models.DO_NOTHING)
    songs = models.ManyToManyField(Song, related_name='users', related_query_name='user')
    display_field = 'username'

    class Meta:
        permissions = (
            ("debug_toolbar", "Can view toolbar"),
        )
