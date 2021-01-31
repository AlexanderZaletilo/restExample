import pytest
from .models import Profile
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_profiles_equal_users(create_user):
    create_user()
    assert get_user_model().objects.count() == Profile.objects.count()


@pytest.mark.django_db
class TestProfileEdition:

    def test_your(self, logged_user):
        api, user = logged_user
        url = reverse('user-detail', args=[user.pk])
        assert api.put(url, {}, format='json').status_code != 403
        response = api.patch(url, {'profile': {'status': 'new_status'}}, format='json')
        user.profile.refresh_from_db(fields=['status'])
        assert response.status_code == 200 and user.profile.status == 'new_status'

    def test_anonymous(self, create_user, api_client):
        assert api_client.put(reverse('user-detail', args=[create_user().pk]), {}, format='json').status_code == 403

    def test_not_yours(self, logged_user, create_user):
        api, user = logged_user
        assert api.patch(reverse('user-detail', args=[create_user().pk])).status_code == 403
