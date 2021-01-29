from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from . import models
from django.db.models import F


@receiver(post_save, sender=models.Message)
def created_message_handler(sender, instance, created, **kwargs):
    if not created:
        return
    instance.topic.message_count = F('message_count') + 1
    instance.topic.save(update_fields=['message_count'])
    instance.topic.subcategory.message_count = F('message_count') + 1
    instance.topic.subcategory.save(update_fields=['message_count'])


@receiver(post_save, sender=models.Topic)
def created_topic_handler(sender, instance, created, **kwargs):
    if not created:
        return
    instance.subcategory.topic_count = F('topic_count') + 1
    instance.subcategory.save(update_fields=['topic_count'])


