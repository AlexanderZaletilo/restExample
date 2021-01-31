import pytest
from rest_framework.reverse import reverse
from .models import *
from django.db.models import Count, Sum


@pytest.mark.django_db
def test_count():
    for topic in Topic.objects.annotate(msg_count=Count('message')):
        assert topic.message_count == topic.msg_count
    for subcat in SubCategory.objects.annotate(msg_count=Sum('topic__message_count'), tpc_count=Count('topic')):
        assert subcat.topic_count == subcat.tpc_count
        assert subcat.message_count == subcat.msg_count


@pytest.mark.django_db
def last_message(logged_user):
    api, user = logged_user
    msg = Message.objects.create(topic=Topic.objects.last(), user=user, text="<>")
    response = api.get(reverse('topic-messages', args=[msg.topic_id]) + '?page=last')
    assert response.data['message_set']['results'][-1]['text'] == '<>'
