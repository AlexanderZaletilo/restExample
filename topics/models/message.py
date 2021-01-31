from django.db import models
from profiles.models import Authored
from .time_stamped import TimeStamped


class Message(Authored, TimeStamped):
    topic = models.ForeignKey('Topic', on_delete=models.CASCADE)
    text = models.TextField()

    def __str__(self):
        return f'Message to {{{self.topic}}} at {self.created} by {self.user.username}: {self.text[:30]}{"..." if len(self.text) > 30 else ""}'
