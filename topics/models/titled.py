from django.db import models


class Titled(models.Model):
    title = models.CharField(max_length=125)

    class Meta:
        abstract = True
