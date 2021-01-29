from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        exclude = ('user',)


class UserMessageSerializer(serializers.HyperlinkedModelSerializer):
    avatar = serializers.SerializerMethodField('get_avatar')

    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'avatar']

    def get_avatar(self, obj):
        try:
            return obj.profile.avatar.url
        except:
            return None


class UserSerializer(serializers.HyperlinkedModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = get_user_model()
        fields = ['url', 'username', 'profile']
        read_only_fields = ('url', 'username')

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile')
        profile = instance.profile
        profile.avatar = profile_data.get('avatar', profile.avatar)
        profile.status = profile_data.get('status', profile.status)
        profile.birthdate = profile_data.get('birthdate', profile.birthdate)
        profile.save()
        return instance



