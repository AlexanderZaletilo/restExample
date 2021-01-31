from .models import Topic
from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Category, SubCategory, Message
from rest_framework.pagination import PageNumberPagination
from django.db.models import Max, Prefetch
from profiles.serializers import UserSerializer, UserMessageSerializer


def render_paginator_data(paginator, data):
    return {
        'next': paginator.get_next_link(),
        'previous': paginator.get_previous_link(),
        'results': data
    }


class MessageSerializer(serializers.ModelSerializer):
    user = UserMessageSerializer(read_only=True)

    class Meta:
        model = Message
        exclude = ('topic', 'id')
        read_only_fields = ('user',)


class TopicSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Topic
        exclude = tuple()
        read_only_fields = ('message_count',)


class TopicWithMessageListSerializer(TopicSerializer):
    message_set = serializers.SerializerMethodField('paginated_messages')

    def paginated_messages(self, obj):
        paginator = PageNumberPagination()
        paginator.page_size = 10
        page = paginator.paginate_queryset(
            obj.message_set.order_by('created').prefetch_related(
                Prefetch('user', queryset=get_user_model().objects.select_related('profile'))
            ),
            self.context['request']
        )
        serializer = MessageSerializer(page, many=True, context={'request': self.context['request']})
        return render_paginator_data(paginator, serializer.data)


class TopicLastMessageTimeSerializer(TopicSerializer):
    last_message_time = serializers.CharField(source='time')

    class Meta(TopicSerializer.Meta):
        exclude = ('subcategory', 'user')


class TopicCreationSerializer(serializers.ModelSerializer):
    message = serializers.CharField()

    class Meta:
        model = Topic
        fields = ['title', 'message']

    def create(self, validated_data):
        message = validated_data.pop('message')
        topic = Topic.objects.create(**validated_data,
                                     user=self.context['request'].user,
                                     subcategory_id=self.context['pk'],
                                     text=message)
        return topic


class SubCategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = SubCategory
        fields = ['title', 'url', 'description', 'message_count', 'topic_count']


class SubCategoryWithTopicListSerializer(SubCategorySerializer):
    topic_set = serializers.SerializerMethodField('paginated_topics')

    class Meta(SubCategorySerializer.Meta):
        fields = SubCategorySerializer.Meta.fields + ['topic_set']

    def paginated_topics(self, obj):
        paginator = PageNumberPagination()
        paginator.page_size = 50
        page = paginator.paginate_queryset(obj.topic_set.annotate(time=Max('message__created')), self.context['request'])
        serializer = TopicLastMessageTimeSerializer(page, many=True, context={'request': self.context['request']})
        return render_paginator_data(paginator, serializer.data)


class SubCategoryMainInlineSerializer(SubCategorySerializer):
    last_message_time = serializers.CharField(source='time')

    class Meta(SubCategorySerializer.Meta):
        fields = SubCategorySerializer.Meta.fields + ['last_message_time']


class CategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class CategoryWithSubsSerializer(CategorySerializer):
    subcategory_set = SubCategorySerializer(many=True)


class MainPageSerializer(serializers.HyperlinkedModelSerializer):
    subcategory_set = SubCategoryMainInlineSerializer(many=True)

    class Meta:
        model = Category
        fields = ['title', 'subcategory_set', 'url']


