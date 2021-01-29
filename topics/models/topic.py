from profiles.models import Authored
from .categories import Titled, SubCategory
from django.db import models


class Topic(Titled, Authored):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    message_count = models.IntegerField(blank=True, default=0)

    def __str__(self):
        return f"Topic {self.title}; {self.message_count} messages"


