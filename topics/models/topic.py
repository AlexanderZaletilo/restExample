from profiles.models import Authored
from .categories import Titled, SubCategory
from .message import Message
from django.db import models
from django.db.models import Manager


class TopicManager(Manager):
    def create(self, *args, **kwargs):
        text = kwargs.pop('text')
        topic = super().create(*args, **kwargs)
        Message.objects.create(text=text, user=kwargs['user'], topic=topic)
        return topic


class Topic(Titled, Authored):
    subcategory = models.ForeignKey(SubCategory, on_delete=models.PROTECT)
    message_count = models.IntegerField(blank=True, default=0)
    objects = TopicManager()

    def __str__(self):
        return f"Topic {self.title}; {self.message_count} messages"


