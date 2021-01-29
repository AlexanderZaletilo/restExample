from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView
from .serializers import UserSerializer
from django.contrib.auth import get_user_model
from rest.permissions import IsOwnerOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet, ModelViewSet
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView


class UserListView(ListAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.select_related('profile')


class UserDetailView(RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.select_related('profile')
    permission_classes = [IsOwnerOrReadOnly]


