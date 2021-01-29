from django.contrib import admin
from .models import Topic, Message, Category, SubCategory
from django_admin_inline_paginator.admin import TabularInlinePaginated


class MessageInline(TabularInlinePaginated):
    model = Message
    per_page = 10

    def get_queryset(self, request):
        return Message.objects.prefetch_related('user').prefetch_related('topic')


class TopicAdmin(admin.ModelAdmin):
    inlines = [MessageInline]
    readonly_fields = ['message_count']


class TopicInline(TabularInlinePaginated):
    model = Topic
    readonly_fields = ('message_count',)
    per_page = 50


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    readonly_fields = ('message_count', 'topic_count')

    def get_queryset(self, request):
        return SubCategory.objects.prefetch_related('category')


class CategoryAdmin(admin.ModelAdmin):
    inlines = [SubCategoryInline]


class SubCategoryAdmin(admin.ModelAdmin):
    inlines = [TopicInline]

    def get_queryset(self, request):
        return SubCategory.objects.prefetch_related('category')


admin.site.register(Category, CategoryAdmin)
admin.site.register(SubCategory, SubCategoryAdmin)
admin.site.register(Topic, TopicAdmin)
