''''from django.db import models
from profiles.models import Authored
from .time_stamped import TimeStamped
from .comment import Comment


class BaseLike(TimeStamped, Authored):

    class Meta:
        abstract = True


class PostLike(BaseLike):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)'''


