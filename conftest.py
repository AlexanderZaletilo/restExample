import pytest
from django.contrib.auth import get_user_model
from topics.models import *
import random


@pytest.fixture(scope='session')
def django_db_setup(django_db_setup, django_db_blocker):
    with django_db_blocker.unblock():
        cats = Category.objects.bulk_create([Category(title=name) for name in ('cat1', 'cat2', 'tech', 'music')])
        subs = SubCategory.objects.bulk_create(
            SubCategory(title=title, description=desc, category=cats[random.randint(0, 3)]) for title, desc in
                                    (('sub4', 'subcategory description'), ('subcategory', 'description'))
        )
        for i in range(10):
            user = get_user_model().objects.create(username=f'user{i}', password=str(i))
            topic = Topic.objects.create(title=f'topic{i}', user=user, subcategory=random.choice(subs), text="text")
        topics = Topic.objects.all()
        users = get_user_model().objects.all()
        for i in range(100):
            Message.objects.create(
                text="a"*random.randint(1, 10),
                topic=random.choice(topics),
                user=random.choice(users)
            )



@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()


@pytest.fixture
@pytest.mark.django_db
def create_user():
    while True:
        try:
            return lambda: (get_user_model().objects.create(
                username="".join([chr(random.randint(65, 90)) for _ in range(random.randint(1, 50))]),
                password='1234'
            ))
        except:
            pass


@pytest.fixture
def logged_user(api_client, create_user):
    user = create_user()
    api_client.force_authenticate(user)
    return api_client, user


