from django.db import models
from .titled import Titled


class Category(Titled):

    class Meta:
        verbose_name_plural = 'categories'

    def __str__(self):
        return f'Category {self.title}'


class SubCategory(Titled):
    description = models.CharField(max_length=125)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    topic_count = models.IntegerField(blank=True, default=0)
    message_count = models.IntegerField(blank=True, default=0)

    class Meta:
        verbose_name_plural = 'subcategories'

    def __str__(self):
        return f'SubCategory {self.category.title}/{self.title}; {self.topic_count} topics; {self.message_count} messages'

