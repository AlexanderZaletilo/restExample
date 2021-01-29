from django.db import models
from django.conf import settings


class Authored(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)

    class Meta:
        abstract = True


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, primary_key=True, on_delete=models.CASCADE)

    avatar = models.ImageField(upload_to='images/', null=True, blank=True)

    status = models.CharField(max_length=255, blank=True)

    birthdate = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Profile {self.user.username}; birth: {self.birthdate}'
