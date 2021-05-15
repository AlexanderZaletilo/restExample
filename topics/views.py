from .serializers import CategorySerializer, SubCategorySerializer,\
    TopicSerializer, CategoryWithSubsSerializer, SubCategoryWithTopicListSerializer, MainPageSerializer,\
    TopicCreationSerializer, TopicWithMessageListSerializer, MessageSerializer
from .models import Topic, Category, SubCategory
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.decorators import action
from rest_framework.views import APIView, Response
from rest_framework.generics import ListAPIView
from django.db.models import Prefetch, Max
from django.http import HttpResponseBadRequest, HttpResponse
from rest_framework import permissions
from rest_framework import status


class ActionsSerializerMixin:
    action_serializers = {}

    def get_serializer_class(self):
        return self.action_serializers.get(self.action, super().get_serializer_class())


class CategoryViewSet(ActionsSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    pagination_class = None
    action_serializers = {'subcategories': CategoryWithSubsSerializer}

    @action(detail=True)
    def subcategories(self, request, pk=None):
        return self.retrieve(request, pk)


class SubCategoryViewSet(ActionsSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = SubCategorySerializer
    queryset = SubCategory.objects.all()
    action_serializers = {'topics': SubCategoryWithTopicListSerializer}
    pagination_class = None

    @action(detail=True, methods=['GET', 'POST'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def topics(self, request, pk=None):
        if request.method == 'GET':
            return self.retrieve(request, pk)
        else:
            serializer = TopicCreationSerializer(data=request.data, context={'request': request, 'pk': pk})
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)


class TopicViewSet(ActionsSerializerMixin, ReadOnlyModelViewSet):
    serializer_class = TopicSerializer
    queryset = Topic.objects.all()
    action_serializers = {'messages': TopicWithMessageListSerializer}
    pagination_class = None

    @action(detail=True, methods=['GET', 'POST'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def messages(self, request, pk=None):
        if request.method == 'GET':
            return self.retrieve(request, pk)
        else:
            serializer = MessageSerializer(data=request.data)
            if not serializer.is_valid():
                return Response(status=status.HTTP_400_BAD_REQUEST)
            serializer.save(topic_id=pk, user=request.user)
            return Response(status=status.HTTP_201_CREATED)


class MainView(ListAPIView):
    serializer_class = MainPageSerializer
    queryset = Category.objects.prefetch_related(
            Prefetch('subcategory_set', queryset=SubCategory.objects.annotate(time=Max('topic__message__created')))
    )
    pagination_class = None







